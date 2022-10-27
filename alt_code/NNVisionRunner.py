# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import NNVision as Vision
import PiCameraSystem as Pcam
from time import sleep
# initialize the camera and grab a reference to the raw camera capture


while True:
    rover_objects = Pcam.read()


