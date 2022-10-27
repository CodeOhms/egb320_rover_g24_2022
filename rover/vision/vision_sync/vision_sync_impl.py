import copy
from multiprocessing import Queue
import numpy as np
import numexpr as ne
import cv2 as cv
from fast_slic import Slic
from scipy.spatial.distance import cdist
from vision.camera_input.cam_input import *

video_stream = None
cam_res = None
resolution = None
frame_queue = None
vision_queue = None
bearings_q = None
distances_q = None

f_scale = 4
f_height, f_width = (0, 0)

# For Pi camera v2.1:
# fov = (62.2, 48.8) # degrees
# focal_len = 3.04e-1 # cm
# px_height = 1.12e-4 # cm/px
# native_ver_px_height = 2464 # px
# For Logitech webcam:
fov = (62.2, 48.8) # degrees
focal_len = 3.08e-1 # cm
px_height = 0.00017097701149425287 # cm/px
native_ver_px_height = 960 # px
res_ver_scale = 0

obj_actual_heights = (None, None, 4.25, 15, 7, 4.5) # cm. Wall and floor, sample, obstacle, rock, lander

# # Setup camera undistort coefficients:
# mtx, distortion = load_coefficients('calibration_charuco.yml')
# newcameramtx, dist_roi = cv.getOptimalNewCameraMatrix(mtx, distortion, (f_width,f_height), 0, (f_width,f_height))
# mapx, mapy = cv.initUndistortRectifyMap(mtx, distortion, None, newcameramtx, (f_width,f_height), 5)

num_classes = 6 # Wall and floor, sample, obstacle, rock, lander

sat_mids = (0, 0, 0.65, 0.45, 0.95, 1.0)
# Hues (in degrees): 180, 220, 2, 110, 207
hue_mids = (
    3.14159265358979323846, 3.83972435438752506923, 0.03490658503988659154,
    1.65806278939461309808, 3.56047167406843233692, 1.04719755119659774615
) # Wall and floor, sample, obstacle, rock, lander
sat_hue_cnums = ne.evaluate('sat_mids*exp(complex(0,hue_mids))')
sat_hue_vecs = np.array([[hsm_comp.real, hsm_comp.imag] for hsm_comp in sat_hue_cnums])

font = cv.FONT_HERSHEY_SIMPLEX

num_regions = 25
regions_properties = [16, 8, 0, 0] # n_cells_x, n_cells_y, size_x, size_y

prev_frame_time = 0
new_frame_time = 0

def init_sync_impl(use_picam, cam_res):
    global f_height
    global f_width
    global video_stream
    global frame_queue
    global vision_queue
    global res_ver_scale
    global regions_properties
    global bearings_q
    global distances_q
    global resolution

    # f_height, f_width = (cam_res[1], cam_res[0])
    resolution = cam_res

    vid_s = init_video_stream(use_picam, cam_res)
    f_fifo_q = Queue()
    vis_fifo_q = Queue()
    video_stream = vid_s
    # video_stream = copy.copy(vid_s)
    frame_queue = f_fifo_q
    vision_queue = vis_fifo_q
    bearings_q = Queue()
    distances_q = Queue()

    # Setup display windows:
    cv.namedWindow("Frame")
    # cv.namedWindow("Wall mask")
    # cv.namedWindow("Floor mask")
    # cv.namedWindow("Sample mask")
    # cv.namedWindow("Obstacle mask")
    # cv.namedWindow("Rock mask")
    # cv.namedWindow("Lander mask")
    cv.namedWindow("Sample conv. hulls")
    cv.namedWindow("Obstacle conv. hulls")
    cv.namedWindow("Rock conv. hulls")
    cv.namedWindow("Lander conv. hulls")
    cv.namedWindow("Debug message")
    cv.moveWindow("Frame", 0, 0)
    # cv.moveWindow("Wall mask", f_width, 0)
    # cv.moveWindow("Floor mask", f_width*2, 0)
    # cv.moveWindow("Sample mask", f_width*3, 0)
    # cv.moveWindow("Obstacle mask", f_width*4, 0)
    # cv.moveWindow("Rock mask", f_width*5, 0)
    # cv.moveWindow("Lander mask", f_width*6, 0)
    win_y_offset = 32
    cv.moveWindow("Sample conv. hulls", 0, f_height+win_y_offset)
    cv.moveWindow("Obstacle conv. hulls", f_width*f_scale, f_height+win_y_offset)
    cv.moveWindow("Rock conv. hulls", f_width*f_scale*2, f_height+win_y_offset)
    cv.moveWindow("Lander conv. hulls", f_width*f_scale*3, f_height+win_y_offset)
    cv.moveWindow("Debug message", 0, f_height*(1+f_scale)+win_y_offset*2)

    return (vid_s, f_fifo_q, vis_fifo_q, bearings_q, distances_q)

def start_sync_impl(video_stream, iso):
    '''
    Implement the vision system synchronously (single-threaded). It will also
    use the shared FIFO buffer for the as the parallel implementations.
    '''
    
    global f_height
    global f_width
    global frame_queue
    global vision_queue
    global res_ver_scale
    global regions_properties
    global f_height
    global f_width
    global cam_res
    global resolution
    
    _, cam_res = camera_start(video_stream, iso)
    print('cam_res', cam_res)
    # f_height, f_width = (resolution[1], resolution[0])
    # f_width, f_height = resolution
    f_height, f_width = resolution
    res_ver_scale = native_ver_px_height/f_height
    regions_shape = [f_width//regions_properties[0], f_height//regions_properties[1]]
    regions_properties[2:] = regions_shape
    regions_properties = tuple(regions_properties)
    
    return video_stream, resolution

def close_sync_impl(video_stream):
    video_stream.stop()
    print('Cam closed')
    cv.destroyAllWindows()

def get_frame_sync_impl(f_q):
    global video_stream
    global vision_queue
    global bearings_q
    global distances_q

    frame = get_frame(video_stream)
    f_q.put(frame) # Put on queue so that it can be processed later,
                   # and viewed immediately as it is also returned!
    
    # This will only ever be called from the synchronous version!
    # Parallel version will start run in parallel with the start
    # command.
    overlays, bearings, distances = _vision_sys_sync_impl()
    vision_queue.put(overlays)
    bearings_q.put(bearings)
    distances_q.put(distances)

    return frame

def display_frame_sync_impl(frame):
    ret = True
    cv.imshow('Frame', frame)
    key = cv.waitKey(1) & 0xFF
    #if the `q` key was pressed, break from the loop
    if key == ord("q"):
        ret = False
    return ret

def get_overlays_sync_impl(vis_q):
    return vis_q.get()

def display_overlays_sync_impl(overlays):
    ret = True
    cv.imshow("Sample conv. hulls", overlays[2])
    cv.imshow("Obstacle conv. hulls", overlays[3])
    cv.imshow("Rock conv. hulls", overlays[4])
    cv.imshow("Lander conv. hulls", overlays[5])
    key = cv.waitKey(1) & 0xFF
    #if the `q` key was pressed, break from the loop
    if key == ord("q"):
        ret = False
    return ret

def get_bearings_sync_impl(bears_q):
    ret = None
    try:
        ret = bears_q.get(block=False)
    except:
        pass
    return ret

def get_bearings_sync_impl_(bears_q):
    ret = None
    try:
        ret = bears_q.get(block=False)
    except:
        pass
    return ret

def get_distances_sync_impl(dists_q):
    ret = None
    try:
        ret = dists_q.get(block=False)
    except:
        pass
    return ret

def get_distances_sync_impl_(dists_q):
    ret = None
    try:
        ret = dists_q.get(block=False)
    except:
        pass
    return ret

def superpx_slic_trans(img, num_regions=40):
    slic = Slic(num_components=num_regions, compactness=10, min_size_factor=0) # Supposedly gets FPS increase, but I don't see any...
    # slic = Slic(num_components=num_regions, compactness=10)
    segments = slic.iterate(img) # Cluster Map
    return segments

def grid_superpx_trans(img, regions_props):
    n_cells_x = regions_props[0]
    n_cells_y = regions_props[1]
    size_x = regions_props[2]
    size_y = regions_props[3]
    
    segments = np.zeros(img.shape[:2], dtype=int)
    for y in range(n_cells_y):
        for x in range(n_cells_x):
            segments[y*size_y:(y+1)*size_y,x*size_x:(x+1)*size_x] = x + y*n_cells_x
    return segments

def gen_superpx_img(img, regions_props):
    return superpx_slic_trans(img, regions_props)
    # return grid_superpx_trans(img, regions_props) # Slower without multithreading...

def get_region1d(img, superpx_img_indicies):
    return img[superpx_img_indicies]

def hue_sat_manhattan(args):
    img_comp = args[0]
    superpx_img_indicies = args[1]
    hue_sat_vec = args[3]

    # Region as a column of HSV pairs:
    region = get_region1d(img_comp, superpx_img_indicies)
    mhdist_between = cdist(hue_sat_vec, region, metric='cityblock')
    # hue_sat_q = np.quantile(mhdist_between, 0.25)
    hue_sat_q = np.mean(mhdist_between)

    return hue_sat_q

def gen_discriptor_img(superpx_img, img, descr_func, img_dtype=None, descr_func_args=[None], descr_dims=3):
    if img_dtype == None:
        img_dtype = img.dtype
    
    descriptors = [ ]
    im_descriptors = np.zeros((img.shape[0], img.shape[1], descr_dims), dtype=img_dtype)

    for i in range(superpx_img.min(), superpx_img.max()+1):
        args = [img, superpx_img==i, descr_dims] + descr_func_args
        descriptors.append(descr_func(args))
        im_descriptors[superpx_img==i] = descriptors[i]

    return (im_descriptors, descriptors)

def _vision_sys_sync_impl():
    global frame_queue
    global prev_frame_time
    global new_frame_time
    
    new_frame_time = time.time()
    
# Capture frame from camera:
    frame = frame_queue.get()
    if frame.shape[:2] != resolution:
        frame = cv.resize(frame, resolution)
    # frame = grab_frame(capture, cam_res)
    # frame_dist = grab_frame(capture, (3240,2464))
    # frame_dist = cv.resize(frame_dist, cam_res)

# # Undistort frame:
    # frame = cv.remap(frame_dist, mapx, mapy, cv.INTER_LINEAR)

# Setup display images:
    masks_shape = np.concatenate(((f_width, f_height), np.array([num_classes])))
    # masks_shape = np.concatenate((frame.shape[:2], np.array([num_classes])))
    masks_hue = np.zeros(masks_shape, dtype=np.uint8)
    masks_sat = np.zeros(masks_shape, dtype=np.uint8)
    masks_objs = np.zeros(masks_shape, dtype=np.uint8)
    frame_masked_objs = np.zeros(masks_shape)
    dbug_img = np.zeros((100,512,3),np.uint8)
    f_upscale = cv.resize(copy.deepcopy(frame), dsize=None, fx=f_scale, fy=f_scale, interpolation= cv.INTER_LINEAR) # Upscale for display!
    contours_imgs = [copy.deepcopy(f_upscale) for x in range(num_classes)]

# Create superpixel image:
    superpx_img = gen_superpx_img(frame, num_regions)
    # superpx_img = gen_superpx_img(frame, regions_properties)

# Apply descriptors:
    frame_f32 = np.float32(frame)
    frame_hsv = cv.cvtColor(frame_f32, cv.COLOR_BGR2HSV_FULL)
    frame_hue = frame_hsv[:,:,0]
    frame_sat = frame_hsv[:,:,1]
    pi = np.pi
    frame_comp = ne.evaluate('frame_sat*exp(complex(0,frame_hue*pi/180))')
    frame_vecs = np.array([[[comp.real,comp.imag] for comp in row] for row in frame_comp[:]])

    # Hue MAD from given hue:
    hue_mads_imgs_and_decrs = np.array(
        [gen_discriptor_img(superpx_img, frame_vecs, hue_sat_manhattan,
                            descr_func_args=[np.array([ sat_hue_vecs[i] ])], descr_dims=1, img_dtype=np.float32)
                            for i in range(num_classes)
        ]
    )
    hue_mad_imgs = hue_mads_imgs_and_decrs[:,0]
    hue_mad_descrs = hue_mads_imgs_and_decrs[:,1]

# Select descriptors to mask objects:
    # mad_threshold = 0.15
    # mad_threshold = 1.0
    hue_mad_regions = np.zeros((1,3))
    hue_mad_labels = hue_mad_descrs
    for i_reg, reg_label in enumerate(np.unique(superpx_img)):
        hue_mad_regions = np.array([hmad_lab[i_reg] for hmad_lab in hue_mad_labels])
        reg_idxs = superpx_img == reg_label
        hue_img_idx = np.argmin(hue_mad_regions)
        # if hue_mad_regions[hue_img_idx] < mad_threshold:
        #     masks_hue[:,:,hue_img_idx][reg_idxs] = 255
        masks_hue[:,:,hue_img_idx][reg_idxs] = 255

# Find contours and bounding boxes:
    contours = [ ]
    cnts_poly = [[ ] for x in range(num_classes)]
    bound_boxes = [[ ] for x in range(num_classes)]
    for cl_i in range(num_classes):
        conts, _ = cv.findContours(masks_hue[:,:,cl_i], cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        contours.append(conts)
    # Find the bounding box for each contour, and draw them:
        for cnt in conts:
            c_poly = cv.approxPolyDP(cnt, 3, True)
            cnts_poly[cl_i].append(c_poly)
            bbox = cv.boundingRect(c_poly)
            bound_boxes[cl_i].append(bbox)
            bbox = np.multiply(f_scale, bbox)
            cv.rectangle(
                contours_imgs[cl_i], (int(bbox[0]), int(bbox[1])),
                (int(bbox[0]+bbox[2]), int(bbox[1]+bbox[3])), (250,0,255), 2
            )

# Correct for distortions:

# Estimate bearing:
    cen_x = [[ ] for x in range(num_classes)]
    bearings = [[ ] for x in range(num_classes)]
    depths = [[ ] for x in range(num_classes)]
    for cl_i, bboxs in enumerate(bound_boxes):
        for bound_box in bboxs:
            # Centre bearing:
            cx = bound_box[0] + bound_box[2]//2 # x + width/2
            cy = bound_box[1] + bound_box[3]//2 # y + height/2
            scaled_cen = (cx*f_scale,cy*f_scale)
            contours_imgs[cl_i] = cv.circle(contours_imgs[cl_i], scaled_cen, radius=2, color=(0, 0, 255), thickness=-1)
            cen_x[cl_i].append(cx)
            cen_bearing = x_px_to_horz_bearing(cx, f_width, fov[0])
            
            # Bearings of the left and right sides:
            lx = bound_box[0] # x
            rx = bound_box[0] + bound_box[2] # x + width
            lb = x_px_to_horz_bearing(lx, f_width, fov[0])
            rb = x_px_to_horz_bearing(rx, f_width, fov[0])
            
            bearings[cl_i].append( (cen_bearing, lb, rb) )

            if obj_actual_heights[cl_i] != None:
                obj_px_height = bound_box[3]
                obj_height = obj_px_height*px_height*res_ver_scale
                obj_distance = obj_actual_heights[cl_i]*focal_len/obj_height
                # Manual calc. of px_height for Logitech webcam:
                # (obj_actual_height/obj_distance) * focal_len * 1/(obj_px_height*res_ver_scale)
                # 7.975[cm] * 4.25[cm]/0.308[cm] * 1/(58[px]*16) = 0.11858258928571428571[cm/px]
                depths[cl_i].append(obj_distance)

                cv.putText(
                    contours_imgs[cl_i], "B: "+str(cen_bearing),
                    scaled_cen, font, 0.3, (255,255,255), 1, cv.LINE_AA
                )
                cv.putText(
                    contours_imgs[cl_i], "D: "+str(obj_distance),
                    (scaled_cen[0],scaled_cen[1]+8), font, 0.3, (255,255,255), 1, cv.LINE_AA
                )
        
    fps = 1/(new_frame_time - prev_frame_time)
    cv.putText(dbug_img, "FPS "+str(fps), (0,25), font, 1, (255,255,255), 2, cv.LINE_AA)
    cv.imshow("Debug message", dbug_img)
    prev_frame_time = new_frame_time

    return (contours_imgs, bearings, depths)

def x_px_to_horz_bearing(x_px, f_width, fov_hor):
    return (x_px-f_width/2)/f_width*fov_hor