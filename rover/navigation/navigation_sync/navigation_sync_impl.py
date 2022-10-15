import numpy as np
import time
from time import sleep
from navigation.nav_state_machine import NavSMachine

nav_smachine_impl = None
nav_smachine = None
vis_get_bearings = None
vis_get_distances = None

# DOCS: https://python-statemachine.readthedocs.io/en/latest/readme.html
def init_sync_impl(vis_to_nav_callbacks):
    global nav_smachine_impl
    global nav_smachine
    global vis_get_bearings
    global vis_get_distances
    global movement

    vis_get_bearings, vis_get_distances = vis_to_nav_callbacks
    # Example, but it shouldn't be used in this function:
    # print(vis_get_bearings())
    
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

    return nav_smachine

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
    
    return 'decision'

# State machine functions implementations:
class NavSMachine_impl:
    def close(self):
        pass

    # Functions run on transistions:
    def on_start(self):
        print('Starting navigation state machine...')
        print()
        bearings = vis_get_bearings
        while bearings[2][0] != None:
            movement = (['left_f', 40], ['right_b', 40])
        if bearings[2][0] !=None:
            movement = (['left_f', 0], ['right_b', 0])
            nav_smachine.find_sample()
            
    
    def on_approach_target(self):
        pass

    def on_obtain_sample(self):
        pass

    def on_find_lander(self):
        pass

    def on_flip_rock(self):
        pass

    def on_find_sample(self):
        bearings = vis_get_bearings
        distance = vis_get_distances
        compiled_GD = []
        if len(bearings[2])==1:
	        GD = [[]]
        elif len(bearings[2])==2:
	        GD = [[],[]]
        elif len(bearings[2])==3:
	        GD = [[],[],[]]

        for x in range(0,len(bearings[2])):
	        for i in range(-31,32):
		        from_peak = abs(bearings[2][x]-i)
		        peak = 283-distance[2][x]
		        GD_value = peak-(peak*from_peak/31)
                if GD_value<0:
                    GD_value = 0
		        GD[x] = GD[x] + [GD_value]
        for j in range(0,63):
            combined_GD_value = 0
            for y in range(0,len(bearings[2])):
                combined_GD_value = combinded_GD_value+GD[y][j]
            compiled_GD = compiled_GD + [combined_GD_value]
        
        compiled_OM = []
        if len(bearings[3])==1:
	        OM = [[]]
        elif len(bearings[3])==2:
	        OM = [[],[]]
        elif len(bearings[3])==3:
	        OM = [[],[],[]]

        for x in range(0,len(bearings[3])):
	        for i in range(-31,32):
		        from_peak = abs(bearings[3][x]-i)
		        peak = 283-distance[3][x]
		        if peak>203:
                    if from_peak==0:
                        OM_value = peak
                    
                    decision_tool = peak - 203
                    if descision_tool/from_peak>4:
                        OM_value = peak-(peak*from_peak/100)
                else:
                    OM_value = 0
		        OM[x] = OM[x] + [OM_value]
        for j in range(0,63):
            combined_OM_value = 0
            for y in range(0,len(bearings[3])):
                combined_OM_value = combinded_OM_value+OM[y][j]
            compiled_OM = compiled_OM + [combined_OM_value]
	    
        compiled_PF = []
        for i in range(0,63):
            PF_value = compiled_OM[i]+compiled_GD[i]
            compiled_PF = compiled_PF + [PF_value]
            

    def on_board_lander(self):
        pass

    def on_find_target(self):
        pass

    def on_finish(self):
        pass

    # Functions run on state entry:
    def on_enter_initialising(self):
        print('Initialising navigation state machine...')
        print()
        
        print('Navigation state machine READY!')
        print()
    
    def on_enter_approach(self):
        pass
    
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
    
    def on_exit_approach(self):
        pass
    
    def on_exit_done(self):
        print('Navigation state machine CLOSED!')
        print()
