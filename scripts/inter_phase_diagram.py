from imports import *
from abp import *
from analysis import *
from parameter_dictionaries import *
from potentials import *
from matplotlib.gridspec import GridSpec
from simulation import get_parameter_suffix
from matplotvideo import attach_video_player_to_figure

def on_frame(time_stamp):
    pass
data_type = "pyABP"
project_name = "pyABP_delta_tests"
p_dict = pyABP_delta_dict
frame_no = 499

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
ax3.set(title="Radial Distribution Function")
ax4.set(title = f"Particles at {frame_no}000 time steps")
ax2.axis("equal")
ax4.axis("equal")
##setting up phase diagram

n_p1,n_ep = 6,7
p1_range,ep_range  = (0,0.6),(0.05,0.35)
##TODO missing last values of ranges on phase diagram
p1_int,ep_int = (p1_range[1]-p1_range[0])/(n_p1-1),(ep_range[1]-ep_range[0])/(n_ep-1)
p1 = np.arange(p1_range[0],p1_range[1]+2*p1_int,p1_int)
ep = np.arange(ep_range[0],ep_range[1]+2*ep_int,ep_int)
P1,EP = np.meshgrid(p1,ep)
ax0.set(xlim=(p1_range[0],p1_range[1]+p1_int),ylim=(ep_range[0],ep_range[1]+ep_int))
# phases = np.linspace(0,5,6)
##creating and saving random phase diagram
# phase_diagram = np.random.choice(phases,(n_ep+1,n_p1+1))
# cols = [f"col{i}" for i in range(n_p1+1)]
# df = pd.DataFrame(phase_diagram,columns=cols)
# df.to_csv("data/phase_diagram.csv",index=False)
phase_diagram = np.array(pd.read_csv(f"data/{project_name}/phase_diagram.csv"))
pc = ax0.pcolormesh(P1,EP,phase_diagram,shading="flat",edgecolor="lightgrey",cmap="bone")
# ax0.set_xticks(p1)
# ax0.set_yticks(ep)
# ax0.grid(which="both")

##initial subplots
p1_init = 0.0
ep_init = 0.05
potential_dict = {"k":1,"epsilon":ep_init,"delta":p1_init}
data_name = f"data/{project_name}/{get_parameter_suffix(potential_dict)}"
save_range = range(frame_no,frame_no+1)
a = Analysis(data_name,p_dict,save_range,data_type=data_type)
a.plot_potential(ax1,k2_potential,[1,ep_init,p1_init])
a.plot_alphashape(ax=ax2,frame_no=frame_no,single = True)
a.plot_g_r(ax3,1)
a.plot_particles(ax4,0)
def onclick(event):
    if event.inaxes ==ax0:
        epsilon = event.ydata
        p1 = event.xdata
        rounded_p1 = round((p1//p1_int)*p1_int,2)
        rounded_epsilon = round((epsilon//ep_int)*ep_int,2)
        if rounded_p1%1 ==0 :
            rounded_p1 = float(rounded_p1)
        if rounded_epsilon%1 ==0 :
            rounded_epsilon = float(rounded_epsilon)
        print(f"rounding rounded_p1/k1 = {rounded_p1}, rounded_epsilon = {rounded_epsilon}")
        ax1.clear()
        ax2.clear()
        ax3.clear()
        ax4.clear()
        ax1.set(title = "p1 Force")
        ##COULD ADD IN ANIMATIONS HERE
        # attach_video_player_to_figure(fig,f"media/Paraview/para_rvd.mp4",on_frame)
        
        # data_name = f"data/p1_tests/p1_test_k_1_p1_{rounded_p1}_epsilon_{rounded_epsilon}"
        # as_folder_name = f"data/alpha_shapes/p1_tests/p1_{rounded_p1}_ep_{rounded_epsilon}"
        # data_name = f"data/pyABP_p1_tests/pyABP_p1_{rounded_p1}_ep_{rounded_epsilon}"
        # as_folder_name = f"data/alpha_shapes/pyABP_p1_tests/p1_{rounded_p1}_ep_{rounded_epsilon}"
        potential_dict = {"k":1,"epsilon":rounded_epsilon,"delta":rounded_p1}
        data_name = f"data/{project_name}/{get_parameter_suffix(potential_dict)}"
        frame_no = 499
        print(save_range)
        a = Analysis(data_name,p_dict,save_range,data_type=data_type)
        a.plot_potential(ax1,repulsion_cohesion_potential2,[1,rounded_epsilon,rounded_p1])
        a.plot_alphashape(ax=ax2,frame_no=frame_no,single = True)
        a.plot_g_r(ax3,1)
        ax4.set(title = f"Particles at {frame_no}000 time steps")
        a.plot_particles(ax4,0)
        fig.suptitle(f"p1 = {rounded_p1}, Epsilon = {rounded_epsilon}")
        fig.canvas.draw_idle()
        plt.show()


##ANNOTATING ON HOVER 
annot = ax0.annotate("", xy=(0.1,0.1), xytext=(-90,10),textcoords="offset points",
                    bbox=dict(boxstyle="round", fc="k"),
                    arrowprops=dict(arrowstyle="-"))
annot.set_visible(True)
def onhover(event):
    if event.inaxes == ax0:
        epsilon = event.ydata
        p1 = event.xdata
        ind_p1 = p1//p1_int
        rounded_p1 = round(ind_p1*p1_int,2)
        ind_ep = epsilon//ep_int
        rounded_epsilon = round(ind_ep*ep_int,2)
        annot.xy = rounded_p1,rounded_epsilon
        # annot.xytext = (-30,10)
        frac_dim = 1
        rad_gyr = 1
        annot.set_text(f"Delta,Epsilon = {rounded_p1,rounded_epsilon} \n\
Fractal Dimension is {frac_dim}.\n\
Radius of Gyration is {rad_gyr}.")
        annot.get_bbox_patch().set_facecolor("grey")
        annot.get_bbox_patch().set_alpha(0.8)
        annot.set_visible(True)
        fig.canvas.draw_idle()
    else:
        annot.set_visible(False)
        fig.canvas.draw_idle()

cid = fig.canvas.mpl_connect('button_press_event', onclick)
# cid2 = fig.canvas.mpl_connect('motion_notify_event', onhover)
plt.savefig("./media/test_save.png")
plt.show()