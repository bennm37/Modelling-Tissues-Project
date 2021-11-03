import numpy as np
from numpy.lib.function_base import select 
import numpy.linalg as lag
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Polygon,Ellipse
from IPython.display import HTML
import pandas as pd 

def short_scale_repulsion(pvec,R=0.1,k=1):
    ##uses repulsion force k(2*R-r_ij) from active colloid paper
    dist = lag.norm(pvec,axis=2)
    f_ij = np.where(dist<R,-k*(np.full(dist.shape,2*R)-dist),np.zeros(dist.shape))
    return f_ij

def repulsion_cohesion_potential(pvec,R=1,k=1,epsilon=0.2):

    """Uses potential from the glassy behaviour paper[1], setting b_i =1 """
    dist = lag.norm(pvec,axis=2)
    f_ij = np.where(dist<R+R*epsilon,k*(R*dist-np.full(dist.shape,R**2)),np.zeros(dist.shape))
    ##TODO convoluted way of saying r<d<r_2 to get into one condition for where
    f_ij = np.where(np.abs(dist-(R+3*R*epsilon/2))<(R*epsilon/2),-k*(R*dist-np.full(dist.shape,(1+2*epsilon)*R**2)),f_ij)
    return f_ij

class ABP(object):
    ##TODO add **kwargs ? 
    def __init__(self,N,v_0=0.1,r=np.zeros(2),thetas=np.zeros(2),box_width=10,dim=2,D=0.5,R=1,k=1,potential=short_scale_repulsion):
        """Creates N Active Brownian Particles with uniformly random
        initial positions and directions unless specified. V_0 is the 
        velocity generated by the traction of the crawling particle on 
        the substrate, measured relative to boxwidth, D is the 
        angular diffusivity parameter measured in radians, R is the 
        radius of particles measured in fraction of box width, k is
        the interaction strength (parameter of interaction force)."""
        #TODO protect against bad input
        self.box_width = box_width
        if np.all(r==0):
            self.r = np.random.uniform(0,self.box_width,(N,dim)) 
        else:
            self.r = r
        if np.all(thetas==0):
            self.thetas = np.random.uniform(0,2*np.pi,N)
        else:
            self.thetas = thetas
        self.v_0 = v_0
        self.dim = dim
        self.N = N
        self.R = R
        self.k = k
        self.D = D #diffusion of polarity
        self.psi = potential
        self.rdot = self.v_0*self.directions()+np.sum(self.interaction_forces(),axis=1)

    def update(self,dt):
        self.rdot = self.v_0*self.directions()+np.sum(self.interaction_forces(),axis=1)
        theta_dot = np.random.normal(0,self.D,self.thetas.shape) 
        self.r = (self.r + self.rdot*dt)%self.box_width #implements periodic boundary conditions
        self.thetas = self.thetas + np.sqrt(dt)*theta_dot
    
    def normalise_3darr(self,arr):
        normalised_arr = np.nan_to_num(arr/np.moveaxis(np.tile(lag.norm(arr,axis=2),(2,1,1)),0,2))
        return normalised_arr

    def pvec(self):
        """Returns a square matrix of pairwise vectors between all particles """
        r = self.r
        r_tile_v = np.tile(r,(self.N,1)).reshape(self.N,self.N,2)
        r_tile_h = np.tile(r,(1,self.N)).reshape(self.N,self.N,2)
        return r_tile_v-r_tile_h

    def wrapped_pvec(self):
        """Returns a square matrix of pairwise vectors between all particles 
        with periodic bounday conditions"""
        L = self.box_width
        pvec = self.pvec()
        # if the distance between particles is more than half the width of the
        # box then the distance is measured the other way
        return pvec - np.where(np.abs(pvec)>L,np.sign(pvec)*L,np.zeros(pvec.shape))
    
    def directions(self):
        return np.array([np.cos(self.thetas),np.sin(self.thetas)]).T
    
    def interaction_forces(self):
        """Uses psi to calculate f_ij, the magnitude of the force between each particle.
        Then multiplies f_ij by the normalised and wrapped vector between 2 particles."""
        pvec = self.wrapped_pvec()
        f_ij = self.psi(pvec,R = self.R,k=self.k)
        pvec_normalised = self.normalise_3darr(pvec)
        # print(pvec_normalised)
        forces = np.zeros(pvec.shape)
        forces[:,:,0] = f_ij*pvec_normalised[:,:,0]
        forces[:,:,1] = f_ij*pvec_normalised[:,:,1]
        return forces
    
    def generate_movement_data(self,T,dt):
        """Generates position and direction data for T time steps of length dt"""
        r_data = np.zeros((T+1,self.N,self.dim))
        direction_data = np.zeros((T+1,self.N,self.dim))
        velocity_data = np.zeros((T+1,self.N,self.dim))
        r_data[0,:,:] = self.r
        direction_data[0,:,:] = self.directions()
        velocity_data[0,:,:] = self.rdot
        for i in range(1,T+1):
            self.update(dt)
            r_data[i,:,:] = self.r
            direction_data[i,:,:] = self.directions()
            velocity_data[i,:,:] = self.rdot
        return r_data,direction_data,velocity_data
   
    def csv_flatten(self,arr):
        """Flattens a 3d array into a 2d array suitable for storing
        in a dataframe"""
        return arr.reshape(arr.shape[0]*arr.shape[1],arr.shape[2])
    
    def get_parameter_dictionary(self):
        ##TODO reverse engineer. Make this the starting point which you pass to ABP
        """Returns a dictionary of the current parameters of 
        the abp object"""
        p_dict = {
            "v_0":self.v_0,
            "box_width":self.box_width,
            "D":self.D,
            "N":self.N,
            "k":self.k}
        return p_dict 

    def get_parameter_suffix(self):
        """Generates a parameter suffix for csv naming"""
        p_dict = self.get_parameter_dictionary()
        out = "__".join([key+"_"+str(p_dict[key]) for key in p_dict])
        return out

    def generate_csv(self,T,dt):
        r,d,v = self.generate_movement_data(T,dt)
        r = self.csv_flatten(r)
        d = self.csv_flatten(d)
        v = self.csv_flatten(v)
        data = np.append(r,d,axis=1)
        data = np.append(data,v,axis=1)
        columns = ["x1","x2","d1","d2","v1","v2"]
        data_frame = pd.DataFrame(data,columns=columns)
        filename = "abp_data__"+self.get_parameter_suffix()+".csv"
        data_frame.to_csv('./data/'+filename)
        return filename

##DISPLAYERS
    def display_state(self):
        fig,ax = plt.subplots()
        s = ax.scatter(self.r[:,0],self.r[:,1])
        q = ax.quiver(self.r[:,0],self.r[:,1],self.directions()[:,0],self.directions()[:,1],
            headlength=10,headaxislength=10,scale=15/self.R)

class Analysis(object):
    def __init__(self,data_name,parameters,T,dt):
        # self.data = open("data_name","r")
        df= pd.read_csv(data_name)
        self.T = T
        self.dt = dt
        self.N = parameters["N"]
        self.r_data = np.array(df[["x1","x2"]]).reshape(T+1,self.N,2)
        self.v_data = np.array(df[["v1","v2"]]).reshape(T+1,self.N,2)
        self.d_data = np.array(df[["d1","d2"]]).reshape(T+1,self.N,2)
        self.p_dict = parameters

    def analytic_msd(self,num_time_steps):
        tau_r =1 #what is persistence time?
        interval = num_time_steps*self.pm["dt"]
        4*self.p_dict["D"]+2*self.p_dict["v_0"]**2*tau_r*(interval-tau_r*(1-np.exp(-interval/tau_r)))
    
    def msd(self,m):
        interval = m*self.dt
        r_diff = np.empty((0,50,2))
        for i in range(0,m):
            if i<self.T%m:
                r_diff = np.append(r_diff,self.r_data[i:-m+i:m]-self.r_data[i+m::m],axis=0)
            else:
                r_diff = np.append(r_diff,self.r_data[i:-2*m+i:m]-self.r_data[i+m:-m+i:m],axis=0) 
        norm_r_diff = lag.norm(r_diff,axis=2)
        msd = np.mean(norm_r_diff**2)
        return msd
    
    def generate_msd_data(self,m_range):
        msd_data = np.zeros(m_range.shape)
        for i,m in enumerate(m_range):
            msd_data[i] = self.msd(m)
        return msd_data

    def animate_movement_patch(self,patch_type="circle"):
        """Animates the movement of the active brownian particles using a 
        matplotlib quiver plot"""
        ##TODO sort arrow scaling
        asp = [10,10,15] ##arrow shape parameters
        sample_rate = 10
        r_data,direction_data,velocity_data = self.r_data,self.d_data,self.v_data
        fig,ax = plt.subplots()
        fig.set_size_inches(8,8)
        ax.set(xlim=(0,self.p_dict["box_width"]),ylim=(0,self.p_dict["box_width"]))
        directions = ax.quiver(r_data[0,:,0],r_data[0,:,1],direction_data[0,:,0],direction_data[0,:,1],
            headaxislength=asp[0],headlength=asp[1],scale=asp[2])
        velocities = ax.quiver(r_data[0,:,0],r_data[0,:,1],velocity_data[0,:,0],velocity_data[0,:,1],color="r",
            headaxislength=asp[0],headlength=asp[1],scale=asp[2])
        for cell in r_data[0,:,:]:
            c = Ellipse(cell,1,1,fill=False,color="k")
            p = ax.add_patch(c)
        def update_anim(i):
            sample = i*sample_rate
            ax.clear()
            ax.set(xlim=(0,self.p_dict["box_width"]),ylim=(0,self.p_dict["box_width"]))
            directions = ax.quiver(r_data[sample,:,0],r_data[sample,:,1],direction_data[sample,:,0],direction_data[sample,:,1],
                headaxislength=asp[0],headlength=asp[1],scale=asp[2])
            velocities = ax.quiver(r_data[sample,:,0],r_data[sample,:,1],velocity_data[sample,:,0],velocity_data[sample,:,1],color="r",
                headaxislength=asp[0],headlength=asp[1],scale=asp[2])
            for cell in r_data[sample,:,:]:
                c = Ellipse(cell,1,1,fill=False,color="k")
                p = ax.add_patch(c)
        anim = animation.FuncAnimation(fig,update_anim,frames=self.T//sample_rate)
        return anim
        