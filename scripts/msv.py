from imports import *
import numpy as np
from analysis import Analysis
from parameter_dictionaries import pyABP_dict
from simulation import get_parameter_suffix,make_search_grid
import pickle
import matplotlib.pyplot as plt


# def make_search_grid2(param_names,param_lists,k=None):
#     """Param names is a list of p parameter values."""
#     shape = [len(l) for l in param_lists]
#     sg = np.zeros(shape,dtype=object)
#     for i,val0 in enumerate(param_lists[0]):
#         for j,val1 in enumerate(param_lists[1]):
#             dict = {}
#             if k:
#                 dict["pyABP"] = ""
#             dict[param_names[0]] = val0
#             dict[param_names[1]] = val1
#             sg[i,j] = dict
#     return sg

project = "pyABP_delta_tests"
sg = pickle.load(open(f"data/{project}/search_grid.p","rb"))
k2 = [0.4,0.8,1.2,1.6,2]
epsilon = [0.05,0.1,0.15,0.2,0.25,0.3]
ep1 = 0.1
samples = [[0.12,ep1],[0.24,ep1],[0.36,ep1]]
# samples = [[0.12,ep1],[0.24,ep1],[0.36,ep1],[0.48,ep1],[0.6,ep1]]
msv_data = np.zeros((5,500))
fig,ax = plt.subplots()
for i,s in enumerate(samples):
    print(f"i={i},s={s}")
    delta,ep = s
    # folder_name = f"pyABP_delta_{delta}_ep_{ep}"
    folder_name = f"k_1_epsilon_{ep}_delta_{delta}"
    a = Analysis(f"data/{project}/{folder_name}",pyABP_dict,range(500),"pyABP")
    msv = a.msv()
    msv_data[i,:] = msv
    ax.plot(msv,label=str(s))
ax.set(xlabel="save no",ylabel="msv",title="MSV of ABP")
ax.legend()
plt.show()