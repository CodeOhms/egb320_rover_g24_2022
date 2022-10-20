from vision import vision as vis
from mobility import mobility as mob
import navigation.navigation_impl as impl 

actions_q = None
nav_smachine = None

def init():
    '''
    NOTE: both the mobility system must be initialised first!
    '''
    
    global actions_q
    global nav_smachine

    actions_q = mob.get_mobility_queue()
    vis_to_nav_callbacks = (vis.get_bearings, vis.get_distances)
    nav_smachine = impl.init_impl(vis_to_nav_callbacks, actions_q)

def start():
    impl.start_impl()

def close():
    impl.close_impl()

def get_decision():
    return impl.get_decision_impl()