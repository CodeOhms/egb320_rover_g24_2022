import RPi.GPIO as GPIO

def init_impl():
    GPIO.setmode(GPIO.BOARD)

def start_impl():
    pass

def close_impl():
    GPIO.cleanup()

def motor_fr_impl():
    pass

def motor_fl_impl():
    pass

def motor_br_impl():
    pass

def motor_bl_impl():
    pass