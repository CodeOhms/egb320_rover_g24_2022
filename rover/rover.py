# from gpio_interface import gpio_interface as io_pins
from vision import vision as vis
from navigation import navigation as nav
from gpio_interface import gpio_interface as io_pins
# from mobility import mobility as mob
import time

def rover_loop():
    ret = True

    # Get decisions from the navigation subsystem:
    # decision = nav.get_decision()

    print('Forward')
    io_pins.motor_forward_l()
    io_pins.motor_forward_r()
    time.sleep(0.2)
    print('Stop')
    io_pins.motor_halt()
    # mob.act_on((Actions.m_forward_l, Actions.m_forward_r))

    # Display information from the vision system:
    frame = vis.get_frame()
    frame_ovs = vis.get_overlays()
    
    if not vis.display_frame(frame) or not vis.display_overlays(frame_ovs):
        # Display window was closed! Shutdown application.
        ret = False
    
    # print('Bearings:')
    # print(vis.get_bearings())
    # print()
    # print('Distances:')
    # print(vis.get_distances())
    # print()
    # print()

    return ret

if __name__ == "__main__":
    print('Starting robot application.')
    print()

    # Initialise:
    print('Initialising systems...')
    print()

    io_pins.init()
    vis.init()
    # vis_to_nav_callbacks = (vis.get_bearings, vis.get_distances)
    # nav.init(vis_to_nav_callbacks)
    # mob.init()
    # Setup display windows:

    io_pins.start()
    vis.start(1200)
    # nav.start()
    # mob.start()

    while(True):
        if not rover_loop():
            break

    print('Closing robot application...')
    print()

    # Clean up:
    print('Cleaning up...')
    print()

    io_pins.close()
    vis.close()
    # nav.close()
    # mob.close()

    print('Done!')
    print()
    