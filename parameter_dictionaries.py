import numpy as np
def box_width_from_phi(N,phi):
    return np.round(np.sqrt(N*np.pi/phi),1)  
N = 100
glass_dict = {
    "N":N,
    "v_0":0.01,
    "D":0.1,
    "k":1,
    "box_width":box_width_from_phi(N,1)
    } 

dense_liquid_dict = {
    "N":N,
    "v_0":0.1,
    "D":0.1,
    "k":1,
    "box_width":box_width_from_phi(N,1)
    }

phase_seperated_dict = {
    "N":N,
    "v_0":0.1,
    "D":0.001,
    "k":1,
    "box_width":box_width_from_phi(N,0.6)
    } 
normal_liquid_dict = {
    "N":N,
    "v_0":0.1,
    "D":0.1,
    "k":1,
    "box_width":box_width_from_phi(N,0.6)
    } 