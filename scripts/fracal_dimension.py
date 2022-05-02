from audioop import mul
from imports import *
from analysis import Analysis
from parameter_dictionaries import pyABP_delta_dict
from imports import * 
import numpy as np 
from bresenham import bresenham
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from scripts.supercover import line_supercover

def boxcount(multipoly):
    """Uses bresenham algorithms to count the number of squares
    the polygon touches at the given resolution"""
    squares = np.zeros((0,2))
    for poly in multipoly:   
        nvert = len(poly)
        for i,point in enumerate(poly):
            if i<nvert-1:
                end = poly[i+1]
            elif nvert == 2 and i == 1: #line case
                return squares
            else: #loop back to first point
                end = poly[0]
            # sq = np.array(list(bresenham(point[0],point[1],end[0],end[1])))
            rr,cc = line_supercover(point[1],point[0],end[1],end[0])
            sq = np.array([rr,cc]).T
            squares = np.append(squares,sq,axis=0)
    return np.unique(squares,axis=0)

def boxplot(squares,nx,ny,multipoly,ax):
    x = np.arange(0,nx,1)
    y = np.arange(0,ny,1)
    X,Y = np.meshgrid(x,y)
    C = np.zeros((nx,ny))
    for square in squares:
        C[int(square[0]),int(square[1])] = 1
    for poly in multipoly:
        p = Polygon(poly,fill=None,edgecolor="k")
        ax.add_patch(p)
    ax.pcolor(X,Y,C,cmap="Blues")

def fractal_dimension(multipoly,scales=[1,1.2]):
    n= 30
    s_up = np.exp(np.linspace(scales[0],scales[1],n))
    counts = np.zeros(n)
    for i,s in enumerate(s_up):
        # print(f"starting scale {s}")
        scaled_multipoly = [np.round(p*s).astype(int) for p in multipoly]
        squares = boxcount(scaled_multipoly)
        counts[i] += len(squares)
    linreg = LinearRegression()
    s_up,counts = s_up.reshape(-1,1),counts.reshape(-1,1)
    linreg.fit(np.log(s_up),np.log(counts))
    m,b = linreg.coef_,linreg.intercept_
    return s_up,counts,m,b

def log_log_plot(s,counts,m,b,scales=[1,3],ax =None,label=None):
    if not ax:
        fig,ax = plt.subplots()
    ax.scatter(np.log(s),np.log(counts))
    x = np.linspace(scales[0],scales[1],30)
    y = m*x+b
    ax.axis("equal")
    if label:
        ax.plot(x,y.reshape(30),label=label)
    else:
        ax.plot(x,y.reshape(30))
    ax.set(xlabel="ln(s)",ylabel="box count")
    print(f"Fractal Dimension is {m} over 20 samples.")

# s = 10
# poly = poly*s 
a = Analysis("data/pyABP_delta_tests/k_1_epsilon_0.1_delta_0.36",pyABP_delta_dict,range(0),"pyABP")
# # a = Analysis("data/pyABP_delta_tests/k_1_epsilon_0.3_delta_0.12",pyABP_delta_dict,range(0),"pyABP")
# multipoly = a.load_alphashape(499)
multipoly = [shape for shape in a.load_alphashape(499)]
s = -0
S = np.exp(s)
# poly = a.load_alphashape(499)
##GRID TEST
# x = np.linspace(0,190,100)
# X,Y = np.meshgrid(x,x)
# multipoly = [row for row in np.moveaxis([X,Y],0,2).reshape(100,100,2)]
# multipoly = np.append(multipoly,[row for row in np.moveaxis([Y,X],0,2).reshape(100,100,2)],axis=0)
#CIRCLE TEST 
# thetas = np.linspace(0,2*np.pi,100)
# R = 90
# points = np.transpose([R*np.cos(thetas)+100,R*np.sin(thetas)+100])
# multipoly = [points]
#TESTING BOXCOUNT/BOXPLOT
fig,ax = plt.subplots()
ax.axes.xaxis.set_visible(False)
ax.axes.yaxis.set_visible(False)
squares = boxcount([np.round(p*S).astype(int) for p in multipoly])
box_size = np.round(200*S,0).astype(int)
boxplot(squares,box_size,box_size,[p*S for p in multipoly],ax)
ax.set(title=f"Supercover Rasterization $s={np.round(S,2)}$,$N_b(s)={len(squares)}$")
# plt.savefig(f"C:/Users/bennm/Documents/UNI/Year3/Non Code Project Stuff/supercover_ep_{0.1}_delt_{0.36}_{np.round(S,2)}.pdf")
plt.savefig(f"media/pyABP_delta_tests/summary_plots/fractal dimension/supercover_ep_{0.1}_delt_{0.36}_{np.round(S,2)}.pdf")
plt.show()


##TESTING FRACTAL DIMENSION
# scales = [-4,-1.5]
# s_up,counts,m,b = fractal_dimension(multipoly,scales=scales)
# plt.style.use("ggplot")
# log_log_plot(s_up,counts,m,b,scales=scales)
# plt.show()

##RUNNING FOR SEARCH GRID
# epsilon = [0.05,0.1,0.15,0.2,0.25,0.3,0.35]
# deltas = [0.0,0.12,0.24,0.36,0.48,0.6]
# f_dim_grid = np.zeros((len(epsilon),len(deltas)))
# for j,delt in enumerate(deltas):
#     fig,ax = plt.subplots()
#     for i,ep in enumerate(epsilon):
#         print(f"Starting ep = {ep},delt = {delt}")
#         a = Analysis(f"data/pyABP_delta_tests/k_1_epsilon_{ep}_delta_{delt}",pyABP_delta_dict,range(0),"pyABP")
#         try:
#             multipoly = [shape for shape in a.load_alphashape(499)]
#         except TypeError:
#             f_dim_grid
#             continue
#         scales = [-4,-1.5]
#         s_up,counts,m,b = fractal_dimension(multipoly,scales=scales)    
#         log_log_plot(s_up,counts,m,b,scales=scales,ax =ax,label=f"$ \epsilon= $ {ep},$ \delta= ${delt}")   
#         f_dim_grid[i,j] = m
#     ax.legend()
#     ax.set(title=f"Box Count at Different Scales, $\delta = {delt}$")
#     plt.savefig(f"media/pyABP_delta_tests/summary_plots/fractal dimension/box_count_delta_{delt}.pdf")
# print(f_dim_grid)


##CRAZY NUMPY ARRAY ADDING HACK
# points = np.array([[1,2],[2,3]])
# other_points = np.array([[4,5],[6,7],[8,9]])
# print(points[np.newaxis,:,:]+other_points[:,:,np.newaxis])