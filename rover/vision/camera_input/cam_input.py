import time
from imutils.video import VideoStream
    
def init_video_stream(cam_res):
    # Vertical res must be multiple of 16, and horizontal a multiple of 32.
    return VideoStream(usePiCamera=True, resolution=cam_res, rotation=180)

def camera_start(video_stream, iso):
# https://picamera.readthedocs.io/en/release-1.13/recipes1.html#capturing-consistent-images
    
    print("Camera warming up...")

    video_stream.start()
    camera = video_stream.stream.camera

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

    return video_stream

def get_frame(video_stream):
    frame = video_stream.read()
    return frame