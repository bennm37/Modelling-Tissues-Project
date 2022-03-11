from imports import *
from analysis import *
from potentials import *
from parameter_dictionaries import *

a = Analysis("data/pyABP_delta_tests/k_1_epsilon_0.1_delta_0.0",pyABP_dict,range(1),"pyABP")
# sliders = a.parameter_potential_plot(repulsion_cohesion_potential,["k","epsilon"],slider_init=[1,0.15])
plt.style.use("ggplot")
fig,ax = plt.subplots()
ax.set(title="Interaction Force",xlabel = "$r_{ij}$",ylabel="Force")
sliders = a.plot_potential(ax,repulsion_cohesion_potential,[1,0.15])
plt.show()