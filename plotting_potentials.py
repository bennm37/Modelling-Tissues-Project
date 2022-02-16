import numpy as np 
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from potentials import *

##plotting_potentials
def plot_potential(potential,parameters,ax=None):
    num_samples = 150
    R = np.ones(1)
    data = np.zeros((num_samples))
    X = np.linspace(0,4,num_samples)
    for i,x in enumerate(X):
        pvec = np.array([[[x,0]]])
        ##TODO change potentials to take in one parameters arg not individual
        k,k2,epsilon = parameters
        data[i] = potential(pvec,R,k,k2,epsilon)[0,0]
    if not ax:
        fig,ax = plt.subplots()
        
    ax.set(ylim=(-1,1))
    p = ax.plot(X,data)
    return p,ax

def parameter_potential_plot(potential,slider_names,slider_ranges=None,slider_init=None):
        n_sliders = len(slider_names)
        if not slider_ranges:
            slider_ranges = [[-5,5] for i in range(n_sliders)]
        if not slider_init:
            slider_init = [1 for i in range(n_sliders)]
        # Create the figure and the vf that we will manipulate

        parameters = slider_init
        p,ax = plot_potential(potential,parameters)
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
            p,ax1 = plot_potential(potential,parameters,ax)

        # register the update function with each slider
        for s in sliders:
            s.on_changed(update)
        plt.show()

# parameter_potential_plot(k2_potential,["k","k2","epsilon"],slider_init=[1,0.15,-1],slider_ranges=[(0,1),(0,3),(0,5)])