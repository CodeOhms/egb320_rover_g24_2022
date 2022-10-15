import navigation.navigation_impl as impl 

nav_smachine = None

def init():
    global nav_smachine
    nav_smachine = impl.init_impl()

def start():
    impl.start_impl()

def close():
    impl.close_impl()

def get_decision():
    impl.get_decision()