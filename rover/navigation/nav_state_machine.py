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
    cont_find = find.to(find)
    approach_target = find.to(approach)
    refind_target = approach.to(find) # Lost sight of target!
    cont_approach = approach.to(approach)
    obtain_sample = approach.to(collect)
    find_lander = collect.to(find)
    refind_sample = collect.to(find)
    flip_rock = approach.to(uncover)
    cont_flip_rock = uncover.to(uncover)
    find_sample = uncover.to(find)
    board_lander = approach.to(deposit)
    cont_board_lander = deposit.to(deposit)
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
        self.func_impls.on_approach_target()

    def on_obtain_sample(self):
        self.func_impls.on_obtain_sample()

    def on_find_lander(self):
        self.func_impls.on_find_lander()

    def on_flip_rock(self):
        self.func_impls.on_flip_rock()

    def on_find_sample(self):
        self.func_impls.on_find_sample()

    def on_board_lander(self):
        self.func_impls.on_board_lander()

    def on_find_target(self):
        self.func_impls.on_find_target()

    def on_finish(self):
        self.func_impls.on_finish

    # Functions run on state entry:
    def on_enter_initialising(self):
        self.func_impls.on_enter_initialising()
        
    def on_enter_find(self):
        self.func_impls.on_enter_find()
    
    def on_enter_approach(self):
        self.func_impls.on_enter_approach()
    
    def on_enter_collect(self):
        self.func_impls.on_enter_collect()
    
    def on_enter_done(self):
        '''
        Clean up after navigation state machine.
        '''
        self.func_impls.on_enter_done()

    # Function run on state exit:
    def on_exit_initialising(self):
        self.func_impls.on_exit_initialising()
    
    def on_exit_done(self):
        self.func_impls.on_exit_done()
