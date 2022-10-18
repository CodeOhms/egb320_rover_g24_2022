from mobility.mobility_sync.mobility_sync_impl import *

def init_impl():
    init_sync_impl()

def start_impl():
    start_sync_impl()

def close_impl():
    close_sync_impl()

def act_on_impl(decision):
    act_on_sync_impl(decision)

def collect_sample_impl():
    pass
    # collect_sample_sync_impl()
