from statemachine import StateMachine, State

class NavSMachine(StateMachine):
    off = State('Uninitialised', initial=True)
    initialising = State('Initialising')
    find_s = State('Find Sample', identifier='finds')
    find_l = State('Find Lander', identifier='findl')
    find_r = State('Find Rock', identifier='findr')
    collect = State('Collect sample')
    uncover = State('Uncover rock')
    deposit = State('Deposit sample')
    done = State('Done')

    # State transistions:
    init = off.to(initialising)
    start = initialising.to(find_s)
    obtain_sample = find_s.to(collect)
    find_lander = collect.to(find_l)
    flip_rock = find_r.to(uncover)
    hidden_sample = uncover.to(find_s)
    find_sample = deposit.to(find_s)
    refind_sample = collect.to(find_s)
    board_lander = approach.to(deposit)
    find_rock = deposit.to(find_r)
    refind_rock = uncover.to(find_r)
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
    
    def on_obtain_sample(self):
        self.func_impls.on_obtain_sample()

    def on_find_lander(self):
        self.func_impls.on_find_lander()

    def on_flip_rock(self):
        self.func_impls.on_flip_rock()

    def on_hidden_sample(self):
        self.func_impls.on_hidden_sample()
    
    def on_find_sample(self):
        self.func_impls.on_find_sample()

    def on_refind_sample(self):
        self.func_impls.on_refind_sample()
        
    def on_board_lander(self):
        self.func_impls.on_board_lander()

    def on_find_rock(self):
        self.func_impls.on_find_rock()
        
    def on_refind_rock(self):
        self.func_impls.on_refind_rock()

    def on_finish(self):
        self.func_impls.on_finish

    # Functions run on state entry:
    def on_enter_initialising(self):
        self.func_impls.on_enter_initialising()
    
    def on_enter_find_s(self):
        self.func_impls.on_enter_find_s()
    
    def on_enter_find_r(self):
        self.func_impls.on_enter_find_r()
    
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
