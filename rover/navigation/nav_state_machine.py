from statemachine import StateMachine, State

class NavSMachine(StateMachine):
    off = State('Uninitialised', initial=True)
    initialising = State('Initialising')
    find = State('Find')
    approach = State('Approach')
    collect = State('Collect sample')
    uncover = State('Uncover rock')
    deposit = State('Deposit sample')
    done = State('Done')

    # State transistions:
    init = off.to(initialising)
    start = initialising.to(find)
    approach_target = find.to(approach)
    obtain_sample = approach.to(collect)
    find_lander = collect.to(find)
    flip_rock = approach.to(uncover)
    find_sample = uncover.to(find)
    board_lander = approach.to(deposit)
    find_target = deposit.to(find)
    finish = find.to(done)

    def __init__(self, func_impls):
        self.func_impls = func_impls
        super().__init__()
    
    def close(self):
        '''
        Signal code called by the state machine to close
        and go to the machine's final state.
        '''
        self.func_impls.close()

    # Functions run on transistions:
    def on_start(self):
        self.func_impls.on_start()
    
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
        self.func_impls.on_enter_initialising()
    
    def on_enter_approach(self):
        pass
    
    def on_enter_done(self):
        '''
        Clean up after navigation state machine.
        '''
        self.func_impls.on_enter_done()

    # Function run on state exit:
    def on_exit_initialising(self):
        self.func_impls.on_exit_initialising()
    
    def on_exit_approach(self):
        pass
    
    def on_exit_done(self):
        self.func_impls.on_exit_done()