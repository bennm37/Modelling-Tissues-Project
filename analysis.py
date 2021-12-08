import numpy as np
# from numpy.lib.function_base import select 
import numpy.linalg as lag
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Polygon,Ellipse
import pandas as pd
import os 
from potentials import * 


class Analysis(object):
    def __init__(self,data_name,parameters,n_saves,data_type = "ben"):
        self.n_saves = n_saves
        self.N = parameters["N"]
        self.p_dict = parameters
        self.T = parameters["T"]
        self.dt = parameters["dt"]

        if data_type == "ben":
            filenames = [f"data_{i}" for i in range(self.n_saves)]
            frames = [pd.read_csv(f"{data_name}/{filename}.csv") for filename in filenames]
            df = pd.concat(frames)
            self.r_data = np.array(df[["x1","x2"]]).reshape(self.n_saves,self.N,2)
            self.v_data = np.array(df[["v1","v2"]]).reshape(self.n_saves,self.N,2)
            self.d_data = np.array(df[["d1","d2"]]).reshape(self.n_saves,self.N,2)
        
        if data_type == "pyABP":
            dat_content = [i.strip().split() for i in open(f"{data_name}/data1.dat")]
            columns = dat_content[0]
            data = np.zeros((self.n_saves,self.N,8))
            for i in range(0,self.n_saves):
                dat_i = [i.strip().split() for i in open(f"{data_name}/data{i}.dat")]
                data[i,:,:] = dat_i[1:]
            df = pd.DataFrame(data.reshape(self.N*self.n_saves,8),columns=columns)
            self.r_data = np.array(df[["x1","x2"]]).reshape(self.n_saves,self.N,2)
            self.v_data = np.array(df[["v1","v2"]]).reshape(self.n_saves,self.N,2)
            self.theta_data = np.array(df["theta"]).reshape(self.n_saves,self.N,1)
            self.d_data = np.append(np.cos(self.theta_data),np.sin(self.theta_data),axis = 2)

    def analytic_msd(self,num_time_steps):
        tau_r =1 #what is persistence time?
        interval = num_time_steps*self.pm["dt"]
        4*self.p_dict["D"]+2*self.p_dict["v_0"]**2*tau_r*(interval-tau_r*(1-np.exp(-interval/tau_r)))
    
    def msd(self,m):
        i_sum = np.sum((self.r_data[m:,:]-self.r_data[:self.n_saves-m,:])**2,axis=1)
        msd = np.sum(i_sum)/(self.n_saves-m)
        return msd
    
    def generate_msd_data(self):
        m_range = np.linspace(0,self.n_saves,self.n_saves,dtype=int)
        msd_data = np.zeros(m_range.shape)
        for i,m in enumerate(m_range):
            if self.msd(m)==np.nan:
                print(m)
            msd_data[i] = self.msd(m)
        return msd_data

    def plot_frame(self,frame_no):
        asp = [10,10,15]
        r_data,direction_data,velocity_data = self.r_data,self.d_data,self.v_data
        fig,ax = plt.subplots()
        fig.set_size_inches(8,8)
        ax.set(xlim=(0,self.p_dict["box_width"]),ylim=(0,self.p_dict["box_width"]))
        directions = ax.quiver(r_data[frame_no,:,0],r_data[frame_no,:,1],direction_data[frame_no,:,0],direction_data[0,:,1],
            headaxislength=asp[0],headlength=asp[1],scale=asp[2])
        velocities = ax.quiver(r_data[frame_no,:,0],r_data[frame_no,:,1],velocity_data[frame_no,:,0],velocity_data[0,:,1],color="r",
            headaxislength=asp[0],headlength=asp[1],scale=asp[2])
        for cell in r_data[frame_no,:,:]:
            c = Ellipse(cell,1,1,fill=False,color="k")
            p = ax.add_patch(c)

    def animate_movement_patch(self,sample_rate =10,patch_type="circle"):
        """Animates the movement of the active brownian particles using a 
        matplotlib quiver plot"""
        ##TODO sort arrow scaling
        asp = [10,10,15] ##arrow shape parameters
        r_data,direction_data,velocity_data = self.r_data,self.d_data,self.v_data
        fig,ax = plt.subplots()
        fig.set_size_inches(8,8)
        ax.set(xlim=(0,self.p_dict["box_width"]),ylim=(0,self.p_dict["box_width"]))
        directions = ax.quiver(r_data[0,:,0],r_data[0,:,1],direction_data[0,:,0],direction_data[0,:,1],
            headaxislength=asp[0],headlength=asp[1],scale=asp[2])
        velocities = ax.quiver(r_data[0,:,0],r_data[0,:,1],velocity_data[0,:,0],velocity_data[0,:,1],color="r",
            headaxislength=asp[0],headlength=asp[1],scale=asp[2])
        ##This creates circles with diameter 1, not radius 1
        for cell in r_data[0,:,:]:
            ## Fix to make sure ellipse is of radius R_i, not 1
            c = Ellipse(cell,2,2,fill=False,color="k")
            p = ax.add_patch(c)
        def update_anim(i):
            sample = i*sample_rate
            ax.clear()
            ax.set(title=f"frame no {i}")
            ax.set(xlim=(0,self.p_dict["box_width"]),ylim=(0,self.p_dict["box_width"]))
            directions = ax.quiver(r_data[sample,:,0],r_data[sample,:,1],direction_data[sample,:,0],direction_data[sample,:,1],
                headaxislength=asp[0],headlength=asp[1],scale=asp[2])
            velocities = ax.quiver(r_data[sample,:,0],r_data[sample,:,1],velocity_data[sample,:,0],velocity_data[sample,:,1],color="r",
                headaxislength=asp[0],headlength=asp[1],scale=asp[2])
            for cell in r_data[sample,:,:]:
                c = Ellipse(cell,2,2,fill=False,color="k")
                p = ax.add_patch(c)
        anim = animation.FuncAnimation(fig,update_anim,frames=self.n_saves//sample_rate,interval=50)
        return anim
        