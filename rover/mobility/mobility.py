import mobility.mobility_impl as impl


def init():
    impl.init_impl()

def start():
    impl.start_impl()

def close():
    impl.close_impl()

def act_on(decision):
    impl.act_on_impl(decision)