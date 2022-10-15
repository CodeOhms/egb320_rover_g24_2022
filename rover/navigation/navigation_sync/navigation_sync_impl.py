from navigation.nav_state_machine import NavSMachine

nav_smachine_impl = None
nav_smachine = None

# DOCS: https://python-statemachine.readthedocs.io/en/latest/readme.html
def init_sync_impl():
    global nav_smachine_impl
    global nav_smachine

    nav_smachine_impl = NavSMachine_impl()
    nav_smachine = NavSMachine(nav_smachine_impl)

    # Example of how to use transistions (state to state):
    print(nav_smachine.current_state)
    nav_smachine.init()
    print(nav_smachine.current_state)
    nav_smachine.start()
    print(nav_smachine.current_state)
    nav_smachine.approach_target()
    print(nav_smachine.current_state)
    nav_smachine.obtain_sample()
    print(nav_smachine.current_state)
    nav_smachine.find_lander()
    print(nav_smachine.current_state)
    nav_smachine.approach_target()
    print(nav_smachine.current_state)
    nav_smachine.board_lander()
    print(nav_smachine.current_state)
    nav_smachine.find_target()
    print(nav_smachine.current_state)

    return nav_smachine

def start_sync_impl():
    pass

def close_sync_impl():
    # global nav_smachine
    pass

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