from imports import *
from analysis import *
from parameter_dictionaries import pyABP_delta_dict

a = Analysis("./data/pyABP_delta_tests/k_1_epsilon_0.05_delta_0.12",pyABP_delta_dict,range(0,500),"pyABP")
plt.style.use("ggplot")
fig,ax = plt.subplots()
ax.set(xlabel="time units",ylabel="alpha length")
a.plot_alpha_length(ax)
plt.show()