from cv2 import phase
from matplotlib.pyplot import grid, title
from numpy import False_
from abp import *
from analysis import *
from parameter_dictionaries import *
from potentials import *
from matplotlib.gridspec import GridSpec
from plotting_potentials import plot_potential

##setting up figure/axes
fig = plt.figure()
fig.set_size_inches(7,7)
gs = GridSpec(2,2)
ax0 = fig.add_subplot(gs[0,0])
ax1 = fig.add_subplot(gs[0,1])
ax2 = fig.add_subplot(gs[1,0])
ax3 = fig.add_subplot(gs[1,1])

#titles 
ax0.set(title = "Phase Diagram")
ax1.set(title = "k2 Force")
ax2.set(title = "Particles at 500000 time steps")
ax3.set(title="Radial Distribution Function")
ax2.axis("equal")

##setting up phase diagram
n_k2 = 5
n_ep = 6
k2_range = (0,2)
ep_range = (0,0.3)
k2_int = (k2_range[1]-k2_range[0])/n_k2
ep_int = (ep_range[1]-ep_range[0])/n_ep
k2 = np.linspace(k2_range[0],k2_range[1],n_k2+1)
epsilon = np.linspace(ep_range[0],ep_range[1],n_ep+1)
ax0.set_xticks(k2)
ax0.set_yticks(epsilon)
ax0.grid(which="both")
ax0.set(xlim=k2_range,ylim=ep_range)
phases = np.linspace(0,5,6)
phase_diagram = np.random.choice(phases,(n_ep+1,n_k2+1))
cols = [f"col{i}" for i in range(n_ep)]
df = pd.DataFrame(phase_diagram,columns=cols)
df.to_csv("data/phase_diagram.csv",index=False)
phase_diagram = pd.read_csv("data/phase_diagram.csv")
ax0.pcolormesh(k2,epsilon,phase_diagram,shading="flat")

##initial subplots
plot_potential(k2_potential,[1,1,0.15],ax=ax1)
def plot_particles(k2,epsilon,frame_no,ax,p_dict = k2_test_dict):
    ax.set(title = f"Particles at {frame_no}0000 dt")
    N = p_dict["N"]
    folder_name = "./data/k2_tests_halfepsilon/"
    try:
        data = pd.read_csv(folder_name +f"k2_test_k_1_k2_{k2}_epsilon_{epsilon}/data_{frame_no}.csv")
    except FileNotFoundError:
        ax.clear()
        return 1
    r_data = np.array(data[["x1","x2"]]).reshape(N,2)
    v_data = np.array(data[["v1","v2"]]).reshape(N,2)
    d_data = np.array(data[["d1","d2"]]).reshape(N,2)
    asp = [10,10,15]
    ax.set(xlim=(0,p_dict["box_width"]),ylim=(0,p_dict["box_width"]))
    directions = ax.quiver(r_data[:,0],r_data[:,1],d_data[:,0],d_data[:,1],
        headaxislength=asp[0],headlength=asp[1],scale=asp[2])
    velocities = ax.quiver(r_data[:,0],r_data[:,1],v_data[:,0],v_data[:,1],color="r",
        headaxislength=asp[0],headlength=asp[1],scale=asp[2])
    for cell in r_data[:,:]:
        c = Ellipse(cell,2,2,fill=False,color="k")
        p = ax.add_patch(c)
    return 0
ret = plot_particles(1,0.15,50,ax2)

def onclick(event):
    epsilon = event.ydata
    k2 = event.xdata
    ##roudning k2,epsilon to nearest values
    rounded_k2 = round((k2//k2_int)*k2_int,2)
    rounded_epsilon = round((epsilon//ep_int)*ep_int,2)
    if rounded_k2%1 ==0 :
        rounded_k2 = int(rounded_k2)
    if rounded_epsilon%1 ==0 :
        rounded_epsilon = int(rounded_epsilon)
    print(f"rounding rounded_k2/k1 = {rounded_k2}, rounded_epsilon = {rounded_epsilon}")
    ax1.clear()
    ax2.clear()
    ax1.set(title = "K2 Force")
    p1,nax1 = plot_potential(k2_potential,[1,rounded_k2,rounded_epsilon],ax=ax1)
    ret = plot_particles(rounded_k2,rounded_epsilon,50,ax2)
    if ret:
        fig.suptitle(f"No data for K2 = {rounded_k2},epsilon = {rounded_epsilon}")
    else:
        fig.suptitle(f"K2 = {rounded_k2}, Epsilon = {rounded_epsilon}")
    fig.canvas.draw_idle()

cid = fig.canvas.mpl_connect('button_press_event', onclick)
plt.show()