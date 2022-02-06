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
fig.set_size_inches(14,7)
gs = GridSpec(2,4)
ax0 = fig.add_subplot(gs[0,0])
ax1 = fig.add_subplot(gs[0,1])
ax2 = fig.add_subplot(gs[1,0])
ax3 = fig.add_subplot(gs[1,1])
ax4 = fig.add_subplot(gs[0:2,2:4])

#titles 
ax0.set(title = "Phase Diagram")
ax1.set(title = "k2 Force")
ax2.set(title = "Alpha Shape of Particles")
ax4.set(title = "Particles at 500000 time steps")
ax3.set(title="Radial Distribution Function")
ax2.axis("equal")
ax4.axis("equal")

##setting up phase diagram
n_k2 = 4
n_ep = 6
k2_range = (0.4,2)
ep_range = (0.05,0.35)
k2_int = (k2_range[1]-k2_range[0])/n_k2
ep_int = (ep_range[1]-ep_range[0])/n_ep
k2 = np.linspace(k2_range[0],k2_range[1],n_k2+1)
epsilon = np.linspace(ep_range[0],ep_range[1],n_ep+1)
ax0.set_xticks(k2)

ax0.set_yticks(epsilon)
ax0.grid(which="both")
ax0.set(xlim=k2_range,ylim=ep_range)
phases = np.linspace(0,5,6)
##creating and saving random phase diagram
# phase_diagram = np.random.choice(phases,(n_ep+1,n_k2+1))
# cols = [f"col{i}" for i in range(n_k2+1)]
# df = pd.DataFrame(phase_diagram,columns=cols)
# df.to_csv("data/phase_diagram.csv",index=False)
phase_diagram = pd.read_csv("data/phase_diagram.csv")
ax0.pcolormesh(k2,epsilon,phase_diagram,shading="flat")

##initial subplots
data_type = "pyABP"
k2_init = 0.4
ep_init = 0.1
plot_potential(k2_potential,[1,k2_init,ep_init],ax=ax1)
def plot_particles(k2,epsilon,frame_no,ax,p_dict = k2_test_dict,data_type= "ben"):
    ax.set(title = f"Particles at {frame_no}0000 dt")
    N = p_dict["N"]
    if data_type == "ben":
        folder_name = "./data/k2_tests/"
        try:
            data = pd.read_csv(folder_name +f"k2_test_k_1_k2_{k2}_epsilon_{epsilon}/data_{frame_no}.csv")
            r_data = np.array(data[["x1","x2"]]).reshape(N,2)
            v_data = np.array(data[["v1","v2"]]).reshape(N,2)
            d_data = np.array(data[["d1","d2"]]).reshape(N,2)
        except FileNotFoundError:
            ax.clear()
            return 1
    if data_type== "pyABP":
        try:
            folder_name = f"./data/pyABP_k2_tests/pyABP_k2_{k2}_ep_{epsilon}"
            dat_content = [i.strip().split() for i in open(f"{folder_name}/data{frame_no}.dat")]
            columns = dat_content[0]
            data = np.array(dat_content[1:])
            df = pd.DataFrame(data.reshape(N,8),columns=columns)
            r_data = np.array(df[["x","y"]]).reshape(N,2).astype(np.float64)
            r_data += p_dict["box_width"]/2
            v_data = np.array(df[["vx","vy"]]).reshape(N,2).astype(np.float64)
            theta_data = np.array(df["theta"]).reshape(N,1).astype(np.float64)
            d_data = np.append(np.cos(theta_data),np.sin(theta_data),axis = 1)
        except FileNotFoundError:
            ax.clear()
            return 1

    asp = [15,15,2,7.5,1]
    ax.set(xlim=(0,p_dict["box_width"]),ylim=(0,p_dict["box_width"]))
    directions = ax.quiver(r_data[:,0],r_data[:,1],d_data[:,0],d_data[:,1])
    velocities = ax.quiver(r_data[:,0],r_data[:,1],v_data[:,0],v_data[:,1],color="r",
        headaxislength=asp[0],headlength=asp[1],scale=asp[2],headwidth=asp[3],minshaft=asp[4])
    for cell in r_data[:,:]:
        c = Ellipse(cell,2,2,fill=False,color="k")
        p = ax.add_patch(c)
    return 0

def plot_g_r(k2,epsilon,frame_no,ax,data_type="ben"):
    try:
        if data_type =="ben":
            df = pd.read_csv(f"./data/g_r/N100_k2_centretests/k2_{k2}_epsilon_{epsilon}")
        if data_type == "pyABP":
            df = pd.read(f"./data/g_r/pyABP_k2/k2_{k2}_epsilon_{epsilon}")
        r = df["r"]
        g_r = df["g(r)"]
        ax.plot(r,g_r)
        ax.set(title = "Radial Distribution Function")
        return 0
    except FileNotFoundError:
        ax.set(title = f"No Data for k2 = {k2},ep ={epsilon}")
        return 0
ret = plot_particles(k2_init,ep_init,50,ax2,p_dict = pyABP_dict,data_type=data_type)
ret = plot_particles(k2_init,ep_init,50,ax4,p_dict = pyABP_dict,data_type=data_type)
plot_g_r(k2_init,ep_init,50,ax3,data_type=data_type)

def onclick(event):
    epsilon = event.ydata
    k2 = event.xdata
    if k2==None or epsilon ==None :
        pass
    elif k2>k2_range[1] or k2<k2_range[0]:
        pass
    elif epsilon>ep_range[1] or epsilon<ep_range[0]:
        pass
    ##roudning k2,epsilon to nearest values
    else:
        rounded_k2 = round((k2//k2_int)*k2_int,2)
        rounded_epsilon = round((epsilon//ep_int)*ep_int,2)
        if rounded_k2%1 ==0 :
            rounded_k2 = int(rounded_k2)
        if rounded_epsilon%1 ==0 :
            rounded_epsilon = int(rounded_epsilon)
        print(f"rounding rounded_k2/k1 = {rounded_k2}, rounded_epsilon = {rounded_epsilon}")
        ax1.clear()
        ax2.clear()
        ax3.clear()
        ax4.clear()
        ax1.set(title = "K2 Force")
        p1,nax1 = plot_potential(k2_potential,[1,rounded_k2,rounded_epsilon],ax=ax1)
        ret = plot_particles(rounded_k2,rounded_epsilon,50,ax2,p_dict = pyABP_dict,data_type=data_type)
        ret = plot_particles(rounded_k2,rounded_epsilon,50,ax4,p_dict = pyABP_dict,data_type=data_type)
        if ret:
            fig.suptitle(f"No data for K2 = {rounded_k2},epsilon = {rounded_epsilon}")
        else:
            fig.suptitle(f"K2 = {rounded_k2}, Epsilon = {rounded_epsilon}")
        ret3 = plot_g_r(rounded_k2,rounded_epsilon,50,ax3)
        fig.canvas.draw_idle()

cid = fig.canvas.mpl_connect('button_press_event', onclick)
plt.show()