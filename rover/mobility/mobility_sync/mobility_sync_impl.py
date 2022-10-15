from gpio_interface import gpio_interface as io_pins

def init_sync_impl(gpio_interface):
    print('Initialising mobility system...')

def start_sync_impl():
    pass

def close_sync_impl():
    pass

def act_on_sync_impl(decision):
    print('Do: ', decision)
    print()

def act_lift_collector():
    '''
    Can be used to flip rocks over.
    '''