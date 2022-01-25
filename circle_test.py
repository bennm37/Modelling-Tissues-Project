from abp import *
from analysis import Analysis
from parameter_dictionaries import *
from potentials import *
from matplotlib.widgets import Slider,RadioButtons

N = 100
test_dict = {
    "R":np.ones(N),
    "N":N,
    "v_0":0.01,
    "D":0.1,
    "box_width":box_width_from_phi(N,0.6),
    "T":100000,
    "dt": 0.01,
    }

def circle_test_setup(potential,potential_parameters,parameters=test_dict):
    ##SETUP 
    N = parameters["N"]
    bw = parameters["box_width"]
    start_radius = np.sqrt(bw)
    # n = np.sqrt(np.linspace(0,N,N,endpoint=False))*np.pi
    # uniform_spacing = start_radius*np.array([np.cos(n)-n*np.sin(n),np.sin(n)+n*np.cos(n)])
    thetas = np.random.uniform(0,2*np.pi,N)
    radii = np.sqrt(np.random.uniform(0,start_radius,N))
    rs = np.transpose([radii*np.cos(thetas),radii*np.sin(thetas)])+np.full((N,2),bw/2)

    ##POTENTIAL SETUP
    k,k_2,epsilon = potential_parameters
    def psi(pvec,R):
        return potential(pvec,R,k,k_2,epsilon)
    if False:
        fig,ax = plt.subplots()
        ax.axis("equal")
        # ax.scatter(uniform_spacing[0],uniform_spacing[1])
        ax.scatter(rs[0],rs[1])
    print(psi([[[1,1]]],[1]))
    particles = ABP(parameters,psi)
    particles.r = rs
    folder_name = f"k2_test_k_{k}_k_2_{k_2}_epsilon_{epsilon}"
    particles.generate_csv(100,folder_name)

    a = Analysis("data/" +folder_name,k_2_test_dict,k_2_test_dict["T"]//100)
    anim =  a.animate_movement_patch()
    anim.save(f"media/centre_tests/{folder_name}.mp4")
    return folder_name

def circle_test(potential,potential_parameters,parameters=test_dict,data_point=1000,ax=None):
    k,epsilon,l = potential_parameters
    def psi(pvec,R):
        return potential(pvec,R,k,epsilon)
    parameters["T"] = data_point
    particles = ABP(parameters,psi)
    particles.r = (particles.box_width/2)*np.ones((particles.N,2))
    ##TODO check these numbers
    asp = [10,10,15]
    r_data,direction_data,velocity_data = particles.generate_movement_data(100)
    if not ax:
        fig,ax = plt.subplots()
    # fig.set_size_inches(8,8)
    ax.set(xlim=(0,parameters["box_width"]),ylim=(0,parameters["box_width"]))
    directions = ax.quiver(r_data[-1,:,0],r_data[-1,:,1],direction_data[-1,:,0],direction_data[0,:,1],
        headaxislength=asp[0],headlength=asp[1],scale=asp[2])
    velocities = ax.quiver(r_data[-1,:,0],r_data[-1,:,1],velocity_data[-1,:,0],velocity_data[0,:,1],color="r",
        headaxislength=asp[0],headlength=asp[1],scale=asp[2])
    for cell in r_data[-1,:,:]:
        c = Ellipse(cell,2,2,fill=False,color="k")
        p = ax.add_patch(c)
    return p,ax


def circle_test_slider(potential,slider_names,slider_ranges=None,slider_init=None):
        n_sliders = len(slider_names)
        if not slider_ranges:
            slider_ranges = [[-5,5] for i in range(n_sliders)]
        if not slider_init:
            slider_init = [1 for i in range(n_sliders)]
        # Create the figure and the vf that we will manipulate

        parameters = slider_init
        p,ax = circle_test(potential,parameters)
        # adjust the main plot to make room for the sliders
        plt.subplots_adjust(bottom=0.1*n_sliders)

        # Make a horizontal slider to control alpha
        slider_ax = [None for i in range(n_sliders)]
        sliders = [None for i in range(n_sliders)]
        for i,name in enumerate(slider_names):
            slider_ax[i] = plt.axes([0.25, 0.1+0.05*i, 0.5, 0.03])
            sliders[i] = Slider(
                slider_ax[i],
                label = name,
                valmin=slider_ranges[i][0],
                valmax=slider_ranges[i][1],
                valinit = slider_init[i])

        def update(val):
            parameters = [s.val for s in sliders]
            ax.clear()
            p,ax1 = circle_test(potential,parameters,ax = ax)

        # register the update function with each slider
        for s in sliders:
            s.on_changed(update)
        plt.show()

# circle_test_slider(parabola_potential,["k","epsilon","l"],slider_init=[1,0.15,-1],slider_ranges=[(0,3),(0,1),(-5,0)])
# circle_test_setup(k_2_potential,[1,2,0.15])
# plt.show()