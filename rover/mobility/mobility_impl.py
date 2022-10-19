# from mobility.mobility_sync.mobility_sync_impl import *
from mobility.mobility_parallel.mobility_parallel_impl import *


def init_impl():
    return init_parallel_impl()

def start_impl():
    start_parallel_impl()

def close_impl():
    close_parallel_impl()

def act_on_impl(decision):
    act_on_parallel_impl(decision)
