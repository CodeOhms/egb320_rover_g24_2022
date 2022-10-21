import gpio_interface.gpio_interface_impl as impl

def init():
    return impl.init_impl()

def start(internal_data):
    impl.start_impl(internal_data)

def close():
    impl.close_impl()

def servo_claw(angle):
    impl.servo_claw_impl(angle)

def motor_halt(internal_data):
    impl.motor_halt_impl(internal_data)

def motor_forward_r(internal_data, duty_cycle):
    impl.motor_forward_r_impl(internal_data, duty_cycle)

def motor_forward_l(internal_data, duty_cycle):
    impl.motor_forward_l_impl(internal_data, duty_cycle)

def motor_back_r(internal_data, duty_cycle):
    impl.motor_back_r_impl(internal_data, duty_cycle)

def motor_back_l(internal_data, duty_cycle):
    impl.motor_back_l_impl(internal_data, duty_cycle)
