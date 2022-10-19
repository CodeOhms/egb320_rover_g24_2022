import RPi.GPIO as GPIO

claw_servo = None
m_driver_in_1 = 14
m_driver_in_2 = 15
m_driver_in_3 = 18
m_driver_in_4 = 17
pwm = None
pwm2 = None
pwm3 = None
pwm4 = None

def init_impl():
    global claw_servo
    global pwm 
    global pwm2
    global pwm3
    global pwm4
    
    GPIO.setmode(GPIO.BCM)
    
    # # Claw servo:
    # GPIO.setup(, GPIO.OUT)
    # claw_servo = GPIO.PWM(, 100) # Updates at 100 Hz.
    
    # Motors:
        # Left:
    GPIO.setup(m_driver_in_1, GPIO.OUT)
    GPIO.setup(m_driver_in_2, GPIO.OUT)
    pwm = GPIO.PWM(m_driver_in_1, 100)
    pwm2 = GPIO.PWM(m_driver_in_2, 100)
    
        # Right:
    GPIO.setup(m_driver_in_3, GPIO.OUT)
    GPIO.setup(m_driver_in_4, GPIO.OUT)
    pwm3 = GPIO.PWM(m_driver_in_3, 100)
    pwm4 = GPIO.PWM(m_driver_in_4, 100)

def start_impl():
    global claw_servo
    global pwm 
    global pwm2
    global pwm3
    global pwm4
    
    # Start at duty cycle of 0 (stopped):
    pwm.start(0)
    pwm2.start(0)
    pwm3.start(0)
    pwm4.start(0)

    # Claw:
    # claw_servo.start(0) # Begin at 0 degrees.

def close_impl():
    GPIO.cleanup()
    print('Cleaned up GPIO.')
    print()

def servo_claw_impl(angle):
    global claw_servo
    
    duty_cycle = angle/180*100
    claw_servo.ChangeDutyCycle(duty_cycle)

def motor_halt_impl():
    print('pwm', pwm)
    print()
    
    pwm.ChangeDutyCycle(0)
    pwm2.ChangeDutyCycle(0)
    pwm3.ChangeDutyCycle(0)
    pwm4.ChangeDutyCycle(0)

def motor_forward_r_impl(duty_cycle):
    pwm3.ChangeDutyCycle(duty_cycle)
    # GPIO.output(m_driver_in_3, GPIO.HIGH)
    GPIO.output(m_driver_in_4, GPIO.LOW)

def motor_forward_l_impl(duty_cycle):
    print('pwm', pwm)
    print()
    pwm.ChangeDutyCycle(duty_cycle)
    # GPIO.output(m_driver_in_1, GPIO.HIGH)
    GPIO.output(m_driver_in_2, GPIO.LOW)

def motor_back_r_impl(duty_cycle):
    GPIO.output(m_driver_in_3, GPIO.LOW)
    # GPIO.output(m_driver_in_4, GPIO.HIGH)
    pwm4.ChangeDutyCycle(duty_cycle)

def motor_back_l_impl(duty_cycle):
    GPIO.output(m_driver_in_1, GPIO.LOW)
    # GPIO.output(m_driver_in_2, GPIO.HIGH)
    pwm2.ChangeDutyCycle(duty_cycle)