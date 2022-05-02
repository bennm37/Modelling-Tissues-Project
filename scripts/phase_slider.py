import numpy as np 
import matplotlib.pyplot as plt 
from matplotlib.widgets import Slider
from pcolour_plots import pcolor_plot
import pickle
def phase_slider(grid,ax):
    n_sliders = 2
    slider_names = ['vmin','vmax']
    slider_ranges = [[-5,10],[-5,10]]
    slider_init = [0,5]
    plt.subplots_adjust(bottom=0.1*n_sliders)
    cb = pcolor_plot(grid,ax,v=slider_init)
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
        ax.clear()
        # cb.remove()
        v_min,v_max = [s.val for s in sliders]
        pcolor_plot(grid,ax,v=[v_min,v_max],lut=3)

    # register the update function with each slider
    for s in sliders:
        s.on_changed(update)
    return sliders

a_length = pickle.load(open("media/pyABP_delta_tests/summary_plots/alpha_lengths/average_lenths.p",'rb'))
a_num = pickle.load(open("media/pyABP_delta_tests/summary_plots/alpha_lengths/num_shapes.p",'rb'))
a_num_log = np.log(a_num)
a_length_scaled = a_length/(2*np.sqrt(2000)*np.pi)
fig,ax = plt.subplots()
sliders = phase_slider(a_num_log,ax)
print(a_num_log)
plt.show()