from abp import *

abp_100 = ABP(100)
T = 1000
f_name = abp_100.generate_csv(T,0.01)
p_dict = abp_100.get_parameter_dictionary()
f_name = "./data/"+f_name
analysis_100 = Analysis(f_name,p_dict,T,0.1)
msd_data = analysis_100.generate_msd_data(np.array((0,T)))
fig,ax = plt.subplots()
ax.plot(msd_data)
plt.show()