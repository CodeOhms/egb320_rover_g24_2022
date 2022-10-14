import navigation.navigation_impl as impl 

nav_smachine = None

def init():
    global nav_smachine
    nav_smachine = impl.init_impl()

def start():
    impl.start_impl()

def close():
    impl.close_impl()

# def write_data():
#     '''
#     The purpose of this function is to transfer calculated data from the
#     vision system code to a shared FIFO buffer. From this buffer, the
#     helper functions `get_frame()`, `get_bearings()` and `get_distances()` can be
#     used to read data from this shared buffer easily.
#     This makes it easier to implement parallel code with either:
#     multiprocessing, multithreading, or asynchronous threading.
#     '''

#     impl.write_data_impl()

def get_decision():
    impl.get_decision()