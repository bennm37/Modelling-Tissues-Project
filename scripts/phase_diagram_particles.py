from cv2 import phase
from matplotlib.pyplot import xlabel
from imports import *
from abp import *
from analysis import *
from parameter_dictionaries import *
from potentials import *
import matplotlib as mpl
from matplotlib.ticker import NullLocator
import matplotlib.cm as cm

plt.style.use("ggplot")
project = "pyABP_delta_tests"
##viridis is nice
cmap = cm.get_cmap("viridis",lut=4)
# epsilons = [0.05,0.1]
# deltas = [0.0,0.12]
phase_diagram = np.array(pd.read_csv(f"data/{project}/phase_diagram.csv"))
# epsilons = [0.05,0.1,0.15,0.2,0.25,0.3,0.35]
# deltas = [0.0,0.12,0.24,0.36,0.48,0.6]
epsilons = [0.1,0.3]
deltas = [0.12,0.48]
cols = np.array([[1,0],[3,2]])
n_ep,n_delt = len(epsilons),len(deltas)
fig,axs = plt.subplots(n_ep,n_delt)
for i,ep in enumerate(epsilons[::-1]):
    for j,delt in enumerate(deltas):
        print(f"starting ep {ep}, delt {delt}")
        folder_name = f"k_1_epsilon_{ep}_delta_{delt}"
        a = Analysis(f"data/{project}/{folder_name}",pyABP_delta_dict,range(499,500),"pyABP")
        r = a.r_data[0]
        axs[i,j].axis("equal")
        color = cmap(cols[i,j])
        axs[i,j].scatter(r[:,0],r[:,1],s=0.1,color=color)
        axs[i,j].axes.xaxis.set_visible(False)
        axs[i,j].axes.yaxis.set_visible(False)
        axs[i,j].set(ylim=(0,200))
cbar = fig.colorbar(cm.ScalarMappable(norm= mpl.colors.Normalize(0,4), cmap=cmap), ax=axs[:,:])
cbar.set_ticks([])
ax_delt = plt.axes([0.17, 0.1, 0.53, 0])
ax_delt.set(xlabel="$\delta$",xlim=(0,0.6))
ax_delt.set_xticks(deltas)
ax_ep = plt.axes([0.1,0.15, 0,0.68])
ax_ep.set(ylabel="$\epsilon$",ylim=(0.05,0.35))
ax_delt.set_yticks(epsilons)

# plt.tight_layout()
plt.show()