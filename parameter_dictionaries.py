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

pyABP_delta_dict = {
    "R":np.ones(N),
    "N":2000,
    "v_0":0.1,
    "D":0.1,
    "k":1,
    "box_width":200,
    "T":500000,
    "dt": 0.01,
    } 

pyABP_dict = {
    "R":np.ones(N),
    "N":2000,
    "v_0":0.1,
    "D":0.1,
    "k":1,
    "box_width":100,
    "T":100000,
    "dt": 0.01,
    } 

k2_test_dict = {
    "R":np.ones(N),
    "N":N,
    "v_0":0.01,
    "D":0.1,
    "k":1,
    "box_width":box_width_from_phi(N,0.3),
    "T":100000,
    "dt": 0.03,
    } 

delta_test_dict = {
    "R":np.ones(N),
    "N":N,
    "v_0":0.01,
    "D":0.1,
    "k":1,
    "box_width":box_width_from_phi(N,0.3),
    "T":100000,
    "dt": 0.03,
    } 

test_dict = {
    "R":np.ones(N),
    "N":N,
    "v_0":0.01,
    "D":0.1,
    "box_width":box_width_from_phi(N,0.6),
    "T":2000,
    "dt": 0.01,
    }