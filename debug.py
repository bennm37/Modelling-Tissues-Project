from cv2 import circle
from abp import * 
from analysis import Analysis
from circle_test import circle_test, circle_test_setup
from potentials import k2_potential
##TODO find better way of importing to avoid cluttering namespace
from parameter_dictionaries import *


##CENTRE TEST PACKING FRACTION 1
k2s = [0.4,0.8,1.2,1.6,2]
epsilons = [0.05,0.1,0.15,0.2,0.25,0.3] 
for k2 in k2s:
    for epsilon in epsilons:
        folder_name = circle_test_setup(k2_potential,[1,k2,epsilon],k2_test_dict)
# circle_test_setup(potential = k2_potential,potential_parameters= [1,1,0.15],parameters = k2_test_dict)

# def plot_cells(ax):
#     start_radius = 10
#     bw = box_width_from_phi(100,0.3)
#     ax.set(xlim=(0,bw),ylim=(0,bw))
#     np.random.seed(seed = 1915069)
#     thetas = np.random.uniform(0,2*np.pi,N)
#     radii = np.sqrt(np.random.uniform(0,start_radius**2,N))
#     rs = np.transpose([radii*np.cos(thetas),radii*np.sin(thetas)])+np.full((N,2),bw/2)
#     for cell in rs[:,:]:
#         c = Ellipse(cell,2,2,fill=False,color="k")
#         p = ax.add_patch(c)
    
# fig,ax = plt.subplots()
# ax1 = plot_cells(ax)
# plt.show()

##TESTING g(r) -radial distribution function 
# epsilon = 0.05
# k2 = 1
# folder_name = "./data/k2_test_k_1_k2_1_epsilon_0.15"

# a = Analysis(folder_name,test_dict,1000)
# # # ,csv="k2_1_epsilon_0.15")
# drs,nf = a.g_r(999,dr=0.01,csv="k2_1_epsilon_0.15")


