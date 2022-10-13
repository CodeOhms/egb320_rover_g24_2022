

def init_camera(camera):
# https://picamera.readthedocs.io/en/release-1.13/recipes1.html#capturing-consistent-images
    print("Camera warming up...")
    
    # Set ISO to the desired value
    camera.iso = 900
    # Wait for the automatic gain control to settle
    time.sleep(2)
    # Now fix the values
    camera.shutter_speed = camera.exposure_speed
    camera.exposure_mode = 'off'
    g = camera.awb_gains
    camera.awb_mode = 'off'
    camera.awb_gains = g

def init_video_stream(vid_stream, cam_res):
    # Vertical res must be multiple of 16, and horizontal a multiple of 32.
    vid_stream = VideoStream(usePiCamera=True, resolution=cam_res, rotation=180).start()
    init_camera(vid_stream.camera)
