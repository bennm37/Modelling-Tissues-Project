from imports import *
from analysis import *
from parameter_dictionaries import pyABP_delta_dict


# plt.style.use("ggplot")
# folder_name = "high_poly_test/k_1_epsilon_0.2_delta_0.36"
# a = Analysis(f"data/{folder_name}",pyABP_delta_dict,range(500),"pyABP")
# ts = np.arange(100,500,20)
# drs,g_r = a.generate_g_r_data(ts)
# fig,ax = plt.subplots()
# ax.plot(drs,g_r)
# ax.set(xlabel="r",ylabel="g(r)",title = "Radial Distribution Function - ep 0.2,delta 0.36")
# plt.show()

# plt.style.use("ggplot")
# project = "pyABP_delta_tests"
# sg = pickle.load(open(f"data/{project}/search_grid.p","rb"))
# # epsilon = [0.05,0.1,0.15,0.2,0.25,0.3,0.35]
# # deltas = [0.0,0.12,0.24,0.36,0.48,0.6]
# epsilon = [0.2]
# for ep1 in epsilon:
#     # samples = [[0.0,ep1],[0.12,ep1],[0.24,ep1],[0.36,ep1],[0.48,ep1],[0.6,ep1]]
#     # samples = [[0.0,ep1],[0.12,ep1],[0.24,ep1],[0.36,ep1],[0.48,ep1]]
#     # samples = [[0.0,ep1],[0.12,ep1],[0.24,ep1],[0.36,ep1]]
#     samples = [[0.24,ep1]]
#     msv_data = np.zeros((6,500))
#     fig,ax = plt.subplots()
#     for i,s in enumerate(samples):
#         print(f"i={i},s={s}")
#         delta,ep = s
#         folder_name = f"k_1_epsilon_{ep}_delta_{delta}"
#         a = Analysis(f"data/{project}/{folder_name}",pyABP_delta_dict,range(500),"pyABP")
#         ts = np.arange(100,500,100)
#         drs,g_r = a.generate_g_r_data(ts)
#         ax.set(xlim=(2,4),ylim=(0,30))
#         ax.plot(drs,g_r,label = str(s))
#     ax.set(xlabel="r",ylabel="g(r)",title=f"RDF for epsilon = {ep1}")
#     ax.legend()
#     plt.show()
    # plt.savefig(f"media/pyABP_delta_tests/summary_plots/g(r)/g(r)_ep_{ep1}.pdf")



# for ep in epsilon:
#     for delt in deltas:
#         folder_name = f"pyABP_delta_tests\k_1_epsilon_{ep}_delta_{delt}"
#         a = Analysis(f"data\{folder_name}",pyABP_delta_dict,range(500),"pyABP")
#         ts = np.arange(100,500,20)
#         print(f"starting ep {ep} delta {delt}")
#         a.generate_g_r_data(ts,csv=f"data/{folder_name}/g(r)")

##SINGLE PLOT WITH PARTICLES
# a = Analysis("data\pyABP_delta_tests\k_1_epsilon_0.05_delta_0.0",pyABP_delta_dict,range(500),"pyABP")
# ts = np.arange(100,500,50)
# drs,g_r = a.generate_g_r_data(ts)
# plt.style.use("ggplot")
# fig,axs = plt.subplots(1,2)
# fig.set_size_inches(10,5)
# axs[0].set(xlim=(0,a.box_width*np.sqrt(2)/2))
# axs[0].plot(drs,g_r)
# a.plot_particles(axs[1],499)
# plt.show()


##TESTING NORMALISATION 
# a = Analysis("C:/Users/bennm/Documents/UNI/Year3/Modelling Tissues Project/data/pyABP_delta_tests/k_1_epsilon_0.15_delta_0.12",pyABP_delta_dict,range(500),"pyABP")
# a = Analysis("",pyABP_delta_dict,range(500),"pyABP")
# data = np.random.uniform(0,a.box_width,(500,a.N,2))
# a.r_data = data
# ts = np.arange(100,500,100)
# # print(ts)
# drs,g_r = a.generate_g_r_data(ts)
# # print(drs)
# # print(g_r)
# # drs,g_r = a.g_r(100)
# plt.style.use("ggplot")
# fig,axs = plt.subplots(2,1)
# fig.set_size_inches(5,10)
# fig.suptitle("Testing Normalisation")
# axs[0].set(xlim=(0,a.box_width*np.sqrt(2)/2),xlabel="$r$",ylabel="$g(r)$",title="RDF")
# axs[0].plot(drs,g_r)
# axs[1].scatter(data[499,:,0],data[499,:,1],s=5)
# axs[1].set(title="Uniformly Distributed Particles")
# plt.tight_layout()
# plt.savefig("C:/Users/bennm/Documents/UNI/Year3/Non Code Project Stuff/g_r_normalisation2.pdf")
