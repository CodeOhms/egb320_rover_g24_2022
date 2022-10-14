from navigation.nav_state_machine import NavSMachine

nav_smachine_impl = None
nav_smachine = None

def init_sync_impl():
    global nav_smachine_impl
    global nav_smachine

    nav_smachine_impl = NavSMachine_impl()
    nav_smachine = NavSMachine(nav_smachine_impl)

    print(nav_smachine.current_state)
    nav_smachine.begin()
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
    pass

def get_decision_sync_impl():
    pass

# State machine functions implementations:
class NavSMachine_impl:
    # Functions run on transistions:
    def on_begin(self):
        print('Begin state machine!')
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
    def on_enter_approach(self):
        pass
    
    def on_enter_done(self):
        '''
        Clean up after navigation state machine.
        '''
        pass

    # Function run on state exit:
    def on_exit_approach(self):
        pass