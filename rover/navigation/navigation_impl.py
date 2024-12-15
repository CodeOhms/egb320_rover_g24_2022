from navigation.navigation_parallel.navigation_parallel_impl import *

def init_impl(vis_to_nav_callbacks, actions_q, bearings_q, distances_q):
    # return init_sync_impl(vis_to_nav_callbacks)
    return init_parallel_impl(vis_to_nav_callbacks, actions_q, bearings_q, distances_q)

def start_impl(nav_process):
    # start_sync_impl()
    start_parallel_impl(nav_process)

def close_impl(nav_process, actions_q):
    close_parallel_impl(nav_process, actions_q)
    # close_sync_impl()

def get_decision_impl():
    return get_decision_parallel_impl()
    # return get_decision_sync_impl()