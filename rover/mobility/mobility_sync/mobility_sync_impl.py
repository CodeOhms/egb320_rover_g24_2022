from mobility.mobility_enums import *
from gpio_interface import gpio_interface as io_pins

def init_sync_impl():
    print('Initialising mobility system...')

def start_sync_impl():
    pass

def close_sync_impl():
    pass

def act_on_sync_impl(decisions):
    print('Do: ', decisions)
    print()
    
    # ( ('claw_up',), ('stop',), ('right_f', 30) )
    for decision in decisions:
        action = decision[0]
        if action is Actions.m_forward_r:
            act_m_forward_r(20)
        elif Actions.m_forward_l:
            pass
        elif Actions.m_back_r:
            pass
        elif Actions.m_back_l:
            dc = decision[1]
            act_m_back_l(dc)
        elif dec is Actions.pivot_l:
            act_m_back_l(30)
            act_m_forward_r(30)
            
def act_m_back_l(duty_cycle):
    io_pins.motor_back_l()

def act_m_back_r(duty_cycle):
    io_pins.motor_back_r()

def act_m_forward_l(duty_cycle):
    io_pins.motor_forward_l()

def act_m_forward_r(duty_cycle):
    io_pins.motor_forward_r()

def act_lift_collector():
    '''
    Can be used to flip rocks over.
    '''
    pass