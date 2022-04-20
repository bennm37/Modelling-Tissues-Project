import numpy as np
# from numpy.lib.function_base import select 
import numpy.linalg as lag
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Polygon,Ellipse
from matplotlib.tri import Triangulation
from matplotlib.widgets import Slider
# from shapely.geometry import Polygon
import pandas as pd
from potentials import * 
import pickle


class Analysis(object):
    def __init__(self,data_name,parameters,save_range,data_type = "ben"):
        ##TODO exception handling
        ##TODO read in all parameters here?
        self.data_type = data_type
        self.n_saves = len(save_range)
        self.save_range = np.array(list(save_range))
        self.N = parameters["N"]
        self.T = parameters["T"]
        self.dt = parameters["dt"]
        self.box_width = parameters["box_width"]
        self.p_dict = parameters
        self.dn = data_name
        self.load_data()

    ##LOADING CANNED DATA 
    def load_data(self):
        data_name = self.dn
        try:    
            if self.data_type == "ben":
                filenames = [f"data_{i}" for i in self.save_range]
                frames = [pd.read_csv(f"{data_name}/rvd_data/{filename}.csv") for filename in filenames]
                df = pd.concat(frames)
                self.r_data = np.array(df[["x1","x2"]]).reshape(self.n_saves,self.N,2)
                self.v_data = np.array(df[["v1","v2"]]).reshape(self.n_saves,self.N,2)
                self.d_data = np.array(df[["d1","d2"]]).reshape(self.n_saves,self.N,2)
            
            if self.data_type == "pyABP":
                ##TODO frame 0 not showing
                ##TODO take rvd data out of here and put it in simulation
                dat_content = [i.strip().split() for i in open(f"{data_name}/rvd_data/data0.dat")]
                columns = dat_content[0]
                data = np.zeros((self.n_saves,self.N,8))
                for i,index in enumerate(self.save_range):
                    dat_i = [j.strip().split() for j in open(f"{data_name}/rvd_data/data{index}.dat")]
                    data[i,:,:] = dat_i[1:]
                df = pd.DataFrame(data.reshape(self.N*self.n_saves,8),columns=columns)
                self.r_data = np.array(df[["x","y"]]).reshape(self.n_saves,self.N,2)
                self.r_data += self.box_width/2
                self.v_data = np.array(df[["vx","vy"]]).reshape(self.n_saves,self.N,2)
                self.theta_data = np.array(df["theta"]).reshape(self.n_saves,self.N,1)
                self.d_data = np.append(np.cos(self.theta_data),np.sin(self.theta_data),axis = 2)

        except FileNotFoundError:
            ##TODO what to do here? 
            print(f"Couldn't find {data_name}")
            self.r_data = np.zeros((self.n_saves,self.N,2))
            self.v_data = np.zeros((self.n_saves,self.N,2))
            self.d_data = np.zeros((self.n_saves,self.N,2))

    def load_alphashape(self,frame_no,folder_name=None):
        if not folder_name:
            folder_name = f"{self.dn}/alpha_shapes"
        try:
            if self.data_type == "ben":
                ##UNPICKLING
                verticies = pickle.load(open(f"{folder_name}/as_{frame_no}.p","rb"))
                return verticies
            if self.data_type == "pyABP":
                verticies = pickle.load(open(f"{folder_name}/as_{frame_no}.p","rb"))
                return [v+self.box_width/2 for v in verticies]
        except FileNotFoundError:
            print(f"couldn't find file for {folder_name}, as_{frame_no}.p")
            return None

    def load_alphalengths(self,folder_name=None):
        if not folder_name:
            folder_name = f"{self.dn}/alpha_shapes"
        try:
            ##UNPICKLING
            print(folder_name)
            # lengths = [pickle.load(open(f"{folder_name}/al_{frame_no}.p","rb")) for frame_no in self.save_range]
            lengths = pickle.load(open(f"{folder_name}/al.p","rb"))
            return lengths
        except FileNotFoundError:
            print(f"couldn't find all the lengths for {folder_name} in save range. ")
            return None

    ##SUMMARY STATISTICS  
    def analytic_msd(self,num_time_steps):
        tau_r =1 #what is persistence time?
        interval = num_time_steps*self.pm["dt"]
        4*self.p_dict["D"]+2*self.p_dict["v_0"]**2*tau_r*(interval-tau_r*(1-np.exp(-interval/tau_r)))
    
    def msd(self,m):
        """Calculates the mean squared displacement from the data for
        a given time scale m."""
        i_sum = np.sum((self.r_data[m:,:]-self.r_data[:self.n_saves-m,:])**2,axis=1)/self.N
        msd = np.sum(i_sum)/(self.n_saves-m)
        return msd
    
    def generate_msd_data(self,csv = None):
        """Calculates the msd for every time scale m."""
        m_range = np.linspace(0,self.n_saves-1,self.n_saves,dtype=int)
        msd_data = np.zeros(m_range.shape)
        for i,m in enumerate(m_range):
            if self.msd(m)==np.nan:
                print(m)
            msd_data[i] = self.msd(m)
        if csv:
            ##TODO CORRECT THIS TO HAVE TIME AS A COLUMN
            cols = ["m","msd"]
            df = pd.DataFrame(np.array([m_range+self.save_range[0],msd_data]).T,columns=cols)
            df.to_csv(f"{csv}/msd.csv",index=False)
        return msd_data

    def R_g(self,t):
        r = self.r_data[t,:,:]
        com = np.mean(r,axis=0)
        r_com = r-com[np.newaxis,:]
        return np.sqrt(np.sum(np.mean(r_com**2,axis=0)))
    
    def generate_R_g_data(self,csv):
        """Calculates the radius of gyration for every time scale m."""
        m_range = np.linspace(0,self.n_saves-1,self.n_saves,dtype=int)
        msd_data = np.zeros(m_range.shape)
        for i,m in enumerate(m_range):
            if self.msd(m)==np.nan:
                print(m)
            msd_data[i] = self.msd(m)
        if csv:
            ##TODO CORRECT THIS TO HAVE TIME AS A COLUMN
            cols = ["m","msd"]
            df = pd.DataFrame(np.array([m_range+self.save_range[0],msd_data]).T,columns=cols)
            df.to_csv(f"{csv}/msd.csv",index=False)
        return msd_data

    def msv(self,csv = None):
        """Calculates the mean squared velocities for all times."""
        msv_data = np.zeros(self.n_saves)
        t = [s for s in self.save_range]
        for i in range(self.n_saves):
            msv_data[i] = np.sum(self.v_data[i,:,:]**2)/self.N
        if csv:
            cols = ["t","msv"]
            df = pd.DataFrame(np.array([t,msv_data]).T,columns=cols)
            df.to_csv(f"./data/{csv}",index=False)
        return msv_data

    def areas(self,drs,dr):
        # print(drs)
        # return 2*np.pi*drs*dr   
        s = self.box_width/2
        areas = np.zeros(drs.shape)
        for i,r in enumerate(drs):
            if r<=s:
                areas[i] = 2*np.pi*r*dr 
            else:
                theta = np.arccos(s/r)
                # outside1 = 2*s*np.sqrt(r**2-s**2)+2*r**2*(2*np.pi-8*theta)
                # outside2 = 2*s*np.sqrt((r+dr)**2-s**2)+2*(r+dr)**2*(2*np.pi-8*theta)
                # areas[i] = outside2-outside1
                areas[i] = r*dr*(2*np.pi-8*theta)
        return areas
    
    def g_r(self,t,dr=0.1,csv = None):
        """Calculates the radial distribution function of the data at a
        given instant of time."""
        pdist = lag.norm(self.wrapped_pvec(t),axis=2)
        ##want to remove diagonal elements as these are resulting in lots of 0s 
        np.fill_diagonal(pdist,np.NaN)
        pdist = pdist[~np.isnan(pdist)].flatten()
        drs = np.arange(0,self.box_width*np.sqrt(2)/2+dr,dr)
        freq = np.histogram(pdist,bins=drs)[0]
        drs = drs[1:]
        # drs = np.round(drs[1:],2)
        ##we need to normalise by the expected number of particles 
        ##in each band, rho*volume 
        rho = self.N**2 /(self.box_width**2)
        areas = self.areas(drs,dr) 
        norm = 1/(rho*areas)
        normalised_freq = freq*norm
        if csv:
            cols = ["r","g(r)"]
            df = pd.DataFrame(np.array([drs,normalised_freq]).T,columns=cols)
            df.to_csv(f"{csv}/g(r)_{t}.csv",index=False)
        return drs,normalised_freq

    def generate_g_r_data(self,ts,csv=None):
        for i,t in enumerate(ts):
            if i==0:
                drs,f = self.g_r(t)
            else:
                drs,fi = self.g_r(t)
                f += fi
    
        f =  f/len(ts)
        if csv:
            cols = ["r","g(r)"]
            df = pd.DataFrame(np.array([drs,f]).T,columns=cols)
            df.to_csv(f"{csv}/g(r).csv",index=False)
        return drs,f

    ##COMUTATIONAL GEOMETRY ALGOS
    def pvec(self,t):
        """Returns a square matrix of pairwise vectors between all particles """
        r = self.r_data[t,:,:]
        r_tile_v = np.tile(r,(self.N,1)).reshape(self.N,self.N,2)
        r_tile_h = np.tile(r,(1,self.N)).reshape(self.N,self.N,2)
        return r_tile_v-r_tile_h

    def wrapped_pvec(self,t):
        """Returns a square matrix of pairwise vectors between all particles 
        with periodic bounday conditions"""
        L = self.box_width
        pvec = self.pvec(t)
        # if the distance between particles is more than half the width of the
        # box then the distance is measured the other way
        return pvec - np.where(np.abs(pvec)>L/2,np.sign(pvec)*L,np.zeros(pvec.shape))

    def d_triangulation(self,t):
        """Finds the delauny triangulation of the cells 
        at time t."""   
        S = self.r_data[t,:,:]
        return Triangulation(S[:,0],S[:,1])
    
    def convex_hull(self,t):
        """Finds the convex hull of the points at time t
        using the gift wrapping algorithm."""
        pass

    ##PLOTTING
    def animate_movement_patch(self,sample_rate = 10,patch_type="circle",figax = None):
        """Animates the movement of the active brownian particles using a 
        matplotlib quiver plot"""
        ##TODO sort arrow scaling
        asp = [5,5,None,5,0.00001] ##arrow shape parameters hal,hl,s,hw,ml
        r_data,direction_data,velocity_data = self.r_data,self.d_data,self.v_data
        if figax:
            fig,ax = figax
        else:
            fig,ax = plt.subplots()
            fig.set_size_inches(8,8)
        ax.set(xlim=(0,self.box_width),ylim=(0,self.box_width))
        directions = ax.quiver(r_data[0,:,0],r_data[0,:,1],direction_data[0,:,0],direction_data[0,:,1],
            headaxislength=asp[0],headlength=asp[1],scale=asp[2],headwidth=asp[3],minlength=asp[4])
        velocities = ax.quiver(r_data[0,:,0],r_data[0,:,1],velocity_data[0,:,0],velocity_data[0,:,1],color="r",
            headaxislength=asp[0],headlength=asp[1],scale=asp[2],headwidth=asp[3],minlength=asp[4])
        ##This creates circles with diameter 1, not radius 1
        for cell in r_data[0,:,:]:
            ## Fix to make sure ellipse is of radius R_i, not 1
            c = Ellipse(cell,2,2,fill=False,color="k")
            p = ax.add_patch(c)
        def update_anim(i):
            sample = i*sample_rate
            ax.clear()
            ax.set(title=f"frame no {i}")
            ax.set(xlim=(0,self.box_width),ylim=(0,self.box_width))
            directions = ax.quiver(r_data[sample,:,0],r_data[sample,:,1],direction_data[sample,:,0],direction_data[sample,:,1],
                headaxislength=asp[0],headlength=asp[1],scale=asp[2],headwidth=asp[3],minlength=asp[4])
            velocities = ax.quiver(r_data[sample,:,0],r_data[sample,:,1],velocity_data[sample,:,0],velocity_data[sample,:,1],color="r",
                headaxislength=asp[0],headlength=asp[1],scale=asp[2],headwidth=asp[3],minlength=asp[4])
            for cell in r_data[sample,:,:]:
                c = Ellipse(cell,2,2,fill=False,color="k")
                p = ax.add_patch(c)
        anim = animation.FuncAnimation(fig,update_anim,frames=self.n_saves//sample_rate,interval=50)
        return anim

    def animate_alpha_shape(self,folder_name,frame_no,sample_rate = 10):
        fig,ax = plt.subplots()
        self.plot_alpha_shape(ax,folder_name,frame_no)
        def update(i):
            ax.clear()
            self.plot_alpha_shape(ax,folder_name,frame_no)
        anim = animation.FuncAnimation(fig,update,frames =100,interval=30)

    def plot_g_r(self,ax,folder_name=None):
        if not folder_name:
            folder_name = f"{self.dn}/g(r)"
        try:
            # df = pd.read_csv(f"./data/g_r/N100_k2_centretests/k2_{k2}_epsilon_{epsilon}")
            print(f"{folder_name}/g(r).csv")
            df = pd.read_csv(f"{folder_name}/g(r).csv")
            r = df["r"]
            g_r = df["g(r)"]
            ax.set(xlim=(0,6))
            ax.plot(r,g_r)
            ax.set(title = "Radial Distribution Function")
        except FileNotFoundError:
            ax.set(title = f"No g(r) data.")

    def plot_potential(self,ax,potential,potential_parameters):
        num_samples = 150
        R = np.ones(1)
        data = np.zeros((num_samples))
        X = np.linspace(0,5,num_samples)
        for i,x in enumerate(X):
            pvec = np.array([[[x,0]]])
            ##TODO change potentials to take in one parameters arg not individual
            data[i] = potential(pvec,R,potential_parameters)[0,0]
        if not ax:
            fig,ax = plt.subplots() 
        ax.set(ylim=(-0.3,1.2))
        p = ax.plot(X,data)
        return p,ax

    def parameter_potential_plot(self,potential,slider_names,slider_ranges=None,slider_init=None):
        n_sliders = len(slider_names)
        if not slider_ranges:
            slider_ranges = [[0,2] for i in range(n_sliders)]
        if not slider_init:
            slider_init = [1 for i in range(n_sliders)]
        # Create the figure and the vf that we will manipulate

        parameters = slider_init
        fig,axs = plt.subplots(1,2)
        ax,ax1 = axs
        # ax.set(xlim=(0,4),ylim=(-2,2))
        p,ax = self.plot_potential(ax,potential,parameters)
        # adjust the main plot to make room for the sliders
        plt.subplots_adjust(bottom=0.1*n_sliders)

        # Make a horizontal slider to control alpha
        slider_ax = [None for i in range(n_sliders)]
        sliders = [None for i in range(n_sliders)]
        for i,name in enumerate(slider_names):
            slider_ax[i] = plt.axes([0.25, 0.1+0.05*i, 0.5, 0.03])
            sliders[i] = Slider(
                slider_ax[i],
                label = name,
                valmin=slider_ranges[i][0],
                valmax=slider_ranges[i][1],
                valinit = slider_init[i])

        def update(val):
            parameters = [s.val for s in sliders]
            ax.clear()
            p,ax1 = self.plot_potential(ax,potential,parameters)

        # register the update function with each slider
        for s in sliders:
            s.on_changed(update)
        ##NOTE if creating sliders in a function, return them ! Otherwise they freeze (weak refs) 
        return sliders

    def plot_alphashape(self,ax,frame_no,folder_name=None,single=False):
        verticies = self.load_alphashape(frame_no,folder_name)
        try:
            ps = [Polygon(v, fill = False,edgecolor="k") for v in verticies]
        except TypeError:
            ax.set(title= "No alphashape data.")
            return -1           
        ax.axis("equal")
        ax.set(xlim=(0,self.box_width),ylim=(0,self.box_width))
        if not single:
            ax.scatter(self.r_data[frame_no,:,0],self.r_data[frame_no,:,1],s=2)
        else:
            ax.scatter(self.r_data[0,:,0],self.r_data[0,:,1],s=2)
        for p in ps:
            ax.add_patch(p)

    def plot_alpha_length(self,ax,label="line"):
        lengths = self.load_alphalengths()
        length_sum = [sum(l) for l in lengths]
        save_unit = 10 ##how many time units between saves
        t = [save_unit*save for save in self.save_range]
        ax.plot(t,length_sum,label=label)

    def plot_particles(self,ax,frame_no):
        asp = [15,15,10,7.5,1] ##hal,hl,s,hw,ms
        r = self.r_data[frame_no,:,:]
        d = self.d_data[frame_no,:,:]
        v = self.v_data[frame_no,:,:]
        ax.set(xlim=(0,self.p_dict["box_width"]),ylim=(0,self.p_dict["box_width"]))
        directions = ax.quiver(r[:,0],r[:,1],d[:,0],d[:,1])
        velocities = ax.quiver(r[:,0],r[:,1],v[:,0],v[:,1],color="r",
            headaxislength=asp[0],headlength=asp[1],scale=asp[2],headwidth=asp[3],minshaft=asp[4])
        for cell in r[:,:]:
            c = Ellipse(cell,2,2,fill=False,color="k")
            p = ax.add_patch(c)
        