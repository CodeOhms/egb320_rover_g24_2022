from vision import vision as vis
from mobility import mobility as mob
import navigation.navigation_impl as impl 

actions_q = None
nav_process = None

def init():
    '''
    NOTE: both the mobility system must be initialised first!
    '''
    
    global actions_q
    global nav_process

    actions_q = mob.get_mobility_queue()
    bearings_q = vis.get_bearings_queue()
    distances_q = vis.get_distances_queue()
    vis_to_nav_callbacks = (vis.get_bearings, vis.get_distances)
    # vis_to_nav_callbacks = (vis.get_bearings_, vis.get_distances_)
    nav_process = impl.init_impl(vis_to_nav_callbacks, actions_q, bearings_q, distances_q)

def start():
    global nav_process
    impl.start_impl(nav_process)

def close():
    global actions_q
    global nav_process
    
    impl.close_impl(nav_process, actions_q)

def get_decision():
    return impl.get_decision_impl()