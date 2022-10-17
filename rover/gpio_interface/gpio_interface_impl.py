import RPi.GPIO as GPIO

claw_servo = None

def init_impl():
    global claw_servo
    
    GPIO.setmode(GPIO.BOARD)
    
    # Claw:
    GPIO.setup(, GPIO.OUT)
    claw_servo = GPIO.PWM(, 100) # Updates at 100 Hz.


def start_impl():
    global claw_servo

    # Claw:
    # claw_servo.start(0) # Begin at 0 degrees.

def close_impl():
    GPIO.cleanup()

def servo_claw_impl(angle):
    global claw_servo
    
    duty_cycle = angle/180*100
    claw_servo.ChangeDutyCycle(duty_cycle)

def motor_fr_impl():
    pass

def motor_fl_impl():
    pass

def motor_br_impl():
    pass

def motor_bl_impl():
    pass