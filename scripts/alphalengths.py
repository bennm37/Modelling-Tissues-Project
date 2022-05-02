from numpy import average
from imports import *
from analysis import *
from parameter_dictionaries import pyABP_delta_dict
import matplotlib.cm as cm
import pickle 

plt.style.use("ggplot")


# project = "pyABP_delta_tests"
# sg = pickle.load(open(f"data/{project}/search_grid.p","rb"))

# k2 = [0.4,0.8,1.2,1.6,2]
# # epsilon = [0.05,0.1,0.15,0.2,0.25,0.3]
# epsilon = [0.35]
# # ep1 = 0.25
# # samples = [[0.12,ep1],[0.24,ep1],[0.36,ep1]]
# for ep1 in epsilon:
#     # samples = [[0.12,ep1],[0.24,ep1],[0.36,ep1],[0.48,ep1],[0.6,ep1]]
#     samples = [[0.12,ep1],[0.24,ep1],[0.36,ep1]]
#     msv_data = np.zeros((5,500))
#     fig,ax = plt.subplots()
#     for i,s in enumerate(samples):
#         print(f"i={i},s={s}")
#         delta,ep = s
#         # folder_name = f"pyABP_delta_{delta}_ep_{ep}"
#         folder_name = f"k_1_epsilon_{ep}_delta_{delta}"
#         a = Analysis(f"data/{project}/{folder_name}",pyABP_delta_dict,range(500),"pyABP")
#         ##STEADY STATE
#         a.plot_alpha_length(ax,label = f"{s}")


#     ax.set(xlabel="save no",ylabel="alpha length",title="Alpha Lengths of ABP")
#     ax.legend()
#     # plt.savefig(f"media/pyABP_delta_tests/summary_plots/alpha_lengths/al_ep_{ep1}.png")
#     plt.show()

##GRID 
plt.style.use("ggplot")
project = "pyABP_delta_tests"
sg = pickle.load(open(f"data/{project}/search_grid.p","rb"))
# eq_times = np.array([[None,None,None,None,None,None],[None,None,None,None,None,300],[None,None,200,100,100,100],[None,None,100,100,100,100],[None,100,100,100,100,None],[100,100,100,100,None,None],[100,100,100,None,None,None]])

epsilons = [0.05,0.1,0.15,0.2,0.25,0.3,0.35]
deltas = [0.0,0.12,0.24,0.36,0.48,0.6]
n_ep = len(epsilons)
n_delt = len(deltas)
eq_times = np.full((n_ep,n_delt),300)
eq_times[-1,-2:] = 0
eq_times[-2,-1] = 0
average_lengths = np.zeros((n_ep,n_delt))
average_num = np.zeros((n_ep,n_delt))
for i,ep in enumerate(epsilons):
    fig,ax = plt.subplots()
    num_lines = np.sum(eq_times[i]!=None)
    min = 2*ep
    max1 = 0.6+2*ep 
    cmap = cm.get_cmap("afmhot")
    max_eq = 0
    c = 0 
    for j,delta in enumerate(deltas):
        color = cmap(((delta+2*ep)-min)/max1)
        eq_time = eq_times[i,j]
        if eq_time:
            if eq_time >max_eq:
                max_eq = eq_time
            print(eq_time)
            folder_name = f"k_1_epsilon_{ep}_delta_{delta}"
            a = Analysis(f"data/{project}/{folder_name}",pyABP_delta_dict,range(500),"pyABP")
            lengths = a.load_alphalengths()
            length_sum = [sum(l) for l in lengths]
            length_n =  [len(l) for l in lengths]
            length_sum_eq = length_sum[eq_time:]
            length_n_eq = length_n[eq_time:]
            average_lengths[i,j] = np.mean(length_sum_eq)
            average_num[i,j] = np.mean(length_n_eq)
# pickle.dump(average_lengths,open("media/pyABP_delta_tests/summary_plots/alpha_lengths/average_lenths.p",'wb'))
pickle.dump(average_num,open("media/pyABP_delta_tests/summary_plots/alpha_lengths/num_shapes.p",'wb'))
print(average_num) 