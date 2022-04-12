import matplotlib
from sympy import O
from imports import *
from analysis import *
from parameter_dictionaries import pyABP_delta_dict
import matplotlib.cm as cm
import os 



plt.style.use("ggplot")
project = "pyABP_delta_tests"
sg = pickle.load(open(f"data/{project}/search_grid.p","rb"))
eq_times = np.array([[None,None,None,None,None,None],[None,None,None,None,None,300],[None,None,200,100,100,100],[None,None,100,100,100,100],[None,100,100,100,100,None],[100,100,100,100,None,None],[100,100,100,None,None,None]])
epsilons = [0.05,0.1,0.15,0.2,0.25,0.3,0.35]
deltas = [0.0,0.12,0.24,0.36,0.48,0.6]
for i,ep in enumerate(epsilons):
    fig,ax = plt.subplots()
    num_lines = np.sum(eq_times[i]!=None)
    min = 2*ep
    max = 0.6+2*ep 
    cmap = cm.get_cmap("summer")
    for j,delta in enumerate(deltas):
        color = cmap(((delta+2*ep)-min)/max)
        eq_time = eq_times[i,j]
        if eq_time:
            file_name = f"data/pyABP_delta_tests/k_1_epsilon_{ep}_delta_{delta}/msd"
            print(f"starting ep {ep} delta {delta}, eq_time {eq_time}")
            df = pd.read_csv(file_name+"/msd.csv")
            m = df["m"]
            msd = df["msd"]
            ax.set(xlim=(0,500))
            ax.plot(m,msd,label = f"[{ep},{delta}]",color=color)
    ax.set(xlabel="t",ylabel="msd",title=f"MSD for epsilon = {ep}")
    ax.legend()
    plt.show()
    plt.savefig(f"media/pyABP_delta_tests/summary_plots/msd/msd_ep_{ep}.pdf")

##CREATING DATA
# eq_times = np.array([[None,None,None,None,None,None],[None,None,None,None,None,300],[None,None,200,100,100,100],[None,None,100,100,100,100],[None,100,100,100,100,100],[100,100,100,100,None,None],[100,100,100,None,None,None]])
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

##ADJUSTING TO START AT EQ TIMES
# eq_times = np.array([[None,None,None,None,None,None],[None,None,None,None,None,300],[None,None,200,100,100,100],[None,None,100,100,100,100],[None,100,100,100,100,100],[100,100,100,100,None,None],[100,100,100,None,None,None]])
# epsilons = [0.05,0.1,0.15,0.2,0.25,0.3,0.35]
# deltas = [0.0,0.12,0.24,0.36,0.48,0.6]
# # epsilons = [0.1]
# # deltas = [0.6]
# for i,ep in enumerate(epsilons):
#     for j,delt in enumerate(deltas):
#         eq_time = eq_times[i,j]
#         if eq_time:
#             file_name = f"data/pyABP_delta_tests/k_1_epsilon_{ep}_delta_{delt}/msd"
#             print(f"starting ep {ep} delta {delt}, eq_time {eq_time}")
#             df = pd.read_csv(file_name+"/msd.csv")
#             df["m"] = np.array(df["m"])+eq_time
#             if os.path.exists(file_name+"/msd2.csv"):
#                 print("path exists")
#                 os.remove(file_name+"/msd.csv")
#                 os.remove(file_name+"/msd2.csv")
#             df.to_csv(file_name+"/msd.csv",index=False)
