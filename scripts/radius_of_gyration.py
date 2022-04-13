from numpy import newaxis
from imports import *
from analysis import *
from parameter_dictionaries import pyABP_delta_dict

epsilon = [0.05,0.1,0.15,0.2,0.25,0.3,0.35]
deltas = [0.0,0.12,0.24,0.36,0.48,0.6]
# epsilon = [0.35]
# deltas = [0.6]
R_g_grid = np.zeros((len(epsilon),len(deltas)))
for i,ep in enumerate(epsilon):
    for j,delt in enumerate(deltas):
        print(f"Starting ep = {ep},delt = {delt}")
        a = Analysis(f"data/pyABP_delta_tests/k_1_epsilon_{ep}_delta_{delt}",pyABP_delta_dict,range(500),"pyABP")
        R_g_grid[i,j] = a.R_g(499)
print(R_g_grid)