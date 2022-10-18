import gpio_interface.gpio_interface_impl as impl

def init():
    impl.init_impl()

def start():
    impl.start_impl()

def close():
    impl.close_impl()

def servo_claw():
    impl.servo_claw_impl()

def motor_halt():
    impl.motor_halt_impl()

def motor_forward_r():
    impl.motor_forward_r_impl()

def motor_forward_l():
    impl.motor_forward_l_impl()

def motor_back_r():
    impl.motor_back_r_impl()

def motor_back_l():
    impl.motor_back_l_impl()
