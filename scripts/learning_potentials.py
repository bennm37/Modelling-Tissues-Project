from imports import *
import numpy as np 
import numpy.linalg as lag
import matplotlib.pyplot as plt
from parameter_dictionaries import toy_dict
from abp import *



# data = "../data/learning_potentials/k_1_epsilon_0.15_delta_0.6/"
data = "/Users/benn-m/Documents/Epithelial ABP/data/learning_potentials/k_1_epsilon_0.15_delta_0.6_many_short"
a = Analysis(data,toy_dict,range(2000),"pyABP")

##CHECK ALL FOR LOOPS AND RESHAPES ARE CORRECT

def normalise_3darr(arr):
    # normalised_arr = arr/np.moveaxis(np.tile(lag.norm(arr,axis=2),(2,1,1)),0,2)
    normalised_arr = np.nan_to_num(arr/lag.norm(arr,axis=2)[:,:,np.newaxis])
    return normalised_arr

# def phi_p(pvec,R,parameters):
#     c,w = parameters
#     ##uses repulsion force k(2*R-r_ij) from active colloid paper
#     ##this finds R_i +R_j for each i and j in 1,...N
#     R_sum = np.sum(np.meshgrid(R,R),axis=0)
#     dist = lag.norm(pvec,axis=2)
#     ##we will work with the distances divided by the sum of the 
#     ## 2 radii 
#     x = dist/R_sum

#     ##Just change this bit
#     in_range1 = (x-c+w)/w
#     in_range2 = -(x-c-w)/w
#     out_range = np.zeros(dist.shape)
#     force = np.where(x<c-w,out_range,in_range1)
#     force = np.where(x<c,force,in_range2)
#     force = np.where(x<c+w,force,out_range)
#     return force

def phi_mt(pvec,centers,width):
    """Returns a n*N*2 array of each components total force on each particle"""
    n = centers.shape[0]
    N = pvec.shape[0]
    normalised_pvec = normalise_3darr(pvec)
    dists = lag.norm(pvec,axis=2)
    tiled_pvec = normalised_pvec[np.newaxis,:,:,:]+np.zeros((n,N,N,2))
    tiled_dists = dists[np.newaxis,:,:] + np.zeros((n,N,N))
    x = tiled_dists-centers[:,np.newaxis,np.newaxis]
    c = 0 
    w = width
    in_range1 = (x-c+w)/w
    in_range2 = -(x-c-w)/w
    out_range = np.zeros(x.shape)
    force = np.where(x<c-w,out_range,in_range1)
    force = np.where(x<c,force,in_range2)
    force = np.where(x<c+w,force,out_range)
    #should pvec not be normalised here?
    return np.sum(force[:,:,:,np.newaxis]*tiled_pvec,axis=2)


def construct_phi(r,centers,width):
    n = len(centers)
    M,L,N,d = r.shape
    phi = np.zeros((n,L,N,d))
    for traj in r:
        ##KEY benifit of this process is can parallelise here instead
        ## of for loop 
        pvec_calc = Analysis(data,toy_dict,range(500),"pyABP")
        phi_m = np.zeros((n,L,N,d))
        for l,t in enumerate(traj):
            pvec = pvec_calc.pvec(l)
            phi_ml = phi_mt(pvec,centers,width)
            phi_m[:,l,:,:] = phi_ml
        phi += phi_m
    return phi/(L*N)

def construct_d(v):
    n,L,N,d = v.shape
    return np.sum(v.reshape(n,L*N*d),axis=0)


def solve():
    phi = construct_phi(traj_data,centers,width)
    print(phi)
    n,L,N,d = phi.shape
    shaped_phi = phi.reshape(n,N*L*d)
    pass

def plot_PL_potential(weights,centers,width):
    w = width 
    num_samples = 20
    fig,ax = plt.subplots()
    data = np.zeros(num_samples)
    for i,c in enumerate(centers):
        X = np.linspace(0,20,num_samples)
        for j,x in enumerate(X):
            pvec = np.array([[[x,0]]])
            ##TODO change potentials to take in one parameters arg not individual
            data[j] += weights[i]*phi_p(pvec,1,[c,w])[0,0]
    ax.plot(X,data)
    plt.show()

def dividing_trajectories(r_data,v_data,L,start_times):
    """Divides R_Data into trajectioes starting from start times of length L"""
    T_total,N,d = r_data.shape
    M = start_times.shape[0]
    traj = np.zeros([M,L,N,d])
    v_traj = np.zeros([M,L,N,d])
    for m,t in enumerate(start_times):
        traj[m] = r_data[t:t+L,:,:]
        v_traj[m] = v_data[t:t+L,:,:]
    return traj,v_traj

def get_histograms(centers):
    dist = lag.norm(a.pvec(1),axis=2).flatten()
    hist = np.histogram(dist,centers)[0]
    T = a.n_saves
    for t in range(1,T):
        dist = lag.norm(a.pvec(t),axis=2).flatten()
        hist += np.histogram(dist,centers)[0]
    return hist


# ts = np.linspace(0,100,1,dtype=int)
r_data = a.r_data
v_data = a.v_data
start_times = np.arange(0,2000,20)
dist = lag.norm(a.pvec(0),axis=2)
# print(f'dist is {dist}')
traj_data,v_traj_data = dividing_trajectories(r_data,v_data,20,start_times)
print(traj_data[99])
width = 0.2
centers = np.arange(0.6,6,width)
hist = get_histograms(centers)
fig,ax1 = plt.subplots()
# print(f'hist is {hist}')
ax1.bar(centers[:-1],hist,width = width)
plt.show()
phi = construct_phi(traj_data,centers,width)
n,L,N,d = phi.shape
move = np.moveaxis(phi,[0,1,2,3],[3,0,1,2])
# print(f"phi shape is {phi.shape}")
# print(f"move shape is {move.shape}")
A = move.reshape(N*L*d,n)
D = construct_d(v_traj_data)
# print(A)
LHS = A.T @ A
RHS = A.T @ D
print(f':LHS shape is {LHS.shape}')
print(f':RHS shape is {RHS.shape}')
print(LHS[np.nonzero(LHS)].shape)
print(LHS)

solution = lag.solve(LHS,RHS)
# print(solution)
fig,ax = plt.subplots()
a.plot_potential(ax,repulsion_cohesion_potential2,[1,0.15,0.6])
ax.set(ylim=(-3,3))
ax.plot(centers,solution)
plt.show()

# print(shaped_phi.T.shape)

## TESTING POTENTIAL PLOTTING
# plot_PL_potential(np.ones(10),[0,10],width=width)
# width = 5
# centers = np.arange(0,10,width)
# weights = 0.5*(centers-5)**2-12.5
# plot_PL_potential(weights,centers,width)
##TESTING phi_mt
# arr = np.array([[1,2],
#                [2,2],])  
# pvec_calc = Analysis(data,toy_dict,range(500),"pyABP")
# pvec_calc.r_data = np.array([arr])
# pvec_calc.N = 2
# pvec = pvec_calc.wrapped_pvec(0)
# centers = np.array([1,2,3,4])
# width = 1
# print(phi_mt(pvec,centers,width))
##seems to work!

##OBSOLETE NOW
# def phi_row(t,c,w):
#     """Uses psi to calculate f_ij, the magnitude of the force between each particle.
#     Then multiplies f_ij by the normalised and wrapped vector between 2 particles."""
#     ## This should be one row of the tensor 
#     pvec = a.wrapped_pvec(t)

#     ##REMOVED k here so specify potential parameters before passing potential
#     f_ij = -phi_p(pvec,1,[c,w])
#     ## sort out normalisation
#     # pvec_normalised = pvec
#     pvec_normalised = normalise_3darr(pvec)
#     forces = np.zeros(pvec.shape)
#     forces[:,:,0] = f_ij*pvec_normalised[:,:,0]
#     forces[:,:,1] = f_ij*pvec_normalised[:,:,1]

#     return np.sum(forces,axis=1)

