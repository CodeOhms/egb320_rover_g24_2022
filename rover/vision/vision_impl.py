from vision.vision_sync.vision_sync_impl import *

def init_impl(cam_res):
    return init_sync_impl(cam_res)

def start_impl(video_stream, iso):
    return start_sync_impl(video_stream, iso)

def close_impl(video_stream):
    close_sync_impl(video_stream)

# def write_data_impl():
#     write_data_sync_impl()

def get_frame_impl(f_q):
    return get_frame_sync_impl(f_q)

def display_frame_impl(frame):
    return display_frame_sync_impl(frame)

def get_overlays_impl(vis_q):
    return get_overlays_sync_impl(vis_q)

def display_overlays_impl(overlays):
    return display_overlays_sync_impl(overlays)

def get_bearings_impl(bears_q):
    return get_bearings_sync_impl(bears_q)

def get_bearings_impl_(bears_q):
    return get_bearings_sync_impl_(bears_q)

def get_distances_impl(dists_q):
    return get_distances_sync_impl(dists_q)

def get_distances_impl_(dists_q):
    return get_distances_sync_impl_(dists_q)