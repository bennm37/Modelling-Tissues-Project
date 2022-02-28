from abp import *
from analysis import *
from parameter_dictionaries import *
from potentials import *
from matplotlib.gridspec import GridSpec
from simulation import get_parameter_suffix,make_param_lists


data_type = "ben"
project_name = "delta_tests"
frame_no = 99

##setting up figure/axes
plt.style.use('ggplot')
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
ax4.set(title = f"Particles at {frame_no}000 time steps")
ax3.set(title="Radial Distribution Function")
ax2.axis("equal")
ax4.axis("equal")
##setting up phase diagram

n_k2,n_ep = 6,7
k2_range,ep_range  = (0,0.6),(0,0.35)
k2_int,ep_int = (k2_range[1]-k2_range[0])/(n_k2),(ep_range[1]-ep_range[0])/(n_ep)
epsilon,k2 = make_param_lists(ep_range,k2_range,n_ep,n_k2)
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
phase_diagram = pd.read_csv(f"data/{project_name}/phase_diagram.csv")
ax0.pcolormesh(k2,epsilon,phase_diagram,shading="flat")

##initial subplots
p_dict = delta_test_dict
k2_init = 0.4
ep_init = 0.1
potential_dict = {"k":1,"epsilon":ep_init,"delta":k2_init}
data_name = f"data/{project_name}/{get_parameter_suffix(potential_dict)}"
save_range = range(frame_no,frame_no+1)
a = Analysis(data_name,p_dict,save_range,data_type=data_type)
a.plot_potential(ax1,k2_potential,[1,k2_init,ep_init])
a.plot_g_r(ax2,1)
# a.plot_alphashape(ax=ax3,frame_no=frame_no,single = True)
a.plot_particles(ax4,0)
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
            rounded_k2 = float(rounded_k2)
        if rounded_epsilon%1 ==0 :
            rounded_epsilon = float(rounded_epsilon)
        print(f"rounding rounded_k2/k1 = {rounded_k2}, rounded_epsilon = {rounded_epsilon}")
        ax1.clear()
        ax2.clear()
        ax3.clear()
        ax4.clear()
        ax1.set(title = "K2 Force")
        # data_name = f"data/k2_tests/k2_test_k_1_k2_{rounded_k2}_epsilon_{rounded_epsilon}"
        # as_folder_name = f"data/alpha_shapes/k2_tests/k2_{rounded_k2}_ep_{rounded_epsilon}"
        # data_name = f"data/pyABP_k2_tests/pyABP_k2_{rounded_k2}_ep_{rounded_epsilon}"
        # as_folder_name = f"data/alpha_shapes/pyABP_k2_tests/k2_{rounded_k2}_ep_{rounded_epsilon}"
        potential_dict = {"k":1,"epsilon":rounded_epsilon,"delta":rounded_k2}
        data_name = f"data/{project_name}/{get_parameter_suffix(potential_dict)}"
        frame_no = 99
        print(save_range)
        a = Analysis(data_name,p_dict,save_range,data_type=data_type)
        a.plot_potential(ax1,repulsion_cohesion_potential2,[1,rounded_k2,rounded_epsilon])
        a.plot_g_r(ax2,1)
        # a.plot_alphashape(ax=ax3,frame_no=frame_no,single = True)
        ax4.set(title = f"Particles at {frame_no}000 time steps")
        a.plot_particles(ax4,0)
        fig.suptitle(f"K2 = {rounded_k2}, Epsilon = {rounded_epsilon}")
        fig.canvas.draw_idle()

cid = fig.canvas.mpl_connect('button_press_event', onclick)
plt.savefig("./media/test_save.png")
plt.show()