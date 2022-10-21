from mobility.mobility_enums import *
import mobility.mobility_impl as impl
from mobility.mobility_helpers import pivot_left    

mobility_q = None

def init():
    global mobility_q
    mobility_q = impl.init_impl()

def start():
    impl.start_impl()

def close():
    impl.close_impl()

def get_mobility_queue():
    return mobility_q

# def act_on(actions):
#     impl.act_on_impl(actions)

# def collect_sample():
#     impl.collect_sample()