from vision import vision as vis
# from navigation import navigation as nav

def rover_loop():
    ret = True

    # Get decisions from the navigation subsystem:
    # nav.write_data()
    # decision = nav.get_decision()

    # Act:

    # Display information from the vision system:
    frame = vis.get_frame()
    frame_ovs = vis.get_overlays()
    
    if not vis.display_frame(frame) or not vis.display_overlays(frame_ovs):
        # Display window was closed! Shutdown application.
        ret = False
    
    print('Bearings:')
    print(vis.get_bearings())
    print()
    print('Distances:')
    print(vis.get_distances())
    print()
    print()

    return ret

if __name__ == "__main__":
    print('Starting robot application.')
    print()

    # Initialise:
    print('Initialising systems...')
    print()

    vis.init()
    # nav.init()
    # Setup display windows:

    vis.start()

    while(True):
        if not rover_loop():
            break

    print('Closing robot application.')
    print()

    # Clean up:
    print('Cleaning up...')
    print()

    vis.close()
    # nav.close()

    print('Done!')
    print()
    