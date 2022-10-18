import RPi.GPIO as GPIO

claw_servo = None
m_driver_in_1 = 14
m_driver_in_2 = 15
m_driver_in_3 = 18
m_driver_in_4 = 17

def init_impl():
    global claw_servo
    
    GPIO.setmode(GPIO.BCM)
    
    # # Claw servo:
    # GPIO.setup(, GPIO.OUT)
    # claw_servo = GPIO.PWM(, 100) # Updates at 100 Hz.
    
    # Motors:
        # Left:
    GPIO.setup(m_driver_in_1, GPIO.OUT)
    GPIO.setup(m_driver_in_2, GPIO.OUT)
        # Right:
    GPIO.setup(m_driver_in_3, GPIO.OUT)
    GPIO.setup(m_driver_in_4, GPIO.OUT)

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

def motor_halt_impl():
    GPIO.output(m_driver_in_1, GPIO.LOW)
    GPIO.output(m_driver_in_2, GPIO.LOW)
    GPIO.output(m_driver_in_3, GPIO.LOW)
    GPIO.output(m_driver_in_4, GPIO.LOW)

def motor_forward_r_impl():
    GPIO.output(m_driver_in_3, GPIO.HIGH)
    GPIO.output(m_driver_in_4, GPIO.LOW)

def motor_forward_l_impl():
    GPIO.output(m_driver_in_1, GPIO.HIGH)
    GPIO.output(m_driver_in_2, GPIO.LOW)

def motor_back_r_impl():
    GPIO.output(m_driver_in_3, GPIO.LOW)
    GPIO.output(m_driver_in_4, GPIO.HIGH)

def motor_back_l_impl():
    GPIO.output(m_driver_in_1, GPIO.LOW)
    GPIO.output(m_driver_in_2, GPIO.HIGH)