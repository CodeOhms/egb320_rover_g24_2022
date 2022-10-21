from glob import glob
from multiprocessing import Process, current_process
import numpy as np
import time
from time import sleep
from queue import SimpleQueue
from navigation.nav_state_machine import NavSMachine
from mobility import mobility as mob
from mobility.mobility_enums import *
from navigation.navigation_parallel.nav_helpers import *

class NavigationInternalData(object):
    def __init__(self, nav_process, vis_to_nav_callbacks, actions_q, bearings_q, distances_q, nav_smachine, nav_smachine_impl, retrieved_samples, pf_max):
        self.nav_process = nav_process
        self.vis_to_nav_callbacks = vis_to_nav_callbacks
        self.vis_get_bearings, self.vis_get_distances = vis_to_nav_callbacks
        self.actions_q = actions_q
        self.bearings_q = bearings_q
        self.distances_q = distances_q
        self.nav_smachine = nav_smachine
        self.nav_smachine_impl = nav_smachine_impl
        self.retrieved_samples = retrieved_samples
        self.pf_max = pf_max

def do_close_nav_loop(acts_q):
    try:
        actions = acts_q.get(block=False)
        if actions[0] == 'close':
            # Add back in queue for mobility system to close:
            acts_q.put( ('close',) )
            return False
    except:
        pass # Nothing in queue, yet
    return True

def nav_loop(nav_smachine_impl):
    nav_internal_data = nav_smachine_impl.nav_internal_data
    acts_q = nav_internal_data.actions_q
    nav_smachine = nav_internal_data.nav_smachine
    
    loop = do_close_nav_loop(acts_q)
    
    # Start the state machine!
    nav_smachine.start()
    print(nav_smachine.current_state)
    
    while(loop):
        cb, cb_args = nav_smachine_impl.get_next_state_callback()
        if cb_args is not None:
            cb(cb_args)
        else:
            cb()
        
        #print(nav_smachine.current_state)
        
        loop = do_close_nav_loop(acts_q)
    
    print('CLOSED NAV LOOP!')
    
    nav_internal_data.nav_smachine.close()

def nav_main(actions_q, bearings_q, distances_q, vis_to_nav_callbacks):
    nav_process = current_process()
    
    nav_smachine_impl = NavSMachine_impl()
    nav_smachine = NavSMachine(nav_smachine_impl)
    nav_smachine.init()
    
    retrieved_samples = 0
    pf_max = 276.0
    
    nav_internal_data = NavigationInternalData(
        nav_process, vis_to_nav_callbacks, actions_q, bearings_q,
        distances_q, nav_smachine, nav_smachine_impl, retrieved_samples, pf_max
    )
    
    nav_smachine_impl.set_nav_internal_data(nav_internal_data)

    nav_loop(nav_smachine_impl)

def init_parallel_impl(vis_to_nav_callbacks, actions_queue, bearings_q, distances_q,):
    actions_q = actions_queue
    nav_process = Process(target=nav_main, args=(actions_q, bearings_q, distances_q, vis_to_nav_callbacks))
    
    return nav_process

def start_parallel_impl(nav_process):
    nav_process.start()

def close_parallel_impl(nav_process, actions_q):
    actions_q.put( ('close',) )
    nav_process.join()

# State machine functions implementations:
class NavSMachine_impl(object):
    def __init__(self):
        self.nav_internal_data = None
        self.nxt_st_cb = (None, None) # 1st index is the callback, 2nd are the args
        self.target = Targets.sample
    
    def set_nav_internal_data(self, nav_internal_data):
        self.nav_internal_data = nav_internal_data

    # Functions unrelated to state machine library:
    def close(self):
        pass

    def set_next_state_callback(self, next_state_callback, args=None):
        self.nxt_st_cb = (next_state_callback, args)

    def get_next_state_callback(self):
        return self.nxt_st_cb

    # Functions run on transistions:
    def on_start(self):
        print('Starting navigation state machine...')
    
    def on_find_target(self):
        pass
                   
    def on_approach_target(self):
        pass

    # def on_obtain_sample(self):
    #     # Move claw down, and stop:
    #     decision = (('stop'), ('claw_down'))
    #     # Need to provide decision and stop here first:
    #     yield decision
        
    #     # Now we can continue:
    #     distance = vis_get_distances()
        
    #     # Move forward a bit:
    #     decision = (['left_f', 30], ['right_f', 30])
    #     yield decision
    #     sleep(0.2*distance[2][0]) # Allow to move forward a bit.
        
    #     # Lift sample, hopefully:
    #     decision = (('claw_lift'), ('stop'))
    #     yield decision
    #     sleep(0.5) # Allow ball to roll, if fumbled.
    #     distance = vis_get_distances()
    #     # Did the ball roll far?:
    #     if(distance[2][0]<15 and distance[2][0]>2):
    #         # Rolled away!
    #         self.set_next_state_callback(nav_smachine.refind_sample)
    #         self.target = Targets.sample
    #     else:
    #         # Got it!
    #         self.set_next_state_callback(nav_smachine.find_lander)
    #         self.target = Targets.lander
        
    # def on_find_lander(self):
    #     '''
    #     A sample has been collected, now returning to lander.
    #     '''
        
    #     self.target = Targets.lander
        
    def on_hidden_sample(self):
        pass
    
    def on_find_sample(self):
        pass

    def on_find_rock(self):
        pass

    def on_refind_rock(self):
        pass
    
    def on_finish(self):
        pass

    # Functions run on state entry:
    def on_enter_initialising(self):
        print('Initialising navigation state machine...')
        print()
        
        print('Navigation state machine READY!')
        print()
    
    def on_enter_find(self):
        nav_smachine = self.nav_internal_data.nav_smachine
        actions_q = self.nav_internal_data.actions_q
        bearings_q = self.nav_internal_data.bearings_q
        distances_q = self.nav_internal_data.distances_q
        vis_get_bearings = self.nav_internal_data.vis_get_bearings
        vis_get_distances = self.nav_internal_data.vis_get_distances
        
        #print('Entered find state')
        #print()
        
        # asdf = 0
        # while(asdf < 3):
        #     print('Forward')
        #     actions_q.put( ((Actions.m_forward_l,), (Actions.m_forward_r,)) )
        #     time.sleep(1)
        #     print('Stop')
        #     actions_q.put( ((Actions.m_halt,),) )
        #     time.sleep(0.5)
        #     print('Backwards')
        #     actions_q.put( ((Actions.m_back_l,), (Actions.m_back_r,)) )
        #     time.sleep(1)
        #     print('Stop')
        #     actions_q.put( ((Actions.m_halt,),) )
        #     time.sleep(0.5)
        #     print('Pivot left')
        #     actions_q.put( ((Actions.pivot_l,),) )
        #     time.sleep(1)
        #     print('Pivot right')
        #     actions_q.put( ((Actions.pivot_r,),) )
        #     time.sleep(1)
        #     print('Stop')
        #     actions_q.put( ((Actions.m_halt,),) )
        #     time.sleep(0.5)
            
        #     asdf += 1
        
        # Make sure claw is not in the way (i.e. lifted):
        # actions_q.put( ((Actions.claw_up,),) )
        
        target = finding_target(self.target, vis_get_bearings, vis_get_distances, actions_q, bearings_q, distances_q)
        #print('target', target)
        #print()
        if target is None:
            #print('loop back to find state')
            #print()
            self.set_next_state_callback(nav_smachine.cont_find)
        else:
            print('find to approach state')
            print()
            self.target = target
            nav_process = self.nav_internal_data.nav_process
            actions_q = self.nav_internal_data.actions_q
            self.set_next_state_callback(nav_smachine.approach_target)
        
        # #print('Exited find state')
        # #print()
    
    def on_enter_approach(self):
        nav_smachine = self.nav_internal_data.nav_smachine
        actions_q = self.nav_internal_data.actions_q
        vis_get_bearings = self.nav_internal_data.vis_get_bearings
        vis_get_distances = self.nav_internal_data.vis_get_distances
        
        nx_st_cb = approaching_target(self.target, vis_get_bearings, vis_get_distances, actions_q)
        if nx_st_cb is None:
            self.set_next_state_callback(nav_smachine.cont_approach)
        else:    
            self.set_next_state_callback(nx_st_cb)
    
    def on_enter_done(self):
        '''
        Clean up after navigation state machine.
        '''
        print('Closing down navigation state machine...')
        print()

    # Functions run on state exit:
    def on_exit_initialising(self):
        print('Navigation state machine RUNNING!')
        print()
    
    def on_exit_approach(self):
        pass
    
    def on_exit_done(self):
        print('Navigation state machine CLOSED!')
        print()
