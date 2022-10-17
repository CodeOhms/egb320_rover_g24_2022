import navigation.navigation_impl as impl 

decisions_q = None
nav_smachine = None

def init(vis_to_nav_callbacks):
    global decisions_q
    global nav_smachine

    decisions_q, nav_smachine = impl.init_impl(vis_to_nav_callbacks)

def start():
    impl.start_impl()

def close():
    impl.close_impl()

def get_decision():
    return impl.get_decision_impl()