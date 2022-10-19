import RPi.GPIO as GPIO
import copy

# claw_servo = None
# m_driver_in_1 = 14
# m_driver_in_2 = 15
# m_driver_in_3 = 18
# m_driver_in_4 = 17
# pwm = None
# pwm2 = None
# pwm3 = None
# pwm4 = None

class GpioInternalData(object):
    def __init__(self, c_servo, pwms):
        self.m_driver_in_1 = 14
        self.m_driver_in_2 = 15
        self.m_driver_in_3 = 18
        self.m_driver_in_4 = 17
        
        self.claw_servo = c_servo
        print('pwms', pwms)
        print()
        self.pwm, self.pwm2, self.pwm3, self.pwm4 = pwms
        print('pwm in internal data', self.pwm)

def init_impl():
    # global claw_servo
    # global pwm 
    # global pwm2
    # global pwm3
    # global pwm4
    
    m_driver_in_1 = 14
    m_driver_in_2 = 15
    m_driver_in_3 = 18
    m_driver_in_4 = 17
    
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
    
    gpio_internal_data = GpioInternalData(None, (pwm, pwm2, pwm3, pwm4))
    print('gpio_internal_data', gpio_internal_data)
    print('gpio_internal_data.pwm', gpio_internal_data.pwm)
    print()
    return gpio_internal_data

def start_impl(internal_data):
    # global claw_servo
    # global pwm 
    # global pwm2
    # global pwm3
    # global pwm4
    
    # Start at duty cycle of 0 (stopped):
    internal_data.pwm.start(0)
    internal_data.pwm2.start(0)
    internal_data.pwm3.start(0)
    internal_data.pwm4.start(0)

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

def motor_halt_impl(internal_data):    
    print('pwm', internal_data.pwm)
    print()
    
    internal_data.pwm.ChangeDutyCycle(0)
    internal_data.pwm2.ChangeDutyCycle(0)
    internal_data.pwm3.ChangeDutyCycle(0)
    internal_data.pwm4.ChangeDutyCycle(0)

def motor_forward_r_impl(internal_data, duty_cycle):
    internal_data.pwm3.ChangeDutyCycle(duty_cycle)
    # GPIO.output(m_driver_in_3, GPIO.HIGH)
    GPIO.output(internal_data.m_driver_in_4, GPIO.LOW)

def motor_forward_l_impl(internal_data, duty_cycle):
    print('pwm', internal_data.pwm)
    print()
    internal_data.pwm.ChangeDutyCycle(duty_cycle)
    # GPIO.output(m_driver_in_1, GPIO.HIGH)
    GPIO.output(internal_data.m_driver_in_2, GPIO.LOW)

def motor_back_r_impl(internal_data, duty_cycle):
    GPIO.output(internal_data.m_driver_in_3, GPIO.LOW)
    # GPIO.output(m_driver_in_4, GPIO.HIGH)
    internal_data.pwm4.ChangeDutyCycle(duty_cycle)

def motor_back_l_impl(internal_data, duty_cycle):
    GPIO.output(internal_data.m_driver_in_1, GPIO.LOW)
    # GPIO.output(m_driver_in_2, GPIO.HIGH)
    internal_data.pwm2.ChangeDutyCycle(duty_cycle)