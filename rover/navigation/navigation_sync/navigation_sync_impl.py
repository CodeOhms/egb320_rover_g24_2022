from queue import SimpleQueue
from navigation.nav_state_machine import NavSMachine

decisions_q = None
nav_smachine_impl = None
nav_smachine = None
vis_get_bearings = None
vis_get_distances = None

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
	cb = nav_smachine_impl.get_next_state_callback()
	cb()
    
    return decision

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
        print()
    
    def on_approach_target(self):
        pass

    def on_obtain_sample(self):
        pass

    def on_find_lander(self):
        pass

    def on_flip_rock(self):
        pass

    def on_find_sample(self):
        pass

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