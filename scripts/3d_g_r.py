import matplotlib.pyplot as plt
import numpy as np
import pandas as pd 

g_r_data = pd.read_csv("C:/Users/bennm/Documents/UNI/Year3/Modelling Tissues Project/data/pyABP_delta_tests/k_1_epsilon_0.1_delta_0.0/g(r)/g(r).csv")
r_data = np.array(g_r_data["r"])
g_r = np.array(g_r_data["g(r)"])
# Create the mesh in polar coordinates and compute corresponding Z.
r_range = 8
n_r = r_range*20
print(r_data)
r = np.linspace(0, r_range,n_r)
p = np.linspace(0, 2*np.pi, 50)
R, P = np.meshgrid(r, p)
G_R = np.zeros(R.shape)
for i,row in enumerate(R):
    for j,r_val in enumerate(row):
        G_R[i,j] = g_r[np.abs(r-r_val).argmin()//2]

# Express the mesh in the cartesian system.
X, Y = R*np.cos(P), R*np.sin(P)

# Plot the surface.
fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.set_axis_off()
ax.plot_surface(X, Y, G_R, cmap = plt.cm.YlGnBu_r,vmax =5)

# Tweak the limits and add latex math labels.
# ax.set_zlim(0, 1)
ax.set_zlabel(r'$g(r)$')
plt.show()

##CONTOUR OVERLAY SCHEMATIC
# fig,ax = plt.subplots()
# img = plt.imread("C:/Users/bennm/Documents/UNI/Year3/Non Code Project Stuff/g(r)_schematic3.png")
# # ax.imshow(img)
# w,h = np.array(img[:,:,0]).shape
# center = np.array([w/2,h/2])
# # scaled_x = X*w/r_range+w/2 
# # scaled_y = Y*h/r_range+h/2 
# scaled_x = X*400/(r_range*0.315)+920
# scaled_y = Y*400/(r_range*0.315)+860
# levels = [9,12,28]
# cont = ax.contour(scaled_x,scaled_y,G_R,levels=levels,cmap="magma",alpha=1)
# ax.set(xlim=(0,w*1.1),ylim=(0,h))
# plt.show()