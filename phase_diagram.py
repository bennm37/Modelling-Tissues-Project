from phase_diagram_functions import *

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
frame_no = 50
ax0.set(title = "Phase Diagram")
ax1.set(title = "k2 Force")
ax2.set(title = "Alpha Shape of Particles")
ax4.set(title = f"Particles at {frame_no}000 time steps")
ax3.set(title="Radial Distribution Function")
ax2.axis("equal")
ax4.axis("equal")

##setting up phase diagram
n_k2 = 5
n_ep = 6
k2_range = (0.4,2.4)
ep_range = (0.05,0.35)
k2_int = (k2_range[1]-k2_range[0])/n_k2
ep_int = round((ep_range[1]-ep_range[0])/n_ep,2)
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
##TODO use get r_data and pass to plot_particles could be cleaner
ret,r_data = plot_particles(k2_init,ep_init,frame_no,ax4,p_dict = pyABP_dict,data_type=data_type)
plot_alpha_shape(k2_init,ep_init,frame_no,ax2,data_type,r_data)
plot_g_r(k2_init,ep_init,frame_no,ax3,data_type=data_type)

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
        ret,r_data = plot_particles(rounded_k2,rounded_epsilon,frame_no,ax4,p_dict = pyABP_dict,data_type=data_type)
        if ret:
            fig.suptitle(f"No data for K2 = {rounded_k2},epsilon = {rounded_epsilon}")
        else:
            fig.suptitle(f"K2 = {rounded_k2}, Epsilon = {rounded_epsilon}")
        ret3 = plot_g_r(rounded_k2,rounded_epsilon,frame_no,ax3,data_type="pyABP")
        plot_alpha_shape(rounded_k2,rounded_epsilon,frame_no,ax2,data_type,r_data)
        fig.canvas.draw_idle()

cid = fig.canvas.mpl_connect('button_press_event', onclick)
plt.savefig("./media/test_save.png")
plt.show()