from glob import glob
from multiprocessing import Process
import numpy as np
import time
from time import sleep
from queue import SimpleQueue
from navigation.nav_state_machine import NavSMachine
from mobility import mobility as mob
from mobility.mobility_enums import *
from navigation.navigation_parallel.nav_helpers import *

loop = None
nav_process = None
decisions_q = None
nav_smachine_impl = None
nav_smachine = None
vis_get_bearings = None
vis_get_distances = None
retrieved_samples = 0
pf_max = 276

def nav_loop():
    global loop
    global nav_smachine
    global nav_smachine_impl
    
    # Start the state machine!
    print(nav_smachine.current_state)
    nav_smachine.start()
    print(nav_smachine.current_state)
    
    
    # while(loop):
    #     cb, cb_args = nav_smachine_impl.get_next_state_callback()
    #     if cb_args is not None:
    #         cb(cb_args)
    #     else:
    #         cb()
    
    print('guiguiguihjvyf')
        
def init_parallel_impl(vis_to_nav_callbacks):
    global nav_process
    global loop
    
    loop = True
    nav_process = Process(target=nav_loop)
    
    global decisions_q
    global nav_smachine_impl
    global nav_smachine
    global vis_get_bearings
    global vis_get_distances

    vis_get_bearings, vis_get_distances = vis_to_nav_callbacks

    decisions_q = SimpleQueue()
    nav_smachine_impl = NavSMachine_impl()
    nav_smachine = NavSMachine(nav_smachine_impl)
    nav_smachine.init()
    
    return decisions_q, nav_smachine

def start_parallel_impl():
    global nav_process
    nav_process.start()

def close_parallel_impl():
    global loop
    global nav_process
    
    loop = False
    nav_process.join()
    
    global nav_smachine
    nav_smachine.close()

def get_decision_parallel_impl():
    decision = None
    try:
        decision = decisions_q.get()
    except:
        pass
    return decision


# State machine functions implementations:
class NavSMachine_impl(object):
    def __init__(self):
        self.nxt_st_cb = (None, None) # 1st index is the callback, 2nd are the args
        self.target = Targets.sample

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
        print('Forward')
        mob.act_on( ((Actions.m_forward_l,), (Actions.m_forward_r,)) )
        time.sleep(0.2)
        print('Stop')
        mob.act_on( ((Actions.m_halt,),) )
        time.sleep(0.5)
        print('Backwards')
        mob.act_on( ((Actions.m_back_l,), (Actions.m_back_r,)) )
        time.sleep(0.2)
        print('Stop')
        mob.act_on( ((Actions.m_halt,),) )
        time.sleep(0.5)
        print('Pivot left')
        mob.act_on( ((Actions.pivot_l,),) )
        time.sleep(0.7)
        print('Pivot right')
        mob.act_on( ((Actions.pivot_r,),) )
        time.sleep(0.7)
        print('Stop')
        mob.act_on( ((Actions.m_halt,),) )
    # time.sleep(0.5)
        
        # Make sure claw is not in the way (i.e. lifted):
        # mob.act_on( (('claw_up'),) )
        
        # target = finding_target(self.target)
        # self.target = target
        # self.set_next_state_callback(nav_smachine.approach_target)
    
    # def on_enter_approach(self):
    #     decision, nx_st_cb = approaching_target(self.target)
        
    #     self.set_next_state_callback(nx_st_cb)
    
    def on_enter_done(self):
        '''
        Clean up after navigation state machine.
        '''
        print('Closing down navigation state machine...')
        print()

    # Function run on state exit:
    def on_exit_initialising(self):
        print('Navigation state machine RUNNING!')
        print()
    
    
    def on_exit_done(self):
        print('Navigation state machine CLOSED!')
        print()
