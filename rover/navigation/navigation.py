import navigation.navigation_impl as impl 

nav_smachine = None

def init(vis_to_nav_callbacks):
    global nav_smachine
    nav_smachine = impl.init_impl(vis_to_nav_callbacks)

def start():
    impl.start_impl()

def close():
    impl.close_impl()

def get_decision():
    return impl.get_decision_impl()