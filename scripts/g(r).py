from imports import *
from analysis import *
from parameter_dictionaries import pyABP_delta_dict


plt.style.use("ggplot")
project = "pyABP_delta_tests"
sg = pickle.load(open(f"data/{project}/search_grid.p","rb"))
k2 = [0.4,0.8,1.2,1.6,2]
# epsilon = [0.05,0.1,0.15,0.2,0.25]
epsilon = [0.35]
for ep1 in epsilon:
    # samples = [[0.0,ep1],[0.12,ep1],[0.24,ep1],[0.36,ep1],[0.48,ep1],[0.6,ep1]]
    # samples = [[0.0,ep1],[0.12,ep1],[0.24,ep1],[0.36,ep1],[0.48,ep1]]
    samples = [[0.0,ep1],[0.12,ep1],[0.24,ep1],[0.36,ep1]]
    msv_data = np.zeros((6,500))
    fig,ax = plt.subplots()
    for i,s in enumerate(samples):
        print(f"i={i},s={s}")
        delta,ep = s
        folder_name = f"k_1_epsilon_{ep}_delta_{delta}"
        a = Analysis(f"data/{project}/{folder_name}",pyABP_delta_dict,range(500),"pyABP")
        ts = np.arange(100,500,20)
        drs,g_r = a.generate_g_r_data(ts)
        ax.set(xlim=(0,10),ylim=(0,30))
        ax.plot(drs,g_r,label = str(s))
    ax.set(xlabel="r",ylabel="g(r)",title=f"RDF for epsilon = {ep1}")
    ax.legend()
    plt.savefig(f"media/pyABP_delta_tests/summary_plots/g(r)/g(r)_ep_{ep1}.pdf")

a = Analysis("data\pyABP_delta_tests\k_1_epsilon_0.3_delta_0.36",pyABP_delta_dict,range(500),"pyABP")


##SINGLE PLOT WITH PARTICLES
# a = Analysis("data\pyABP_delta_tests\k_1_epsilon_0.3_delta_0.36",pyABP_delta_dict,range(500),"pyABP")
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
# a = Analysis("",pyABP_delta_dict,range(500),"pyABP")
# data = np.random.uniform(0,a.box_width,(500,a.N,2))
# a.r_data = data
# ts = np.arange(100,500,100)
# # print(ts)
# drs,g_r = a.generate_g_r_data(ts)
# # drs,g_r = a.g_r(100)
# plt.style.use("ggplot")
# fig,axs = plt.subplots(1,2)
# fig.set_size_inches(10,5)
# axs[0].set(xlim=(0,a.box_width*np.sqrt(2)/2))
# axs[0].plot(drs,g_r)
# axs[1].scatter(data[499,:,0],data[499,:,1],s=5)
# plt.show()
