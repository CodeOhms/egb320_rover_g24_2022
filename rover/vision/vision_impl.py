from vision.vision_sync.vision_sync_impl import *

def init_impl(video_stream, cam_res):
    return init_sync_impl(video_stream, cam_res)

def start_impl(video_stream):
    return start_sync_impl(video_stream)

def close_impl(video_stream):
    close_sync_impl(video_stream)

# def write_data_impl():
#     write_data_sync_impl()

def get_frame_impl(video_stream):
    return get_frame_sync_impl(video_stream)