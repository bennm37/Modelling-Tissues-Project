import numpy as np
import numpy.linalg as lag
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Polygon,Ellipse
import pandas as pd
import os 
from potentials import * 

class ABP():
    ##TODO add **kwargs ? 
    def __init__(self,parameters,potential,type="rbox"):
        "N,v_0=0.1,box_width=10,dim=2,D=0.5,R=1,k=1,potential=short_scale_repulsion"
        """Creates N Active Brownian Particles with uniformly random
        initial positions and directions unless specified. V_0 is the 
        velocity generated by the traction of the crawling particle on 
        the substrate, measured relative to boxwidth, D is the 
        angular diffusivity parameter measured in radians, R is the 
        radius of particles measured in fraction of box width, k is
        the interaction strength (parameter of interaction force)."""
        #TODO protect against bad input
        self.dim = 2
        self.parameters = parameters
        self.R = parameters["R"]
        self.v_0 = parameters["v_0"]
        self.N = parameters["N"]
        self.D = parameters["D"] #diffusion of polarity
        self.box_width = parameters["box_width"]
        self.T = parameters["T"]
        self.dt = parameters["dt"]
        self.psi = potential
        self.initalise(type)
        self.thetas = np.random.uniform(0,2*np.pi,self.N)
        self.rdot = self.v_0*self.directions()+np.sum(self.interaction_forces(),axis=1)
    
    def initalise(self,type):
        if type == "rbox":
            self.r = np.random.uniform(0,self.box_width,(self.N,self.dim))
        if type == "rcircle":
            radius = np.sqrt(self.N)
            np.random.seed(seed = 1915069)
            thetas = np.random.uniform(0,2*np.pi,self.N)
            radii = np.sqrt(np.random.uniform(0,radius**2,self.N))
            self.r = np.transpose([radii*np.cos(thetas),radii*np.sin(thetas)])+np.full((self.N,2),self.box_width/2)
        ##TODO add types ubox,ucircle, rstrip,ustrip
    
    def equilibrate(self,et):
        """Updataes for et time steps"""
        pass
    
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
        return pvec - np.where(np.abs(pvec)>L/2,np.sign(pvec)*L,np.zeros(pvec.shape))
    
    def directions(self):
        return np.array([np.cos(self.thetas),np.sin(self.thetas)]).T
    
    def interaction_forces(self):
        """Uses psi to calculate f_ij, the magnitude of the force between each particle.
        Then multiplies f_ij by the normalised and wrapped vector between 2 particles."""
        pvec = self.wrapped_pvec()
        ##REMOVED k here so specify potential parameters before passing potential
        f_ij = -self.psi(pvec,R = self.R)
        pvec_normalised = self.normalise_3darr(pvec)
        forces = np.zeros(pvec.shape)
        forces[:,:,0] = f_ij*pvec_normalised[:,:,0]
        forces[:,:,1] = f_ij*pvec_normalised[:,:,1]
        return forces
    
    def generate_movement_data(self,sample_rate,debug=False):
        """Generates position and direction data for T time steps of length dt"""
        ##TODO do we need t_data?
        #t_data = np.linspace(0,T,int(T//dt))
        num_samples = np.floor(self.T//sample_rate).astype(np.int)
        r_data = np.zeros((num_samples,self.N,self.dim))
        direction_data = np.zeros((num_samples,self.N,self.dim))
        velocity_data = np.zeros((num_samples,self.N,self.dim))
        r_data[0,:,:] = self.r
        direction_data[0,:,:] = self.directions()
        velocity_data[0,:,:] = self.rdot
        for i in range(1,num_samples):
            for j in range(sample_rate):
                self.update(self.dt)
            r_data[i,:,:] = self.r
            direction_data[i,:,:] = self.directions()
            velocity_data[i,:,:] = self.rdot
        return r_data,direction_data,velocity_data

    def get_parameter_suffix(self):
        """Generates a parameter suffix for csv naming"""
        p_dict = self.parameters
        out = "__".join([key+"_"+str(p_dict[key]) for key in p_dict])
        return out

    def generate_csv(self,sample_rate,folder_name = None):
        """Makes a folder named after parameter values 
        and saves the positions velocities and directions 
        at each sample rate dts"""
        if folder_name:
            folder_name = folder_name
        else:
            folder_name = "abp_data__"+self.get_parameter_suffix()
        try:   
            os.mkdir(f"./data/{folder_name}")
        except FileExistsError:
            print("Using prexisting file.")
        num_samples = int(np.floor(self.T//sample_rate))
        columns = ["x1","x2","d1","d2","v1","v2"]
        data = np.append(self.r,self.directions(),axis=1)
        data = np.append(data,self.rdot,axis=1)
        data_frame = pd.DataFrame(data,columns=columns)
        data_frame.to_csv(f"./data/{folder_name}/data_0.csv",index=False)
        for i in range(1,num_samples):
            for j in range(sample_rate):
                self.update(self.dt)
            data = np.append(self.r,self.directions(),axis=1)
            data = np.append(data,self.rdot,axis=1)
            data_frame = pd.DataFrame(data,columns=columns)
            data_frame.to_csv(f"./data/{folder_name}/data_{i}.csv")
        return folder_name
    
    
class ABP_strip(ABP):
    ##TODO probably neater just to have different initialisation 
    ## and equilibration methods in abp?
    """Derived class to consider rectangular boxes and create"""
    def __init__(self,parameters,potential,rect_dim):
        super().__init__(parameters,potential)
        self.rect_dim = rect_dim

    def update(self,dt):
        self.rdot = self.v_0*self.directions()+np.sum(self.interaction_forces(),axis=1)
        theta_dot = np.random.normal(0,self.D,self.thetas.shape) 
        self.r = (self.r + self.rdot*dt)
        self.r[:,0] = self.r[:,0]%self.rect_dim[0]
        self.r[:,1] = self.r[:,1]%self.rect_dim[1]
        self.thetas = self.thetas + np.sqrt(dt)*theta_dot

    def equilibrate(self,equilibration_time):
        num_steps = int(equilibration_time//self.dt)
        for i in range(num_steps):
            self.update()
        
    def generate_data(self,type,equilibration_time):
        """Sets up particles in desired setup, equilibrates them 
        and then generates movement data."""
        pass
