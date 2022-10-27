import vision.vision_impl as impl

video_stream = None
actual_res = None
frame_queue = None
vision_queue = None
bearings_q = None
distances_q = None

def init(use_picam=True, cam_res=(64, 32)):
    global video_stream
    global frame_queue
    global vision_queue
    global bearings_q
    global distances_q
    
    # Res for webcam. Comment when using Pi cam.:
    # use_picam = False
    # cam_res=(80, 60)
    video_stream, frame_queue, vision_queue, bearings_q, distances_q = impl.init_impl(use_picam, cam_res)

def start(iso=600):
    global video_stream
    global actual_res
    
    video_stream, actual_res = impl.start_impl(video_stream, iso)

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
    global frame_queue
    return impl.get_frame_impl(frame_queue)

def display_frame(frame):
    global frame_queue
    return impl.display_frame_impl(frame)

def get_overlays():
    global vision_queue
    return impl.get_overlays_impl(vision_queue)

def display_overlays(overlays):
    return impl.display_overlays_impl(overlays)

def get_bearings_queue():
    global bearings_q
    return bearings_q

def get_bearings():
    global bearings_q
    return impl.get_bearings_impl(bearings_q)

def get_distances_queue():
    global distances_q
    return distances_q

def get_distances():
    global distances_q
    return impl.get_distances_impl(distances_q)