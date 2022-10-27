from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import NNVision as Vision
from time import sleep

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 15
rawCapture = PiRGBArray(camera, size=(640, 480))
sleep(1)
exp_shut = 15000
#while True:
    #diff = camera.exposure_speed - exp_shut
    #print(f"ces : {camera.exposure_speed}, diff : {diff}")
    #sleep(0.05)
    #if abs(diff) < 10000:
    #    camera.exposure_mode = 'off'
    #    diff = camera.exposure_speed - exp_shut
    #    if abs(diff) < 10000:
    #        break
    #    else:
    #        camera.exposure_mode = 'auto'
    
camera.exposure_mode = 'off'
camera.iso = 300 
camera.shutter_speed = 15000
awbg = camera.awb_gains  # get auto-white balance settings
camera.awb_mode = 'off'
#camera.awb_gains = (1.015625, 2.0625)
camera.awb_gains = (35/32, 267/128)
print(f"shutter_speed : {str(camera.shutter_speed)}, exposure_speed : {str(camera.exposure_speed)}, awbg : {str(awbg)}  ")

# allow the camera to warmup
time.sleep(3)

def read():
    awbg = camera.awb_gains
    
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        #print(f"shutter_speed : {str(camera.shutter_speed)}, exposure_speed : {str(camera.exposure_speed)}, awbg : {str(awbg)}  ")
        image = frame.array
        rover_objects = Vision.get_rover_objects(processed_frame=image, get_new_frame=False,
                                                                         draw_cv=True)
        # show the frame
        cv2.imshow("Frame", image)
        key = cv2.waitKey(1) & 0xFF
        # clear the stream in preparation for the next frame
        rawCapture.truncate(0)
        # if the `q` key was pressed, break from the loop
        return rover_objects
        break
    
def wait(wait_time,samples_interrupt=False,rocks_interrupt=False,obstacle_interrupt=False,lander_interrupt=False,wall_interrupt=False):
    start_seconds = time.time()
    while True:
        current_time = time.time() - start_seconds
        print(f"Current time {round(current_time,2)}")
        read()
        if current_time > wait_time:
            break

def setISO(value):
    camera.iso = value
