import gpio_interface.gpio_interface_impl as impl

def init():
    impl.init_impl()

def start():
    impl.start_impl()

def close():
    impl.close_impl()

def servo_claw(angle):
    impl.servo_claw_impl(angle)

def motor_halt():
    impl.motor_halt_impl()

def motor_forward_r(duty_cycle):
    impl.motor_forward_r_impl(duty_cycle)

def motor_forward_l(duty_cycle):
    impl.motor_forward_l_impl(duty_cycle)

def motor_back_r(duty_cycle):
    impl.motor_back_r_impl(duty_cycle)

def motor_back_l(duty_cycle):
    impl.motor_back_l_impl(duty_cycle)
