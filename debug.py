from abp import * 
from analysis import Analysis
##TODO find better way of importing to avoid cluttering namespace
from parameter_dictionaries import *
N = 100
test_dict = {
    "R":np.ones(N),
    "N":N,
    "v_0":0.01,
    "D":0.1,
    "k":1,
    "box_width":box_width_from_phi(N,0.6),
    "T":100000,
    "dt": 0.01,
    } 

pyABP_dict = {
    "R":np.ones(N),
    "N":2000,
    "v_0":0.1,
    "D":0.001,
    "k":1,
    "box_width":50,
    "T":100000,
    "dt": 0.01,
    } 

delta_test_dict = {
    "R":np.ones(N),
    "N":N,
    "v_0":0.01,
    "D":0.1,
    "k":1,
    "box_width":box_width_from_phi(N,0.6),
    "T":100000,
    "dt": 0.03,
    } 

##DATA GENERATION
# glass = ABP(glass_dict,repulsion_cohesion_potential)
# glass.generate_csv(100)
# dense_liquid = ABP(dense_liquid_dict,repulsion_cohesion_potential)
# dense_liquid.generate_csv(100)
# phase_seperated = ABP(phase_seperated_dict,repulsion_cohesion_potential)
# phase_seperated.generate_csv(100)
# normal_liquid = ABP(normal_liquid_dict,repulsion_cohesion_potential)
# normal_liquid.generate_csv(100)

##DELTA POTENTIAL TESTS
# deltas = [0.5]
# for delta in deltas:
#     def delta_potential(pvec,R=1,k=1,epsilon = 0.15,delta=delta):
#         return repulsion_cohesion_potential2(pvec,R,k,epsilon,delta)
#     delta_test = ABP(delta_test_dict,delta_potential)
#     delta_test.r = (delta_test.box_width/2)*np.ones((100,2))
#     folder_name = f"delta_{delta}_centre2"
#     delta_test.generate_csv(100,folder_name)
#     a = Analysis(f"./data/{folder_name}",test_dict,1000)
#     anim = a.animate_movement_patch(sample_rate=10)
#     anim.save(f"media/delta_{delta}_centre2_anim.mp4")

##PARABOLA POTENTIAL TESTS
ls = [-0.05,-0.1,-0.2,-0.4,-0.6,-0.8,-1]
for l in ls:
    def l_potential(pvec,R=1,k=1,epsilon = 0.5,l=l):
        return parabola_potential(pvec,R,k,epsilon,l)
    l_test = ABP(delta_test_dict,l_potential)
    # l_test.r = (l_test.box_width/2)*np.ones((100,2))
    folder_name = f"l_{l}"
    l_test.generate_csv(100,folder_name)
    a = Analysis(f"./data/{folder_name}",test_dict,1000)
    anim = a.animate_movement_patch(sample_rate=10)
    anim.save(f"media/l_{l}_anim.mp4")


##TEST ZONE
l = -0.5
def l_potential(pvec,R=1,k=1,epsilon = 0.5,l=l):
    return parabola_potential(pvec,R,k,epsilon,l)
l_test = ABP(delta_test_dict,l_potential)

print(l_test.interaction_forces()==np.nan)