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

##DATA GENERATION
# glass = ABP(glass_dict,repulsion_cohesion_potential)
# glass.generate_csv(100000,0.01,100)
# dense_liquid = ABP(dense_liquid_dict,repulsion_cohesion_potential)
# dense_liquid.generate_csv(100000,0.01,100)
# phase_seperated = ABP(phase_seperated_dict,repulsion_cohesion_potential)
# phase_seperated.generate_csv(100000,0.01,100)
# normal_liquid = ABP(normal_liquid_dict,repulsion_cohesion_potential)
# normal_liquid.generate_csv(100000,0.01,100)

test = ABP (test_dict,parabola_potential)
test.generate_csv(100,"parabola_potential_data")
a = Analysis("./data/parabola_potential_data",test_dict,1000)
anim = a.animate_movement_patch(sample_rate=10)
plt.show()

##plotting_potentials
# def plot_potential(potential):
#     num_samples = 100
#     R = np.ones(1)
#     data = np.zeros((num_samples))
#     X = np.linspace(0,20,num_samples)
#     for i,x in enumerate(X):
#         pvec = np.array([[[x,0]]])
#         data[i] = potential(pvec,R)[0,0]
#     plt.plot(X,data)
# plot_potential(parabola_potential)
# plt.show()
