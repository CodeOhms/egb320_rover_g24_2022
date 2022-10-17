<<<<<<< HEAD
import numpy as np
import time
from time import sleep
=======
from queue import SimpleQueue
>>>>>>> main
from navigation.nav_state_machine import NavSMachine

decisions_q = None
nav_smachine_impl = None
nav_smachine = None
vis_get_bearings = None
vis_get_distances = None
retrieved_samples = 0


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
<<<<<<< HEAD
    
=======

	decisions_q = SimpleQueue()
>>>>>>> main
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
	cb = nav_smachine_impl.get_next_state_callback()
	cb()
    
    return decision

def create_potential_field(goal):
	bearings = vis_get_bearings()
        distance = vis_get_distances()
        compiled_GD = []
        if len(bearings[goal])==1:
	        GD = [[]]
        elif len(bearings[goal])==2:
	        GD = [[],[]]
        elif len(bearings[goal])==3:
	        GD = [[],[],[]]

        for x in range(0,len(bearings[goal])):
		for i in range(-31,32):
		        from_peak = abs(bearings[goal][x]-i)
		        peak = 283-distance[goal][x]
		        GD_value = peak-(peak*from_peak/31)
                	if GD_value<0:
                    		GD_value = 0
		        GD[x] = GD[x] + [GD_value]
			
        for j in range(0,63):
		combined_GD_value = 0
            	for y in range(0,len(bearings[goal])):
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
				decision_tool = peak-203
                    		if (descision_tool/from_peak)>4:
					OM_value = peak-(peak*from_peak/100)
				else:
					OM_value = 0
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
			PF_value = compiled_GD[i]-compiled_OM[i]
			compiled_PF = compiled_PF + [PF_value]
	return compiled_PF

def navigate_PF(PF):
	max = max(PF)
	position_of_max = PF.index(max)
	bearing = position_of_max - 31
	if bearing<0:
		movement = (['left_f', 40*(1.0-0.8*abs(bearing)/40)], ['right_f', 40])
	elif bearing>0:
		movement = (['left_f', 40], ['right_f', 40*(1.0-0.8*abs(bearing)/40)])
	else:
		movement = (['left_f', 40], ['right_f', 40])
	return bearing

# State machine functions implementations:
class NavSMachine_impl:
	self.nxt_st_cb = None

	# Functions unrelated to state machine library:
    def close(self):
        pass

	def set_next_state_callback(self, next_state_callback):
		self.nxt_st_cb = next_state_callback

	def get_next_state_callback(self):
		return self.nxt_st_cb

    # Functions run on transistions:
    def on_start(self):
        print('Starting navigation state machine...')
                   
    def on_approach_target(self):
        pass

    def on_obtain_sample(self):
        servo = 6.75
		movement = (['left_f', 0], ['right_f', 0])
		sleep(0.8)
		distance = vis_get_distances
		movement = (['left_f', 30], ['right_f', 30])
		sleep(0.2*distance[2][0])
		servo = 9
		movement = (['left_f', 0], ['right_f', 0])
		sleep(0.5)
		distance = vis_get_distances
		if(distance[2][0]<15&&distance[2][0]>2):
			nav_smachine.refind_sample()
		else:
			nav_smachine.find_lander()
		
    def on_find_lander(self):
        bearings = vis_get_bearings()
		distance = vis_get_distances()
		while bearings[5][0] == None:
			movement = (['left_b', 30], ['right_f', 30])
			bearings = vis_get_bearings()
		if bearings[5][0] != None:
			movement = (['left_b', 0], ['right_f', 0])
			while (nav_smachine.is_findl==True):
				if distance[5][0] != None:
					PF = create_potential_field(5)
					bearing = navigate_PF(PF)
					if max(PF)>280:
						if bearing<4 && bearing>-4:
						movement = (['left_f', 30], ['right_f', 30])
				else:
					nav_smachine.board_lander()

    def on_flip_rock(self):
        servo = 6.75
		movement = (['left_f', 0], ['right_f', 0])
		sleep(0.8)
		distance = vis_get_distances()
		movement = (['left_f', 30], ['right_f', 30])
		sleep(0.2*distance[4][0])
		movement = (['left_f', 0], ['right_f', 0])
		sleep(0.5)
		servo = 9
		distance = vis_get_distances()
		if(distance[2][0]!=None):
			nav_smachine.hidden_sample()
		else:
			nav_smachine.refind_rock()
		
		def on_hidden_sample(self):
			pass
		
		def on_find_sample(self):
			pass

		def on_refind_sample(self):
			pass
			
		def on_board_lander(self):
			while(distance[5][0]==None):
				movement = (['left_f', 30], ['right_f', 30])
				distance = vis_get_distances()
				movement = (['left_f', 0], ['right_f', 0])
				sleep(0.5)
				servo = 6.75
				sleep(0.5)
				movement = (['left_b', 20], ['right_b', 20])
				sleep(0.5)
				movement = (['left_b', 0], ['right_b', 0])
				retrieved_samples = retrieved_samples+1
				if retrieved_samples<2:
					nav_smachine.find_sample()
				else:
					nav_smachine.find_rock()

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
    
    def on_enter_find_s(self):
        servo = 9
    	bearings = vis_get_bearings
		while bearings[2][0] == None:
			movement = (['left_b', 30], ['right_f', 30])
			bearings = vis_get_bearings
		if bearings[2][0] != None:
					movement = (['left_b', 0], ['right_f', 0])
			while (nav_smachine.is_finds==True):
				PF = create_potential_field(2)
				bearing = navigate_PF(PF)
				if max(PF)>276:
					if bearing<4 && bearing>-4:
						nav_smachine.obtain_sample()
    
    def on_enter_find_r(self):
    	servo = 9
    	bearings = vis_get_bearings()
   	while bearings[4][0] == None:
		movement = (['left_b', 30], ['right_f', 30])
		bearings = vis_get_bearings()
		if bearings[4][0] != None:
			movement = (['left_b', 0], ['right_f', 0])
			while (nav_smachine.is_findr==True):
				PF = create_potential_field(4)
				bearing = navigate_PF(PF)
				if max(PF)>276:
					if bearing<4 && bearing>-4:
						nav_smachine.flip_rock()
    
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
