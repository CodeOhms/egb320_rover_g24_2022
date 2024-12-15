# from gpio_interface import gpio_interface as io_pins
from vision import vision as vis
from navigation import navigation as nav
from gpio_interface import gpio_interface as io_pins
from mobility import mobility as mob
from mobility.mobility_enums import *
import time

def rover_loop():
    ret = True

    # Get decisions from the navigation subsystem:
    # decision = nav.get_decision()

    # print('Forward')
    # mob.act_on( ((Actions.m_forward_l,), (Actions.m_forward_r,)) )
    # time.sleep(0.2)
    # print('Stop')
    # mob.act_on( ((Actions.m_halt,),) )
    # time.sleep(0.5)
    # print('Backwards')
    # mob.act_on( ((Actions.m_back_l,), (Actions.m_back_r,)) )
    # time.sleep(0.2)
    # print('Stop')
    # mob.act_on( ((Actions.m_halt,),) )
    # time.sleep(0.5)
    # print('Pivot left')
    # mob.act_on( ((Actions.pivot_l,),) )
    # time.sleep(0.7)
    # print('Pivot right')
    # mob.act_on( ((Actions.pivot_r,),) )
    # time.sleep(0.7)
    # print('Stop')
    # mob.act_on( ((Actions.m_halt,),) )
    # time.sleep(0.5)

    # Display information from the vision system:
    frame = vis.get_frame()
    frame_ovs = vis.get_overlays()
    
    if not vis.display_frame(frame) or not vis.display_overlays(frame_ovs):
        # Display window was closed! Shutdown application.
        ret = False

    return ret

if __name__ == "__main__":
    print('Starting robot application.')
    print()

    # Initialise:
    print('Initialising systems...')
    print()

    mob.init()
    vis.init()
    nav.init()
    # Setup display windows:

    mob.start()
    vis.start(1200)
    nav.start()

    while(True):
        if not rover_loop():
            break

    print('Closing robot application...')
    print()

    # Clean up:
    print('Cleaning up...')
    print()

    # io_pins.close()
    mob.close()
    vis.close()
    nav.close()

    print('Done!')
    print()
    