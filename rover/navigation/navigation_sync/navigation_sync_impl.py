import numpy as np
import time
from time import sleep
from queue import SimpleQueue
from enum import Enum
from navigation.nav_state_machine import NavSMachine
import mobility.mobility_helpers as mobh

decisions_q = None
nav_smachine_impl = None
nav_smachine = None
vis_get_bearings = None
vis_get_distances = None
retrieved_samples = 0
pf_max = 276


# DOCS: https://python-statemachine.readthedocs.io/en/latest/readme.html
def init_sync_impl(vis_to_nav_callbacks):
    global decisions_q
    global nav_smachine_impl
    global nav_smachine
    global vis_get_bearings
    global vis_get_distances

    vis_get_bearings, vis_get_distances = vis_to_nav_callbacks
    # Example, but it shouldn't be used in this function:
    # print(vis_get_bearings())

    decisions_q = SimpleQueue()
    nav_smachine_impl = NavSMachine_impl()
    nav_smachine = NavSMachine(nav_smachine_impl)
    nav_smachine.init()
    
    # Example of how to use transistions (state to state):
    # print(nav_smachine.current_state)
    # 
    # print(nav_smachine.current_state)
    # nav_smachine.start()
    # print(nav_smachine.current_state)
    # nav_smachine.approach_target()
    # print(nav_smachine.current_state)
    # nav_smachine.obtain_sample()
    # print(nav_smachine.current_state)
    # nav_smachine.find_lander()
    # print(nav_smachine.current_state)
    # nav_smachine.approach_target()
    # print(nav_smachine.current_state)
    # nav_smachine.board_lander()
    # print(nav_smachine.current_state)
    # nav_smachine.find_target()
    # print(nav_smachine.current_state)

    return decisions_q, nav_smachine

def start_sync_impl():
    global nav_smachine
    nav_smachine.start()

def close_sync_impl():
    global nav_smachine
    nav_smachine.close()

def get_decision_sync_impl():
    '''
    
    RETURNS: a string representing the decision of the navigation system.
    '''

    decision = decisions_q.get()

    # Below only to be done in the synchronous implementation!
    cb, cb_args = nav_smachine_impl.get_next_state_callback()
    # Special case for obtain sample:
    if cb == nav_smachine.on_obtain_sample:
        obtain_s_gen = cb()
        next(obtain_s_gen)
    elif cb_args is None:
        cb()
    else:
        cb(cb_args)
    
    return decision

# def create_potential_field(goal):
#     bearings = vis_get_bearings()
#     distance = vis_get_distances()
#     compiled_GD = []
#     if len(bearings[goal])==1:
#         GD = [[]]
#     elif len(bearings[goal])==2:
#         GD = [[],[]]
#     elif len(bearings[goal])==3:
#         GD = [[],[],[]]

#     for x in range(0,len(bearings[goal])):
#         for i in range(-31,32):
#             from_peak = abs(bearings[goal][x]-i)
#             peak = 283-distance[goal][x]
#             GD_value = peak-(peak*from_peak/31)
#                 if GD_value<0:
#                         GD_value = 0
#             GD[x] = GD[x] + [GD_value]
        
#     for j in range(0,63):
#         combined_GD_value = 0
#             for y in range(0,len(bearings[goal])):
#                 combined_GD_value = combinded_GD_value+GD[y][j]
#         compiled_GD = compiled_GD + [combined_GD_value]
    
#     compiled_OM = []
#     if len(bearings[3])==1:
#         OM = [[]]
#     elif len(bearings[3])==2:
#         OM = [[],[]]
#     elif len(bearings[3])==3:
#         OM = [[],[],[]]

#     for x in range(0,len(bearings[3])):
#         for i in range(-31,32):
#         from_peak = abs(bearings[3][x]-i)
#             peak = 283-distance[3][x]
#             if peak>203:
#                         if from_peak==0:
#                             OM_value = peak
#             decision_tool = peak-203
#                         if (descision_tool/from_peak)>4:
#                 OM_value = peak-(peak*from_peak/100)
#             else:
#                 OM_value = 0
#                 else:
#                     OM_value = 0
#             OM[x] = OM[x] + [OM_value]
        
#     for j in range(0,63):
#         combined_OM_value = 0
#             for y in range(0,len(bearings[3])):
#                 combined_OM_value = combinded_OM_value+OM[y][j]
#             compiled_OM = compiled_OM + [combined_OM_value]
    
#     compiled_PF = []
#     for i in range(0,63):
#         PF_value = compiled_GD[i]-compiled_OM[i]
#         compiled_PF = compiled_PF + [PF_value]
#     return compiled_PF

# def navigate_PF(PF):
#     max = max(PF)
#     position_of_max = PF.index(max)
#     bearing = position_of_max - 31
#     if bearing<0:
#         movement = (['left_f', 40*(1.0-0.8*abs(bearing)/40)], ['right_f', 40])
#     elif bearing>0:
#         movement = (['left_f', 40], ['right_f', 40*(1.0-0.8*abs(bearing)/40)])
#     else:
#         movement = (['left_f', 40], ['right_f', 40])
#     return bearing

class Targets(Enum):
    sample = 2
    rock = 4
    lander = 5

def finding_target(target):
    '''
    Find either targets by priorty, or the target specified.

    @param target. If the parameter is
    'sample' the function will attempt to find a sample or a rock,
    but will prioritise finding a rock.
    If set to 'lander' the function will attempt to find the
    lander.
    '''

    decision = ()

    bearings = vis_get_bearings()
    distances = vis_get_distances()

    target_i = None # Target indicies in bearings and distances.
    if target == Targets.sample:
        target_i = [2]
    elif target == Targets.rock:
        target_i = [4]
    elif target == Targets.lander:
        target_i = [5]
    else:
        raise("Expected either Targets.sample or Targets.lander for the `target` argument!")

    # Pivot to find a target:
    targ_bear = None
    targ_dist = None
    for t_i in target_i:
        targ_bear = bearings[t_i]
        targ_dist = distances[t_i]
        if len(targ_bear) > 0 and len(targ_dist) > 0:
            decision = (('halt')) # Found it! Stop!
            found_targ = Targets[t_i]
            break
        else:
            decision = (('pivot_l')) # Keep looking...

    # return targ_bear, targ_dist
    return decision, found_targ

def approaching_target(target):
    decision = ()
    nx_st_cb = None
    
    bearings = vis_get_bearings()
    distances = vis_get_distances()
    
    target_i = None # Target indicies in bearings and distances.
    if target == Targets.sample:
        target_i = [2]
    elif target == Targets.rock:
        target_i = [4]
    elif target == Targets.lander:
        target_i = [5]
    else:
        raise("Expected either Targets.sample or Targets.lander for the `target` argument!")
    
    targ_bear = None
    targ_dist = None
    for t_i in target_i:
        targ_bear = bearings[t_i]
        targ_dist = distances[t_i]
        if len(targ_bear) < 1 and len(targ_dist) < 1:
            decision = (('halt')) # Lost it! Stop!
            print('Target ' + str(target) + ' lost!')
            break
        else:
            # Approaching...
            PF = create_potential_field(2)
            steering = navigate_PF(PF)
            
            # Is it close enough to interact with?:
            if max(PF) > pf_max:
                # Make sure target aligned decently:
                if steering < 4 && steering > -4:
                    nx_st_cb = (nav_smachine.obtain_sample, None)
            else:
                nx_st_cb = (nav_smachine.cont_approach, None)
                   
        return decision, nx_st_cb
    

        # servo = 9
    #     bearings = vis_get_bearings
    #     while bearings[2][0] == None:
    #         movement = (['left_b', 30], ['right_f', 30])
    #         bearings = vis_get_bearings
    #     if bearings[2][0] != None:
    #                 movement = (['left_b', 0], ['right_f', 0])
    #         while (nav_smachine.is_finds==True):
    #             PF = create_potential_field(2)
    #             bearing = navigate_PF(PF)
    #             if max(PF)>276:
    #                 if bearing<4 && bearing>-4:
    #                     # nav_smachine.obtain_sample()
    #                     self.set_next_state_callback(nav_smachine.obtain_sample)



# State machine functions implementations:
class NavSMachine_impl:
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

    def on_obtain_sample(self):
        # Move claw down, and stop:
        decision = (('stop'), ('claw_down'))
        # Need to provide decision and stop here first:
        yield decision
        
        # Now we can continue:
        distance = vis_get_distances()
        
        # Move forward a bit:
        decision = (['left_f', 30], ['right_f', 30])
        yield decision
        sleep(0.2*distance[2][0]) # Allow to move forward a bit.
        
        # Lift sample, hopefully:
        decision = (('claw_lift'), ('stop'))
        yield decision
        sleep(0.5) # Allow ball to roll, if fumbled.
        distance = vis_get_distances()
        # Did the ball roll far?:
        if(distance[2][0]<15 and distance[2][0]>2):
            # Rolled away!
            self.set_next_state_callback(nav_smachine.refind_sample)
            self.target = Targets.sample
        else:
            # Got it!
            self.set_next_state_callback(nav_smachine.find_lander)
            self.target = Targets.lander
        
    # def on_obtain_sample(self):
    #     servo = 6.75
    #     movement = (['left_f', 0], ['right_f', 0])
    #     sleep(0.8)
    #     distance = vis_get_distances
    #     movement = (['left_f', 30], ['right_f', 30])
    #     sleep(0.2*distance[2][0])
    #     servo = 9
    #     movement = (['left_f', 0], ['right_f', 0])
    #     sleep(0.5)
    #     distance = vis_get_distances
    #     if(distance[2][0]<15&&distance[2][0]>2):
    #         # nav_smachine.refind_sample()
    #         self.set_next_state_callback(nav_smachine.refind_sample)
    #     else:
    #         # nav_smachine.find_lander()
    #         self.set_next_state_callback(nav_smachine.find_lander)
        
    def on_find_lander(self):
        '''
        A sample has been collected, now returning to lander.
        '''
        
        self.target = Targets.lander
          
    # def on_find_lander(self):
    #     bearings = vis_get_bearings()
    # 	distance = vis_get_distances()
    # 	while bearings[5][0] == None:
    # 		movement = (['left_b', 30], ['right_f', 30])
    # 		bearings = vis_get_bearings()
    # 	if bearings[5][0] != None:
    # 		movement = (['left_b', 0], ['right_f', 0])
    # 		while (nav_smachine.is_findl==True):
    # 			if distance[5][0] != None:
    # 				PF = create_potential_field(5)
    # 				bearing = navigate_PF(PF)
    # 				if max(PF)>280:
    # 					if bearing<4 && bearing>-4:
    # 					movement = (['left_f', 30], ['right_f', 30])
    # 			else:
    # 				# nav_smachine.board_lander()
    # 				self.set_next_state_callback(nav_smachine.board_lander)

    # def on_flip_rock(self):
    #     servo = 6.75
    #     movement = (['left_f', 0], ['right_f', 0])
    #     sleep(0.8)
    #     distance = vis_get_distances()
    #     movement = (['left_f', 30], ['right_f', 30])
    #     sleep(0.2*distance[4][0])
    #     movement = (['left_f', 0], ['right_f', 0])
    #     sleep(0.5)
    #     servo = 9
    #     distance = vis_get_distances()
    #     if(distance[2][0]!=None):
    #         # nav_smachine.hidden_sample()
    #         self.set_next_state_callback(nav_smachine.hidden_sample)
    #     else:
    #         # nav_smachine.refind_rock()
    #         self.set_next_state_callback(nav_smachine.refind_rock)
        
        def on_hidden_sample(self):
            pass
        
        def on_find_sample(self):
            pass
            
        # def on_board_lander(self):
        #     while(distance[5][0]==None):
        #         movement = (['left_f', 30], ['right_f', 30])
        #         distance = vis_get_distances()
        #         movement = (['left_f', 0], ['right_f', 0])
        #         sleep(0.5)
        #         servo = 6.75
        #         sleep(0.5)
        #         movement = (['left_b', 20], ['right_b', 20])
        #         sleep(0.5)
        #         movement = (['left_b', 0], ['right_b', 0])
        #         retrieved_samples += 1
        #         if retrieved_samples<2:
        #             # nav_smachine.find_sample()
        #             self.set_next_state_callback(nav_smachine.find_sample)
        #         else:
        #             # nav_smachine.find_rock()
        #             self.set_next_state_callback(nav_smachine.find_rock)

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
        decision, target = finding_target(self.target)
        self.target = target
            
        # Make sure claw is not in the way (i.e. lifted):
        decision = (('claw_up'), decision)
        
        # Target not found! Need to allow main loop to continue for vision system,
        # and next loop start finding again!
        if len(decision) == 0:
            self.set_next_state_callback(nav_smachine.cont_find)
        else:
            self.set_next_state_callback(nav_smachine.approach_target)
    
    def on_enter_approach(self):
        decision, nx_st_cb = approaching_target(self.target)
        
        self.set_next_state_callback(nx_st_cb)
    
    # def on_enter_find_s(self):
    #     servo = 9
    #     bearings = vis_get_bearings
    #     while bearings[2][0] == None:
    #         movement = (['left_b', 30], ['right_f', 30])
    #         bearings = vis_get_bearings
    #     if bearings[2][0] != None:
    #                 movement = (['left_b', 0], ['right_f', 0])
    #         while (nav_smachine.is_finds==True):
    #             PF = create_potential_field(2)
    #             bearing = navigate_PF(PF)
    #             if max(PF)>276:
    #                 if bearing<4 && bearing>-4:
    #                     # nav_smachine.obtain_sample()
    #                     self.set_next_state_callback(nav_smachine.obtain_sample)
    
    # def on_enter_find_r(self):
    #     servo = 9
    #     bearings = vis_get_bearings()
    #    while bearings[4][0] == None:
    #     movement = (['left_b', 30], ['right_f', 30])
    #     bearings = vis_get_bearings()
    #     if bearings[4][0] != None:
    #         movement = (['left_b', 0], ['right_f', 0])
    #         while (nav_smachine.is_findr==True):
    #             PF = create_potential_field(4)
    #             bearing = navigate_PF(PF)
    #             if max(PF)>276:
    #                 if bearing<4 && bearing>-4:
    #                     # nav_smachine.flip_rock()
    #                     self.set_next_state_callback(nav_smachine.flip_rock)
    
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
