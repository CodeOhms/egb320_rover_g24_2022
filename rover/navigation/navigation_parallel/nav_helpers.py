from enum import Enum
from mobility.mobility_enums import *
from mobility import mobility as mob

##########
# Potential Fields

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

def finding_target(target, vis_get_bearings, vis_get_distances):
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
                mob.act_on( ((Actions.pivot_l,),) ) # Keep looking...
            else:
                mob.act_on( ((Actions.m_halt,),) ) # Found it! Stop!
                found_targ = Targets[t_i]
                break

    return found_targ

# def approaching_target(target, vis_get_bearings, vis_get_distances):
#     decision = ()
#     nx_st_cb = None
    
#     bearings = vis_get_bearings()
#     distances = vis_get_distances()
    
#     target_i = None # Target indicies in bearings and distances.
#     if target == Targets.sample:
#         target_i = [2]
#     elif target == Targets.rock:
#         target_i = [4]
#     elif target == Targets.lander:
#         target_i = [5]
#     else:
#         raise("Expected either Targets.sample or Targets.lander for the `target` argument!")
    
#     targ_bear = None
#     targ_dist = None
#     for t_i in target_i:
#         targ_bear = bearings[t_i]
#         targ_dist = distances[t_i]
#         if len(targ_bear) < 1 and len(targ_dist) < 1:
#             decision = (('halt')) # Lost it! Stop!
#             print('Target ' + str(target) + ' lost!')
#             break
#         else:
#             # Approaching...
#             PF = create_potential_field(2)
#             steering = navigate_PF(PF)
            
#             # Is it close enough to interact with?:
#             if max(PF) > pf_max:
#                 # Make sure target aligned decently:
#                 if steering < 4 && steering > -4:
#                     nx_st_cb = (nav_smachine.obtain_sample, None)
#             else:
#                 nx_st_cb = (nav_smachine.cont_approach, None)
                   
#         return decision, nx_st_cb