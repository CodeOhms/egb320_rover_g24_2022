import time
import cv2 as cv
from imutils.video import VideoStream
    
resolution = None

def init_video_stream(use_picam, cam_res):
    global resolution
    
    resolution = cam_res
    
    vs = None
    try:
        # Vertical res must be multiple of 16, and horizontal a multiple of 32.
        vs = VideoStream(usePiCamera=use_picam, resolution=cam_res, rotation=180)
    except:
        print('Pi camera not available. Looking for a web cam...')
        print()
        vs = VideoStream(usePiCamera=False, resolution=cam_res, rotation=180)
        ocv_vid = vs.stream.stream
    return vs

def camera_start(video_stream, iso):
# https://picamera.readthedocs.io/en/release-1.13/recipes1.html#capturing-consistent-images

    global resolution
    
    print("Camera warming up...")

    actual_res = None
    if type(video_stream.stream.stream) is cv.VideoCapture:
        # cam_res = video_stream.cam_res
        ocv_vid = video_stream.stream.stream
        iso = ocv_vid.set(cv.CAP_PROP_ISO_SPEED, iso)
        
        time.sleep(2)
        
        # Change values:
        aexp = 1 #V4L2_EXPOSURE_MANUAL
        ocv_vid.set(cv.CAP_PROP_FRAME_WIDTH, resolution[0])
        ocv_vid.set(cv.CAP_PROP_FRAME_HEIGHT, resolution[1])
        # ocv_vid.set(cv.CAP_PROP_FRAME_WIDTH, 80)
        # ocv_vid.set(cv.CAP_PROP_FRAME_HEIGHT, 60)
        ocv_vid.set(cv.CAP_PROP_AUTO_EXPOSURE, aexp)
        
        # Frame dimensions may have changed:
        f_w = ocv_vid.get(cv.CAP_PROP_FRAME_WIDTH)
        f_h = ocv_vid.get(cv.CAP_PROP_FRAME_HEIGHT)
        actual_res = (int(f_h), int(f_w))
        
        video_stream.start()
    else:
        video_stream.start()
        camera = video_stream.stream.camera

        # camera.awb_mode = 'off'
        # camera.awb_gains = (1.4, 1.5)

        # Set ISO to the desired value
        camera.iso = iso

        # Wait for the automatic gain control to settle
        time.sleep(2)
        # Now fix the values
        camera.shutter_speed = camera.exposure_speed
        camera.exposure_mode = 'off'
        g = camera.awb_gains
        camera.awb_mode = 'off'
        camera.awb_gains = g
        actual_res = camera.resolution

    return video_stream, actual_res

def get_frame(video_stream):
    frame = video_stream.read()
    return frame