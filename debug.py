from matplotlib.cbook import delete_masked_points
from abp import * 
from analysis import *
##TODO find better way of importing to avoid cluttering namespace
from parameter_dictionaries import *
from simulation import *
import os

# n_delta,n_ep = 6,6
# delta_range,ep_range  = (0,0.6),(0.05,0.35)
n_delta,n_ep = 1,1
delta_range,ep_range  = (0.36,0.36),(0.2,0.2)
epsilon,delta = make_param_lists(ep_range,delta_range,n_ep,n_delta)
sg = make_search_grid(["epsilon","delta"],[epsilon,delta],True)
# simulation("delta_tests",delta_test_dict,repulsion_cohesion_potential2,sg)
# delete_project("pyABP_delta_tests")
# while not os.listdir("data/pyABP_delta_tests/k_1_epsilon_0.25_delta_0.5/rvd_data"):
#     pass
# simulation("pyABP_delta_tests",pyABP_dict,repulsion_cohesion_potential2,sg,"pyABP",stats=["g(r)","anim"])
pyABP_delta_dict["T"] = 500000
pyABP_delta_dict["box_width"] = 200
# sg = [list(l) for l in sg]
simulation("high_poly_test",pyABP_delta_dict,repulsion_cohesion_potential2,sg,"pyABP",stats=[])

##TESTING NEW PLOTTING
# parameters = pyABP_dict
# k,k2,epsilon = 1,0.8,0.05
# # folder_name = f"pyABP_k2_tests/pyABP_k2_{k2}_epsilon_{epsilon}"
# folder_name = f"pyABP_k2_tests/pyABP_k2_{k2}_ep_{epsilon}"
# n_saves = parameters["T"]//100
# save_range = range(90,91)
# a = Analysis("data/" +folder_name,parameters,save_range,data_type="pyABP")
# as_folder_name = f"./data/alpha_shapes/pyABP_k2_tests/k2_{k2}_ep_{epsilon}"
# frame_no = 90

# ##PLOTTING
# fig,axs = plt.subplots(2,2)
# a.plot_particles(axs[0,0],0)
# a.plot_potential(axs[0,1],parabola_potential,[1,0.15,-0.5])
# plot_g_r(a,2,0.15,axs[1,0])
# a.plot_alphashape(axs[1,1],as_folder_name,frame_no,True)
# plt.show()

##CENTRE TEST PACKING FRACTION 1
# k2s = [0.4,0.8,1.2,1.6,2]
# epsilons = [0.05,0.1,0.15,0.2,0.25,0.3] 
# for k2 in k2s:
#     for epsilon in epsilons:
#         # folder_name = circle_test_setup(k2_potential,[1,k2,epsilon],k2_test_dict)
#         a = Analysis(f"./data/pyABP_k2_tests/pyABP_k2_{k2}_ep_{epsilon}",pyABP_dict,range(100),data_type="pyABP")
#         dr,nf,ax = a.g_r(50,csv=f"k2_{k2}_epsilon_{epsilon}")
# circle_test_setup(potential = k2_potential,potential_parameters= [1,1,0.15],parameters = k2_test_dict)

##TESTING PYABP CODE
# folder_name = "pyABP_k2_1_ep_0.15"
# a = Analysis(f"./data/{folder_name}",pyABP_dict,range(100),data_type="pyABP")
# anim = a.animate_movement_patch(1)
# anim.save(f"./media/{folder_name}.mp4")

##TESTING g(r) -radial distribution function 
# epsilon = 0.05
# k2 = 1
# folder_name = "./data/k2_test_k_1_k2_1_epsilon_0.15"

# a = Analysis(folder_name,test_dict,range(1000))
# # # ,csv="k2_1_epsilon_0.15")
# drs,nf = a.g_r(999,dr=0.01,csv="k2_1_epsilon_0.15")


# "data/delta_tests/k_1_epsilon_0.05_delta_0.4/rvd_data"
# "data/delta_tests/k_1_epsilon_0.05_delta_0.4/rvd_data"