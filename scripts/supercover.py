import numpy as np 
import matplotlib.pyplot as plt
from skimage import draw
from sympy import multiplicity

def rasterize_polygons(polygons, bounds = [[-100, -100], [100, 100]], dx = 1, dy = 1):
    # Prepare polygon array by shifting all points into the first quadrant and
    # separating points into x and y lists
    xpts = []
    ypts = []
    for p in polygons:
        p_array = np.asarray(p)
        x = p_array[:,0]
        y = p_array[:,1]
        xpts.append((x-bounds[0][0])/dx-0.5)
        ypts.append((y-bounds[0][1])/dy-0.5)

    # Initialize the raster matrix we'll be writing to
    xsize = int(np.ceil((bounds[1][0]-bounds[0][0]))/dx)
    ysize = int(np.ceil((bounds[1][1]-bounds[0][1]))/dy)
    raster = np.zeros((ysize, xsize), dtype=np.bool)

    # TODO: Replace polygon_perimeter with the supercover version
    for n in range(len(xpts)):
        rr, cc = draw.polygon(ypts[n], xpts[n], shape=raster.shape)
        rrp, ccp = draw.polygon_perimeter(ypts[n], xpts[n], shape=raster.shape, clip=False)
        raster[rr, cc] = 1
        raster[rrp, ccp] = 1

    return raster 
def line_supercover(y0, x0, y1, x1):
    dx = abs(x1-x0)
    dy = abs(y1-y0)
    x = x0
    y = y0
    ii = 0
    n = dx + dy
    err = dx - dy
    x_inc = 1 
    y_inc = 1 

    max_length = (max(dx,dy)+1)*3

    rr = np.zeros(max_length, dtype=np.intp)
    cc = np.zeros(max_length, dtype=np.intp)

    if x1 > x0: x_inc = 1 
    else:       x_inc = -1
    if y1 > y0: y_inc = 1 
    else:       y_inc = -1

    dx = 2 * dx
    dy = 2 * dy

    while n > 0:
        rr[ii] = y
        cc[ii] = x
        ii = ii + 1
        if (err > 0):
            x += x_inc
            err -= dy
        elif (err < 0):
            y += y_inc
            err += dx
        else: # If err == 0 the algorithm is on a corner
            rr[ii] = y + y_inc
            cc[ii] = x
            rr[ii+1] = y
            cc[ii+1] = x + x_inc
            ii = ii + 2
            x += x_inc
            y += y_inc
            err = err + dx - dy
            n = n - 1
        n = n - 1 
    rr[ii] = y
    cc[ii] = x
        
    return np.asarray(rr[0:ii+1]), np.asarray(cc[0:ii+1])

    
# thetas = np.linspace(0,2*np.pi,100)
# R = 90
# points = np.transpose([R*np.cos(thetas),R*np.sin(thetas)])
# multipoly = [points]
# rr,cc = line_supercover(1,1,7,9)
# print(rr,cc)
