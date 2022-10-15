from navigation.navigation_sync.navigation_sync_impl import *

def init_impl(vis_to_nav_callbacks):
    return init_sync_impl(vis_to_nav_callbacks)

def start_impl():
    start_sync_impl()

def close_impl():
    close_sync_impl()

def get_decision_impl():
    return get_decision_sync_impl()