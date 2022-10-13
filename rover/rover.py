import cv2 as cv
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
    # frame_ov = vis.get_overlay()
    cv.imshow('Frame', frame)
    # cv.imshow('Vision', frame_ov)

    key = cv.waitKey(1) & 0xFF
    #if the `q` key was pressed, break from the loop
    if key == ord("q"):
        ret = False

    return ret

if __name__ == "__main__":
    print('Starting robot application.')
    print()

    # Initialise:
    print('Initialising systems...')
    print()

    vis.init()
    # nav.init()

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
    cv.destroyAllWindows()

    print('Done!')
    print()
    