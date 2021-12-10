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
    "v_0":0.1,
    "D":0.1,
    "k":1,
    "box_width":box_width_from_phi(N,0.6),
    "T":100000,
    "dt": 0.01,
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
deltas = [0.3,0.35,0.4,0.45,0.5,1,2]
for delta in deltas:
    def delta_potential(pvec,R=1,k=1,epsilon = 0.15,delta=delta):
        return repulsion_cohesion_potential2(pvec,R,k,epsilon,delta)
    delta_test = ABP (delta_test_dict,delta_potential)
    folder_name = f"delta_{delta}"
    delta_test.generate_csv(100,folder_name)
    a = Analysis(f"./data/{folder_name}",test_dict,1000)
    anim = a.animate_movement_patch(sample_rate=10)
    anim.save(f"media/delta_{delta}_anim.mp4")

# a2 = Analysis("C:/Users/bennm/Documents/UNI/Year3/pyABP/pyABP/test_data1",pyABP_dict,100,data_type="pyABP")
# anim = a2.animate_movement_patch(sample_rate=1)
# # plt.show()
# anim.save("media/pyabp_test.mp4")

