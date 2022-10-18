from mobility.mobility_enums import *
import mobility.mobility_impl as impl
from mobility.mobility_helpers import pivot_left    

def init():
    impl.init_impl()

def start():
    impl.start_impl()

def close():
    impl.close_impl()

def act_on(decision):
    impl.act_on_impl(decision)

def collect_sample():
    impl.collect_sample()