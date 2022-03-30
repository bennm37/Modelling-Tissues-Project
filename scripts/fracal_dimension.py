from imports import *
from analysis import Analysis
from parameter_dictionaries import pyABP_delta_dict
from imports import * 
import numpy as np 
from bresenham import bresenham
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

# s = 10
# poly = poly*s 
a = Analysis("data/pyABP_delta_tests/k_1_epsilon_0.1_delta_0.36",pyABP_delta_dict,range(0),"pyABP")
poly = a.load_alphashape(499)[11]
s=10 
# print([(i,len(p)) for i,p in enumerate(poly)])
# poly = np.array([[1,1],[5,5],[5,8],[2,7]])
# print(poly)
def boxcount(poly):
    """Uses bresenham algorithms to count the number of squares
    the polygon touches at the given resolution"""
    squares = np.zeros((0,2))
    npoly = len(poly)
    for i,point in enumerate(poly):
        if i<npoly-1:
            end = poly[i+1]
        elif npoly == 2 and i == 1: #line case
            return squares
        else: #loop back to first point
            end = poly[0]
        sq = np.array(list(bresenham(point[0],point[1],end[0],end[1])))
        squares = np.append(squares,sq,axis=0)
    return squares

# ax.axis("equal")
# ax.set(xlim=(0,10),ylim=(0,10))
def boxplot(squares,nx,ny,poly,ax):
    x = np.arange(0,nx,1)
    y = np.arange(0,ny,1)
    X,Y = np.meshgrid(x,y)
    C = np.zeros((nx,ny))
    for square in squares:
        C[int(square[0]),int(square[1])] = 1
    p = Polygon(poly,fill=None,edgecolor="k")
    ax.add_patch(p)
    ax.pcolor(X,Y,C.T,cmap="coolwarm")


fig,ax = plt.subplots()
squares = boxcount(np.round(poly*s,0).astype(int))
boxplot(squares,200*s,200*s,poly,ax)
plt.show()


def fractal_dimension(multipoly):
    n=20
    s_up = np.arange(4,n+3,1)
    counts = np.zeros(n-1)
    for i,s in enumerate(s_up):
        for poly in multipoly:
            test_poly = np.round(poly*s,0).astype(np.int)
            squares = boxcount(test_poly)
            counts[i] += len(squares)
    linreg = LinearRegression()
    s_up,counts = s_up.reshape(-1,1),counts.reshape(-1,1)
    linreg.fit(np.log(s_up),np.log(counts))
    m,b = linreg.coef_,linreg.intercept_
    return s_up,counts,m,b

s_up,counts,m,b = fractal_dimension([poly])

def log_log_plot(s,counts,m,b):
    fig,ax = plt.subplots()
    ax.scatter(np.log(s_up),np.log(counts))
    x = np.linspace(0,np.log(20),30)
    y = m*x+b
    ax.plot(x,y.reshape(30))
    ax.set(xlabel="s",ylabel="square count")
    print(f"Fractal Dimension is {m} over 20 samples.")

log_log_plot(s_up,counts,m,b)
plt.show()


##CRAZY NUMPY ARRAY ADDING HACK
# points = np.array([[1,2],[2,3]])
# other_points = np.array([[4,5],[6,7],[8,9]])
# print(points[np.newaxis,:,:]+other_points[:,:,np.newaxis])