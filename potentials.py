import numpy as np
from numpy.lib.function_base import kaiser 
import numpy.linalg as lag 


def short_sacle_repulsion(pvec,R=1,k=1):
    ##uses repulsion force k(2*R-r_ij) from active colloid paper
    ##this finds R_i +R_j for each i and j in 1,...N
    R_sum = np.sum(np.meshgrid(R,R),axis=0)
    dist = lag.norm(pvec,axis=2)
    ##we will work with the distances divided by the sum of the 
    ## 2 radii 
    x = dist/R_sum
    in_range = -k*x+k
    out_range = np.zeros(dist.shape)
    force = np.where(x<1,in_range,out_range)
    return force

def repulsion_cohesion_potential(pvec,R=1,k=1,epsilon = 0.15):
    ##uses repulsion force k(2*R-r_ij) from active colloid paper
    ##this finds R_i +R_j for each i and j in 1,...N
    R_sum = np.sum(np.meshgrid(R,R),axis=0)
    dist = lag.norm(pvec,axis=2)
    ##we will work with the distances divided by the sum of the 
    ## 2 radii 
    x = dist/R_sum
    in_range1 = -k*x+k
    in_range2 = k*x-k*(1+epsilon)
    out_range = np.zeros(dist.shape)
    force = np.where(x<1+epsilon/2,in_range1,in_range2)
    force = np.where(x>1+epsilon,out_range,force)
    return force
    

def repulsion_cohesion_potential2(pvec,R=1,k=1,epsilon = 0.15,delta=0.2):
    ##uses repulsion force k(2*R-r_ij) from active colloid paper
    ##this finds R_i +R_j for each i and j in 1,...N
    R_sum = np.sum(np.meshgrid(R,R),axis=0)
    dist = lag.norm(pvec,axis=2)
    ##we will work with the distances divided by the sum of the 
    ## 2 radii 
    x = dist/R_sum
    in_range1 = -k*x+k
    in_range2 = -k*(epsilon/2)
    in_range3 = k*x-k*(1+epsilon+delta)
    out_range = np.zeros(dist.shape)
    force = np.where(x<1+epsilon/2,in_range1,in_range2)
    force = np.where(x>1+epsilon/2+delta,in_range3,force)
    force = np.where(x>1+epsilon+delta,out_range,force)
    return force


# def repulsion_cohesion_potential2(pvec,R=1,k=1,epsilon=0.15,delta=0.2):
#     """Uses potential from the glassy behaviour paper[1], setting b_i =1 """
#     dist = lag.norm(pvec,axis=2)
#     f_ij = np.where(dist<R+R*epsilon,k*(R*dist-np.full(dist.shape,R**2)),np.zeros(dist.shape))
#     ##TODO convoluted way of saying r<d<r_2 to get into one condition for where
#     f_ij = np.where(np.abs(dist-(R+3*R*epsilon/2))<(R*epsilon/2),-k*(R*dist-np.full(dist.shape,(1+2*epsilon)*R**2)),f_ij)
#     return f_ij

def parabola_potential(pvec,R,k=1,epsilon=0.5,l=-0.5):
    ##calculated to give y intercept k,minimum l and a root at 1+epsilon
    b = 2*(l-k)*(1+np.sqrt(1-k/(k-l)))/(1+epsilon)
    a = (b**2)/(4*(k-l))
    c = k
    ##this finds R_i +R_j for each i and j in 1,...N
    R_sum = np.sum(np.meshgrid(R,R),axis=0)
    dist = lag.norm(pvec,axis=2)
    ##we will work with the distances divided by the sum of the 
    ## 2 radii and then rescale in the end
    x = dist/R_sum
    in_range = a*x**2+b*x+c
    out_range = np.zeros(dist.shape)
    force = np.where(x<1+epsilon,in_range,out_range)
    return force

