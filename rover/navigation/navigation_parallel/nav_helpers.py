from enum import Enum
from mobility.mobility_enums import *
from mobility import mobility as mob

##########
# Potential Fields

def goal_potential_field(x_array, bearings, intensity, intensity_max):
    '''
    Piecewise triangular function.
    '''
    
    g_pf_total = np.zeros_like(x_array)
    m = intensity_max/x_array.max() # Gradients
    for i, bear in enumerate(bearings):
        c = (intensity[i] - m*bear, intensity[i] + m*bear)
        pw = np.piecewise(x_array, [x_array < bear, x_array >= bear], [lambda x: m*x+c[0], lambda x: -m*x+c[1]])
        # Clip results below zero and above intensity maximum:
        pw[pw<0] = 0
        pw[pw>intensity_max] = intensity_max
        g_pf_total = g_pf_total + pw            
    return g_pf_total

def hazard_potential_field(x_array, bearings, intensity, intensity_max):
    '''
    Piecewise square function.
    '''
    
    h_pf_total = np.zeros_like(x_array)
    for i, bear_range in enumerate(bearings):
        b_min = bear_range[0]
        b_max = bear_range[1]
        pw = np.where(((b_min <= x_array) & (x_array <= b_max)), intensity[i], 0)
        # Clip results below zero and above intensity maximum:
        pw[pw<0] = 0
        pw[pw>intensity_max] = intensity_max
        h_pf_total = h_pf_total + pw
    return h_pf_total

class PF(object):
    def __init__(self, pf_function, bearing_range=(-180,180), num_samples=360, y_data=None):
        self.pf_function = pf_function
        self.bearing_range = bearing_range
        b_min, b_max = bearing_range
        self.x_data = np.linspace(b_min, b_max, num=num_samples)
        if y_data is None:
            self.y_data = np.zeros_like(self.x_data)
        else:
            self.y_data = y_data
    
    # Alternative initialiser:
    @classmethod
    def heading_field(cls, goal_pot_f, haz_pot_f):
        heading_pf = goal_pot_f.y_data - haz_pot_f.y_data
        
        # Clip results below zero:
        heading_pf[heading_pf<0] = 0

        b_range = (goal_pot_f.x_data.min(), goal_pot_f.x_data.max())
        n_samp = goal_pot_f.x_data.size
        return cls(None, bearing_range=b_range, num_samples=n_samp, y_data=heading_pf)
    
    def gen_potential_field(self, bearings, intensity=None, intensity_max=1):
        if intensity is None:
            intensity = intensity_max
        pf_res = self.pf_function(self.x_data, bearings, intensity, intensity_max)
        
        # Clip results below zero and above intensity maximum:
        pf_res[pf_res<0] = 0
        pf_res[pf_res>intensity_max] = intensity_max
        
        self.y_data = pf_res




# if __name__ == '__main__':
#     goal_pf = PF(goal_potential_field)
#     haz_pf = PF(hazard_potential_field)
    
#     goal_pf.gen_potential_field((-90.0, 90), (0.6, 0.5))
#     haz_pf.gen_potential_field(((-80, -20), (-10, 10), (60, 110)), (0.8, 0.2, 0.8))
    
#     motor_heading_pf = PF.heading_field(goal_pf, haz_pf)
    
#     plt.figure()
#     plt.plot(goal_pf.x_data, goal_pf.y_data)
#     plt.title('Goal Potential Field')
    
#     plt.figure()
#     plt.plot(haz_pf.x_data, haz_pf.y_data)
#     plt.title('Hazard Potential Field')
    
#     plt.figure()
#     plt.plot(motor_heading_pf.x_data, motor_heading_pf.y_data)
#     plt.title('Motor Heading Potential Field')
#     plt.show()
    




# def create_potential_field(goal):
#     bearings = vis_get_bearings()
#     distance = vis_get_distances()
#     compiled_GD = []
#     if len(bearings[goal])==1:
#         GD = [[]]
#     elif len(bearings[goal])==2:
#         GD = [[],[]]
#     elif len(bearings[goal])==3:
#         GD = [[],[],[]]

#     for x in range(0,len(bearings[goal])):
#         for i in range(-31,32):
#             from_peak = abs(bearings[goal][x]-i)
#             peak = 283-distance[goal][x]
#             GD_value = peak-(peak*from_peak/31)
#                 if GD_value<0:
#                         GD_value = 0
#             GD[x] = GD[x] + [GD_value]
        
#     for j in range(0,63):
#         combined_GD_value = 0
#             for y in range(0,len(bearings[goal])):
#                 combined_GD_value = combinded_GD_value+GD[y][j]
#         compiled_GD = compiled_GD + [combined_GD_value]
    
#     compiled_OM = []
#     if len(bearings[3])==1:
#         OM = [[]]
#     elif len(bearings[3])==2:
#         OM = [[],[]]
#     elif len(bearings[3])==3:
#         OM = [[],[],[]]

#     for x in range(0,len(bearings[3])):
#         for i in range(-31,32):
#         from_peak = abs(bearings[3][x]-i)
#             peak = 283-distance[3][x]
#             if peak>203:
#                         if from_peak==0:
#                             OM_value = peak
#             decision_tool = peak-203
#                         if (descision_tool/from_peak)>4:
#                 OM_value = peak-(peak*from_peak/100)
#             else:
#                 OM_value = 0
#                 else:
#                     OM_value = 0
#             OM[x] = OM[x] + [OM_value]
        
#     for j in range(0,63):
#         combined_OM_value = 0
#             for y in range(0,len(bearings[3])):
#                 combined_OM_value = combinded_OM_value+OM[y][j]
#             compiled_OM = compiled_OM + [combined_OM_value]
    
#     compiled_PF = []
#     for i in range(0,63):
#         PF_value = compiled_GD[i]-compiled_OM[i]
#         compiled_PF = compiled_PF + [PF_value]
#     return compiled_PF

# def navigate_PF(PF):
#     max = max(PF)
#     position_of_max = PF.index(max)
#     bearing = position_of_max - 31
#     if bearing<0:
#         movement = (['left_f', 40*(1.0-0.8*abs(bearing)/40)], ['right_f', 40])
#     elif bearing>0:
#         movement = (['left_f', 40], ['right_f', 40*(1.0-0.8*abs(bearing)/40)])
#     else:
#         movement = (['left_f', 40], ['right_f', 40])
#     return bearing

##########


class Targets(Enum):
    sample = 2
    rock = 4
    lander = 5
    sample_and_lander = 6

def finding_target(target, vis_get_bearings, vis_get_distances, actions_q):
    '''
    Find either targets by priorty, or the target specified.

    @param target. If the parameter is
    'sample' the function will attempt to find a sample or a rock,
    but will prioritise finding a rock.
    If set to 'lander' the function will attempt to find the
    lander.
    '''

    decision = ()

    bearings = vis_get_bearings()
    distances = vis_get_distances()

    target_i = None # Target indicies in bearings and distances.
    if target == Targets.sample:
        target_i = [2]
    elif target == Targets.rock:
        target_i = [4]
    elif target == Targets.lander:
        target_i = [5]
    else:
        raise("Expected either Targets.sample, Targets.rock or Targets.lander for the `target` argument!")

    # Pivot to find a target:
    targ_bear = None
    targ_dist = None
    found_targ = None
    while(found_targ is None):
        for t_i in target_i:
            targ_bear = bearings[t_i]
            targ_dist = distances[t_i]
            if len(targ_bear) == 0 and len(targ_dist) == 0:
                actions_q.put( ((Actions.pivot_l,),) ) # Keep looking...
            else:
                actions_q.put( ((Actions.m_halt,),) ) # Found it! Stop!
                found_targ = Targets(t_i)
                break

    return found_targ

def approaching_target(target, vis_get_bearings, vis_get_distances, actions_q):
    decision = ()
    nx_st_cb = None
    
    bearings = vis_get_bearings()
    distances = vis_get_distances()
    
    target_i = None # Target indicies in bearings and distances.
    if target == Targets.sample:
        target_i = [2]
    elif target == Targets.rock:
        target_i = [4]
    elif target == Targets.lander:
        target_i = [5]
    else:
        raise("Expected either Targets.sample or Targets.lander for the `target` argument!")
    
    targ_bear = None
    targ_dist = None
    for t_i in target_i:
        targ_bear = bearings[t_i]
        targ_dist = distances[t_i]
        if len(targ_bear) < 1 and len(targ_dist) < 1:
            actions_q.put( ((Actions.m_halt,),) ) # Lost it! Stop!
            print('Target ' + str(target) + ' lost!')
            break
        else:
            # Approaching...
            PF = create_potential_field(2)
            steering = navigate_PF(PF)
            
            # Is it close enough to interact with?:
            if max(PF) > pf_max:
                # Make sure target aligned decently:
                if steering < 4 && steering > -4:
                    nx_st_cb = (nav_smachine.obtain_sample, None)
            else:
                nx_st_cb = (nav_smachine.cont_approach, None)
                   
        return nx_st_cb