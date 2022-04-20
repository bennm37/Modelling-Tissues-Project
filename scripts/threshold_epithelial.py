import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import cv2 as cv
from skimage.segmentation import clear_border 
from skimage import measure
from imports import *
from analysis import *
from parameter_dictionaries import pyABP_delta_dict

filename = "C:/Users/bennm/Documents/UNI/Year3/Non Code Project Stuff/epithelial cells 3.jpg"
img_col = cv.imread(filename)
img = img_col[:1200,:1200,0]

##applying thresholding for left cells
ret,thresh_img = cv.threshold(img,90,250,cv.THRESH_BINARY)
# no_edge = clear_border(thresh_img)
label_thresh_img = measure.label(thresh_img)

##creates a dataframe with all the properties of each region
props = measure.regionprops_table(label_thresh_img,properties=["centroid","area"])
df = pd.DataFrame(props)
centres = np.array(df)

##scatter centres
plt.scatter(centres[:,0],centres[:,1])
r_data = np.array([centres[:,0:2]])
print(r_data.shape)
plt.show()


a = Analysis("data/pyABP_delta_tests/k_1_epsilon_0.1_delta_0.0",pyABP_delta_dict,range(1),"pyABP")
print(a.r_data.shape)
cell_dict = pyABP_delta_dict
##1 is 1200,477 : 2 is 582,1200 : 3 is     : 4 is 600,103
cell_dict["box_width"]= 1200
cell_dict["N"]= 251
a = Analysis("",cell_dict,range(1))
print(a.N,a.box_width,a.r_data.shape)
a.r_data = r_data
drs,g_r = a.g_r(0,dr=2)
fig,ax = plt.subplots()
ax.plot(drs,g_r)
plt.show()
print(drs,g_r)



##PLOTTING AND FILTERING 
# print("filtering by cell size")
# centres = centres[centres[:,2]>20]
# centres = centres[centres[:,2]<500]
# print(f"filtered centres are {centres}")

fig,ax = plt.subplots(1,1)
axs = [ax]
axs[0].scatter(centres[:,1],centres[:,0],s=2)
axs[0].imshow(img_col)
for centre in centres:
    R = np.sqrt(centre[2]/np.pi)
    p = Ellipse([centre[1],centre[0]],2*R,2*R,fill=None,color="red")
    axs[0].add_patch(p)
areas = centres[:,2]
# axs[1].hist(areas,bins=100,range=(0,1000))
plt.show()