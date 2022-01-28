from cv2 import circle
from abp import * 
from analysis import Analysis
from circle_test import circle_test, circle_test_setup
from potentials import k_2_potential
##TODO find better way of importing to avoid cluttering namespace
from parameter_dictionaries import *


##CENTRE TEST PACKING FRACTION 1
k_2s = [0,0.4,0.8,1.2,1.6,2]
epsilons = [0.05,0.1,0.15,0.2,0.25,0.3] 
for k_2 in k_2s:
    for epsilon in epsilons:
        folder_name = circle_test_setup(k_2_potential,[1,k_2,epsilon],k2_test_dict)


##CENTRE TESTS
# k_2s = [1]
# epsilon = 0.05
# for k_2 in k_2s:
#     # def k_2_potential(pvec,R=1,k=1,epsilon = epsilon,k_2=k_2):
#     #     return repulsion_cohesion_potential2(pvec,R,k,epsilon,k_2)
#     # k_2_test = ABP(delta_test_dict,k_2_potential)
#     # k_2_test.r = (k_2_test.box_width/2)*np.ones((100,2))
#     folder_name = f"k_2_{k_2}_e_{epsilon}v2"
#     # k_2_test.generate_csv(100,folder_name)
#     a = Analysis(f"./data/{folder_name}",test_dict,100)
#     anim = a.animate_movement_patch(sample_rate=1)
#     anim.save(f"media/k_2_{k_2}_e_{epsilon}_anim2.mp4")

##PARABOLA POTENTIAL TESTS
# ls = [-0.05,-0.1,-0.2,-0.4,-0.6,-0.8,-1]
# for l in ls:
#     def l_potential(pvec,R=1,k=1,epsilon = 0.5,l=l):
#         return parabola_potential(pvec,R,k,epsilon,l)
#     l_test = ABP(delta_test_dict,l_potential)
#     # l_test.r = (l_test.box_width/2)*np.ones((100,2))
#     folder_name = f"l_{l}"
#     l_test.generate_csv(100,folder_name)
#     a = Analysis(f"./data/{folder_name}",test_dict,1000)
#     anim = a.animate_movement_patch(sample_rate=10)
#     anim.save(f"media/l_{l}_anim.mp4")


##TESTING g(r) -radial distribution function 
# epsilon = 0.05
# k_2 = 1
# # folder_name = f"k_2_{k_2}_e_{epsilon}v2"
# folder_name = "l_-0.1"

# a = Analysis(f"./data/{folder_name}",test_dict,1000)
# print(a.r_data.shape)
# a.g_r(1)