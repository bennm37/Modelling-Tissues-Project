from imports import *
from abp import ABP 
import numpy as np
import time
import numpy.linalg as lag
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from analysis import Analysis
from parameter_dictionaries import inter_potential_dict
from potentials import repulsion_cohesion_potential, repulsion_cohesion_potential2
plt.style.use("ggplot")
def inter_potential_test(ax,potential,potential_parameters):
    global particles
    psi = lambda pvec,R: potential(pvec,R,potential_parameters)
    particles = ABP(inter_potential_dict,psi)
    particles.r = np.array([[4,5],[6,5]],dtype=float)
    plt.ion()
    plt.show()
    while True:
        particles.update(0.2)
        ax.clear()
        plot_particles(ax,particles.r,particles.directions(),particles.rdot)
        plt.draw()
        plt.pause(0.03)
def plot_particles(ax,r1,d,v,boxwidth=10):
    asp = [15,15,10,7.5,1] ##hal,hl,s,hw,ms
    ax.axis("equal")
    ax.set(xlim=(0,boxwidth),ylim=(0,boxwidth))
    directions = ax.quiver(r1[:,0],r1[:,1],d[:,0],d[:,1])
    velocities = ax.quiver(r1[:,0],r1[:,1],v[:,0],v[:,1],color="r",
        headaxislength=asp[0],headlength=asp[1],scale=asp[2],headwidth=asp[3],minshaft=asp[4])
    for cell in r1[:,:]:
        c = Ellipse(cell,2,2,fill=False,color="k")
        p = ax.add_patch(c)

def button_press_callback(event):
    'whenever a mouse button is pressed'
    print("mouse pressed")
    global pind
    global particles
    if event.inaxes is None:
        return
    if event.button != 1:
        return
    mouse = np.array([event.xdata,event.ydata])
    pos = particles.r[0]
    if lag.norm(mouse-pos)<1:
        print("in radius")
        pind = 0 

def button_release_callback(event):
    'whenever a mouse button is released'
    global pind
    if event.button != 1:
        return
    pind = None

def motion_notify_callback(event):
    'on mouse movement'
    global particles
    if pind is None:
        return
    if event.inaxes is None:
        return
    if event.button != 1:
        return
    r = particles.r
    x = event.xdata
    y = event.ydata
    # print(f"event.xdata = {x}")
    # print(f"event.ydata = {y}")
    r[pind,0] = float(x) 
    r[pind,1] = float(y)
    particles.r = r
    ax.clear()
    plot_particles(ax,particles.r,particles.directions(),particles.rdot)
    fig.canvas.draw()


fig,axs = plt.subplots(1,2)
fig.set_size_inches(10,5)
ax = axs[1]
potential_parameters = [1,0.15,0.1]
a = Analysis("1",inter_potential_dict,range(1))
a.plot_potential(axs[0],repulsion_cohesion_potential2,potential_parameters)

fig.canvas.mpl_connect('button_press_event', button_press_callback)
fig.canvas.mpl_connect('button_release_event', button_release_callback)
fig.canvas.mpl_connect('motion_notify_event', motion_notify_callback)
pind = None
inter_potential_test(ax,repulsion_cohesion_potential2,potential_parameters)