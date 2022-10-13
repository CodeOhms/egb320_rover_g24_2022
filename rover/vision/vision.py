from vision.camera_input.cam_input import init_video_stream
import vision.vision_impl as impl

video_stream = None
frame_queue = None
vision_queue = None

def init(cam_res=(64, 32)):
    global video_stream
    global frame_queue
    global vision_queue
    
    video_stream, frame_queue, vision_queue = impl.init_impl(cam_res)

def start():
    global video_stream
    video_stream = impl.start_impl(video_stream)

def close():
    impl.close_impl(video_stream)

# def write_data():
#     '''
#     The purpose of this function is to transfer calculated data from the
#     vision system code to a shared FIFO buffer. From this buffer, the
#     helper functions `get_frame()`, `get_bearings()` and `get_distances()` can be
#     used to read data from this shared buffer easily.
#     This makes it easier to implement parallel code with either:
#     multiprocessing, multithreading, or asynchronous threading.
#     '''

#     impl.write_data_impl()

def get_frame():
    return impl.get_frame_impl(frame_queue)

def display_frame(frame):
    return impl.display_frame_impl(frame)

def get_overlays():
    return impl.get_overlays_impl(vision_queue)

def display_overlays(overlays):
    return impl.display_overlays_impl(overlays)

def get_bearings():
    pass

def get_distances():
    pass