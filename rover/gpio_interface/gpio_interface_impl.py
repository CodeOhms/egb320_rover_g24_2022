import RPi.GPIO as GPIO
import copy

class GpioInternalData(object):
    def __init__(self, c_servo, m_driver_inputs, pwms):
        self.m_driver_in_1, self.m_driver_in_2, self.m_driver_in_3, self.m_driver_in_4 = m_driver_inputs
        self.claw_servo = c_servo
        self.pwm, self.pwm2, self.pwm3, self.pwm4 = pwms

def init_impl():
    # in1 green 
    # in2 yellow
    # in3 dark purple
    # in4 gray
    m_driver_in_1 = 27
    m_driver_in_2 = 22
    m_driver_in_3 = 18
    m_driver_in_4 = 17
    # m_driver_in_1 = 14
    # m_driver_in_2 = 15
    # m_driver_in_3 = 17
    # m_driver_in_4 = 18
    
    #servo bcm 22
    
    m_driver_inputs = (m_driver_in_1, m_driver_in_2, m_driver_in_3, m_driver_in_4)
    
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
    pwms = (pwm, pwm2, pwm3, pwm4)
    m_driver_inputs = (m_driver_in_1, m_driver_in_2, m_driver_in_3, m_driver_in_4)
    
    gpio_internal_data = GpioInternalData(None,  m_driver_inputs, pwms)
    print('gpio_internal_data', gpio_internal_data)
    print('gpio_internal_data.pwm', gpio_internal_data.pwm)
    print()
    return gpio_internal_data

def start_impl(internal_data):
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
    internal_data.pwm.ChangeDutyCycle(0)
    internal_data.pwm2.ChangeDutyCycle(0)
    internal_data.pwm3.ChangeDutyCycle(0)
    internal_data.pwm4.ChangeDutyCycle(0)

def motor_forward_r_impl(internal_data, duty_cycle):
    internal_data.pwm3.ChangeDutyCycle(duty_cycle)
    # GPIO.output(m_driver_in_3, GPIO.HIGH)
    GPIO.output(internal_data.m_driver_in_4, GPIO.LOW)

def motor_forward_l_impl(internal_data, duty_cycle):
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