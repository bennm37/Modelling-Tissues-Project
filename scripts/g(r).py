from imports import *
from analysis import *
from parameter_dictionaries import pyABP_delta_dict

a = Analysis("data/pyABP_delta_tests/k_1_epsilon_0._delta_0.0",pyABP_delta_dict,range(500),"pyABP")
ts = np.arange(100,500,20)
# print(ts)
drs,g_r = a.generate_g_r_data(ts)
plt.style.use("ggplot")
fig,ax = plt.subplots()
ax.set(xlim=(0,8))
ax.plot(drs,g_r)
plt.show()