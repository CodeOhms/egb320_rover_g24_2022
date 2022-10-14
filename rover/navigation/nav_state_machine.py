from statemachine import StateMachine, State
# import copy

class NavSMachine(StateMachine):
    start = State('Start', initial=True)
    find = State('Find')
    approach = State('Approach')
    collect = State('Collect sample')
    uncover = State('Uncover rock')
    deposit = State('Deposit sample')
    done = State('Done')

    # State transistions:
    begin = start.to(find)
    approach_target = find.to(approach)
    obtain_sample = approach.to(collect)
    find_lander = collect.to(find)
    flip_rock = approach.to(uncover)
    find_sample = uncover.to(find)
    board_lander = approach.to(deposit)
    find_target = deposit.to(find)
    finish = find.to(done)

    def __init__(self, func_impls):
        # self.func_impls = copy.deepcopy(func_impls)
        self.func_impls = func_impls
        super().__init__()

    # Functions run on transistions:
    def on_begin(self):
        self.func_impls.on_begin()
    
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