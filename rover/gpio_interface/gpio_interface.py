import gpio.gpio_impl as impl

def init():
    impl.init_impl()

def start():
    impl.start_impl()

def close():
    impl.close_impl()

def servo_claw():
    impl.servo_claw_impl()

def motor_fr():
    impl.motor_fr_impl()

def motor_fl():
    impl.motor_fl_impl()

def motor_br():
    impl.motor_br_impl()

def motor_bl():
    impl.motor_bl_impl()
