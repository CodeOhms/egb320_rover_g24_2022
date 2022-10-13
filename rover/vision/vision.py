from vision.camera_input.cam_input import init_video_stream
import vision.vision_impl as impl

video_stream = None




# f_scale = 4
# f_height, f_width = frame.shape[:2]

# fov = [62.2, 48.8] # degrees
# focal_len = 3.04e-1 # cm
# px_height = 1.12e-4 # cm
# res_ver_scale = 2464/f_height

# obj_actual_heights = [None, None, 4.3, 15, 7, 4.5] # cm. Wall and floor, sample, obstacle, rock, lander

# # # Setup camera undistort coefficients:
# # mtx, distortion = load_coefficients('calibration_charuco.yml')
# # newcameramtx, dist_roi = cv.getOptimalNewCameraMatrix(mtx, distortion, (f_width,f_height), 0, (f_width,f_height))
# # mapx, mapy = cv.initUndistortRectifyMap(mtx, distortion, None, newcameramtx, (f_width,f_height), 5)

# num_classes = 6 # Wall and floor, sample, obstacle, rock, lander

# sat_mids = [0, 0, 0.65, 0.45, 0.95, 1.0]
# # Hues (in degrees): 180, 220, 2, 110, 207
# hue_mids = [
#     3.14159265358979323846, 3.83972435438752506923, 0.03490658503988659154,
#     1.65806278939461309808, 3.56047167406843233692, 1.04719755119659774615
# ] # Wall and floor, sample, obstacle, rock, lander
# sat_hue_cnums = ne.evaluate('sat_mids*exp(complex(0,hue_mids))')
# sat_hue_vecs = np.array([[hsm_comp.real, hsm_comp.imag] for hsm_comp in sat_hue_cnums])

# prev_frame_time = 0
# new_frame_time = 0

# font = cv.FONT_HERSHEY_SIMPLEX

# num_regions = 25
# regions_properties = [16, 8, 0, 0] # n_cells_x, n_cells_y, size_x, size_y
# regions_shape = [f_width//regions_properties[0], f_height//regions_properties[1]]
# regions_properties[2:] = regions_shape





def init(cam_res=(64, 32)):
    global video_stream
    video_stream = impl.init_impl(video_stream, cam_res)

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
    return impl.get_frame_impl(video_stream)

def get_overlay():
    pass

def get_bearings():
    pass

def get_distances():
    pass