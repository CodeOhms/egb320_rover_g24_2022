from cam_input import init_video_stream
from vision_impl import *

def init_vision(cam_res=(64, 32)):
    init_video_stream(vid_stream, cam_res)

def vision_start():
    vision_start_impl()

def vision_close():
    pass

def vision_write_data():
    '''
    The purpose of this function is to transfer calculated data from the
    vision system code to a shared FIFO buffer. From this buffer, the
    helper functions `get_frame()`, `get_bearings()` and `get_distances()` can be
    used to read data from this shared buffer easily.
    This makes it easier to implement parallel code with either:
    multiprocessing, multithreading, or asynchronous threading.
    '''

def get_frame():
    pass

def get_bearings():
    pass

def get_distances():
    pass