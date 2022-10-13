from vision.camera_input.cam_input import *

def init_sync_impl(video_stream, cam_res):
    return init_video_stream(cam_res)

def start_sync_impl(video_stream):
    '''
    Implement the vision system synchronously (single-threaded). It will also
    use the shared FIFO buffer for the as the parallel implementations.
    '''
    
    return camera_start(video_stream)

def close_sync_impl(video_stream):
    video_stream.stop()

# def write_data_sync_impl():
#     pass

def get_frame_sync_impl(video_stream):
    return get_frame(video_stream)