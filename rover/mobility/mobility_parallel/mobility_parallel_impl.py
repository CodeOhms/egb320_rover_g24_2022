from multiprocessing import Process, Queue
from gpio_interface import gpio_interface as io_pins
from mobility.mobility_enums import *

mobility_process = None
mobility_q = None

def mobility_loop(mob_q):
    ret = True
    try:
        actions = mob_q.get(block=False)
        print('actions', actions)
        print()
        if actions[0] == 'close':
            ret = False
        else:
            print('act')
            act_on_parallel_impl(actions)
    except:
        pass # Nothing in queue, yet
    return ret

def mobility_main(mob_q):
    loop = True
    
    # Initialise:
    io_pins.init()
    
    # Start:
    io_pins.start()
    
    # Loop:
    while(loop):
        loop = mobility_loop(mob_q)

    # Close:
    print('ASDFJKWJE0F[W0[=F SOPFJ[WFJPOWJFOPW FOFPOOPFOPF')
    mobility_q.close()
    io_pins.close()

def init_parallel_impl():
    global mobility_process
    global mobility_q
    
    # Initialise:
    # io_pins.init()
    
    # # Start:
    # io_pins.start()
    
    mobility_q = Queue()
    mobility_process = Process(target=mobility_main, args=(mobility_q,))
    
    return mobility_q

def start_parallel_impl():
    global mobility_process    
    mobility_process.start()

def close_parallel_impl():
    global mobility_process
    global mobility_q
    
    print('TELL MOB PROCESS TO CLOSE!!!')
    mobility_q.put( ('close',) )
    mobility_process.join()

def act_on_parallel_impl(actions):
    print('Do: ', actions)
    print()
    
    # Before every action, a halt is necessary:
    act_m_halt()
    
    for action in actions:
        action = action[0]
        if action is Actions.m_halt:
            act_m_halt()
        elif action is Actions.m_forward_r:
            act_m_forward_r(30)
        elif action is Actions.m_forward_l:
            act_m_forward_l(30)
        elif action is Actions.m_back_r:
            act_m_back_r(30)
        elif action is Actions.m_back_l:
            act_m_back_l(30)
        elif action is Actions.pivot_l:
            act_m_back_r(30)
            act_m_forward_l(30)
        elif action is Actions.pivot_r:
            act_m_back_l(30)
            act_m_forward_r(30)

def act_m_halt():
    io_pins.motor_halt()

def act_m_back_l(duty_cycle):
    io_pins.motor_back_l(duty_cycle)

def act_m_back_r(duty_cycle):
    io_pins.motor_back_r(duty_cycle)

def act_m_forward_l(duty_cycle):
    io_pins.motor_forward_l(duty_cycle)

def act_m_forward_r(duty_cycle):
    io_pins.motor_forward_r(duty_cycle)

def act_lift_collector():
    '''
    Can be used to flip rocks over.
    '''
    pass