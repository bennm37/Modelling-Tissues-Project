from imports import *
from analysis import *
from potentials import *
from parameter_dictionaries import *

a = Analysis("data/pyABP_delta_tests/k_1_epsilon_0.1_delta_0.0",pyABP_dict,range(1),"pyABP")
# sliders = a.parameter_potential_plot(repulsion_cohesion_potential,["k","epsilon"],slider_init=[1,0.15])
plt.style.use("ggplot")
fig,axs = plt.subplots(1,4)
fig.set_size_inches(11,3)
axs = axs.reshape(2,2)

epsilons = [0.1,0.2]
deltas = [0,0.24]
# fig.suptitle("Interaction Potentials")
# shift = 0.05
# l, b, w, h = axs[1,0].get_position().bounds
# axs[1,0].set_position([l,b-shift,w,h])
# l, b, w, h = axs[1,1].get_position().bounds
# axs[1,1].set_position([l,b-shift,w,h])
# axs[1,1].set_position(p2)
labels = np.array([["A","B"],["C","D"]])
for i,delt in enumerate(deltas):
    for j,ep in enumerate(epsilons):
        axs[i,j].set(title=f"{labels[i,j]}  $\epsilon$ = {ep}, $\delta$ = {delt}",xlabel = "$r_{ij}/b_{ij} $",ylabel="$F_{ij}$")
        # axs[i,j].yaxis.labelpad = -8
        # axs[i,j].xaxis.labelpad = -5
        sliders = a.plot_potential(axs[i,j],repulsion_cohesion_potential2,[1,ep,delt])
# sliders = a.parameter_potential_plot(repulsion_cohesion_potential2,["k","epsilon","delta"],[(0,2),(0,0.4),(0,0.7)],[1,0.15,0.1])
# plt.savefig("C:/Users/bennm/Documents/UNI/Year3/Non Code Project Stuff/potential2.svg")
plt.tight_layout()
plt.show()