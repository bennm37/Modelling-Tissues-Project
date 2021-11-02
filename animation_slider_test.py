import numpy as np 
import matplotlib.animation as animation
import matplotlib.pyplot as plt 
from matplotlib.patches import Ellipse
from matplotlib.widgets import Slider

fig,ax = plt.subplots()
fig.set_size_inches(8,8)
k_init = 1
omega_init = 0.1
ax.set(xlim=(-2*k_init,2*k_init),ylim=(-2*k_init,2*k_init))
N = 200
PHI = (3-np.sqrt(5))*np.pi
r = np.linspace(0,k_init,N+1)
thetas = np.linspace(0,N*PHI,N+1)
s = ax.scatter(r*np.cos(thetas),r*np.sin(thetas))
plt.subplots_adjust(left=0.25, bottom=0.25)
axk = plt.axes([0.25, 0.1, 0.65, 0.03])
k_slider = Slider(axk,
    label ="k",
    valmin=0,
    valmax=10,
    valinit=k_init
)
def update(val):
    r = np.linspace(0,k_slider.val,N+1)
    s.set_offsets(np.array((r*np.cos(thetas),r*np.sin(thetas))).T)
k_slider.on_changed(update)
def update_anim(i):
    thetas = np.linspace(0,N*PHI,N+1)+omega_init*i
    s.set_offsets(np.array((r*np.cos(thetas),r*np.sin(thetas))).T)
anim = animation.FuncAnimation(fig,update,100)

plt.show()