import matplotlib
from sympy import O
from imports import *
from analysis import *
from parameter_dictionaries import pyABP_delta_dict
import matplotlib.cm as cm
import os 


##PLOT MANY 
plt.style.use("ggplot")
project = "pyABP_delta_tests"
sg = pickle.load(open(f"data/{project}/search_grid.p","rb"))
eq_times = np.array([[None,None,None,None,None,None],[None,None,None,None,None,300],[None,None,200,100,100,100],[None,None,100,100,100,100],[None,100,100,100,100,None],[100,100,100,100,None,None],[100,100,100,None,None,None]])
c1 = np.array([0,0.01,0.001,0.0006,0.0005,0.0005,0.0005])*5
c2 = np.array([0,0.01,0.003,0.002,0.003,0.003,0.003])*0.05
ylims = [(10**-2,10**2.5),(10**-2,10**2),(10**-2,10**2),(10**-2,10**1),(10**-2,10**1),(10**-2,10**1),(10**-2,10**1.5)]
epsilons = [0.05,0.1,0.15,0.20,0.25,0.3,0.35]
deltas = [0.0,0.12,0.24,0.36,0.48,0.6]
for i,ep in enumerate(epsilons):
    fig,ax = plt.subplots()
    num_lines = np.sum(eq_times[i]!=None)
    min1 = 2*ep
    max1 = 0.6+2*ep 
    cmap = cm.get_cmap("afmhot")
    max_eq = 0
    c = 0 
    for j,delta in enumerate(deltas):
        color = cmap(((delta+2*ep)-min1)/max1)
        eq_time = eq_times[i,j]
        if eq_time:
            if eq_time >max_eq:
                max_eq = eq_time
            file_name = f"data/pyABP_delta_tests/k_1_epsilon_{ep}_delta_{delta}/msd"
            print(f"starting ep {ep} delta {delta}, eq_time {eq_time}")
            df = pd.read_csv(file_name+"/msd_com.csv")
            m = df["m"]
            msd = df["msd"]
            # ax.set(xlim=(0,5000))
            ax.loglog(m*10-eq_time*10,msd,label = f"[{ep},{delta}]",color=color)
            # ax.plot(m*10-eq_time*10,msd,label = f"[{ep},{delta}]",color=color)
    t1 = np.logspace(-10,4,200)
    ax.loglog(t1,c1[i]*t1,"k--")
    ax.loglog(t1,c2[i]*(t1)**2,"k--")
    ax.set(xlabel="t",ylabel="msd",title=f"MSD for epsilon = {ep}",xlim=(10,min(5000-max_eq*10,2000)),ylim=ylims[i])
    ax.legend()
    # plt.show()
    plt.savefig(f"media/pyABP_delta_tests/summary_plots/msd/msd_ep_colors_{ep}.pdf")


##PLOT SINGLE 
# ep = 0.3
# delta = 0.12
# eq_time = 100
# file_name = f"data/pyABP_delta_tests/k_1_epsilon_{ep}_delta_{delta}/msd"
# print(f"starting ep {ep} delta {delta}, eq_time {eq_time}")
# df = pd.read_csv(file_name+"/msd.csv")
# m = df["m"]
# msd = df["msd"]
# # ax.set(xlim=(0,5000))
# plt.style.use("ggplot")
# fig,ax = plt.subplots()
# ax.loglog(m*10,msd,label = f"[{ep},{delta}]",color="k")
# plt.show()

#CREATING DATA
eq_times = np.array([[None,None,None,None,None,None],[None,None,None,None,None,300],[None,None,200,100,100,100],[None,None,100,100,100,100],[None,100,100,100,100,100],[100,100,100,100,None,None],[100,100,100,None,None,None]])
# epsilons = [0.3]
# deltas = [0.12]
# epsilons = [0.05,0.1,0.15,0.2,0.25,0.3,0.35]
# deltas = [0.0,0.12,0.24,0.36,0.48,0.6]
# for i,ep in enumerate(epsilons):
#     for j,delt in enumerate(deltas):
#         eq_time = eq_times[i,j]
#         if eq_time:
#             folder_name = f"pyABP_delta_tests/k_1_epsilon_{ep}_delta_{delt}"
#             a = Analysis(f"data/{folder_name}",pyABP_delta_dict,range(eq_time,500),"pyABP")
#             print(f"starting ep {ep} delta {delt}, eq_time {eq_time}")
#             msd_data = a.generate_msd_data(csv=f"data/{folder_name}/msd")

##TESTING r_com
# ep,delt = 0.3,0.12
# eq_time = 300
# folder_name = f"pyABP_delta_tests/k_1_epsilon_{ep}_delta_{delt}"
# a = Analysis(f"data/{folder_name}",pyABP_delta_dict,range(eq_time,500),"pyABP")
# r = a.r_data
# r_com = r-np.mean(r,axis=1)[:,np.newaxis,:]
# com = np.mean(r,axis=1)
# n = com.shape[0]
# scomd = np.zeros(n)
# for i in range(n):
#     scomd[i] = np.sum((com[i]-com[0])**2)
# fig,ax = plt.subplots()
# ax.plot(scomd)
# plt.show()

# fig,ax = plt.subplots()
# ax.plot(com[:,0],com[:,1])
# plt.show()
# print(r_com[0].shape)
# com_com = np.mean(r_com[0],axis=0)
# print(com_com)
# print(np.allclose(com_com,np.zeros(com_com.shape)))

##ADJUSTING TO START AT EQ TIMES
# eq_times = np.array([[None,None,None,None,None,None],[None,None,None,None,None,300],[None,None,200,100,100,100],[None,None,100,100,100,100],[None,100,100,100,100,100],[100,100,100,100,None,None],[100,100,100,None,None,None]])
# epsilons = [0.05,0.1,0.15,0.2,0.25,0.3,0.35]
# deltas = [0.0,0.12,0.24,0.36,0.48,0.6]
# epsilons = [0.1]
# deltas = [0.6]
# for i,ep in enumerate(epsilons):
#     for j,delt in enumerate(deltas):
#         eq_time = eq_times[i,j]
#         if eq_time:
#             file_name = f"data/pyABP_delta_tests/k_1_epsilon_{ep}_delta_{delt}/msd"
#             print(f"starting ep {ep} delta {delt}, eq_time {eq_time}")
#             df = pd.read_csv(file_name+"/msd.csv")
#             df["m"] = np.array(df["m"])-eq_time
#             if os.path.exists(file_name+"/msd2.csv"):
#                 print("path exists")
#                 os.remove(file_name+"/msd.csv")
#             df.to_csv(file_name+"/msd.csv",index=False)
