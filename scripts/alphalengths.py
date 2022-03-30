from imports import *
from analysis import *
from parameter_dictionaries import pyABP_delta_dict

plt.style.use("ggplot")


project = "pyABP_delta_tests"
sg = pickle.load(open(f"data/{project}/search_grid.p","rb"))

k2 = [0.4,0.8,1.2,1.6,2]
# epsilon = [0.05,0.1,0.15,0.2,0.25,0.3]
epsilon = [0.35]
# ep1 = 0.25
# samples = [[0.12,ep1],[0.24,ep1],[0.36,ep1]]
for ep1 in epsilon:
    # samples = [[0.12,ep1],[0.24,ep1],[0.36,ep1],[0.48,ep1],[0.6,ep1]]
    samples = [[0.12,ep1],[0.24,ep1],[0.36,ep1]]
    msv_data = np.zeros((5,500))
    fig,ax = plt.subplots()
    for i,s in enumerate(samples):
        print(f"i={i},s={s}")
        delta,ep = s
        # folder_name = f"pyABP_delta_{delta}_ep_{ep}"
        folder_name = f"k_1_epsilon_{ep}_delta_{delta}"
        a = Analysis(f"data/{project}/{folder_name}",pyABP_delta_dict,range(500),"pyABP")
        a.plot_alpha_length(ax,label = f"{s}")
    ax.set(xlabel="save no",ylabel="alpha length",title="Alpha Lengths of ABP")
    ax.legend()
    plt.savefig(f"media/pyABP_delta_tests/summary_plots/alpha_lengths/al_ep_{ep1}.png")