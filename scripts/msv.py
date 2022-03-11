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

project = "pyABP_k2_tests"
sg = pickle.load(open(f"data/{project}/search_grid.p","rb"))
k2 = [0.4,0.8,1.2,1.6,2]
epsilon = [0.05,0.1,0.15,0.2,0.25,0.3]
# sg = make_search_grid2(["k2","ep"],[k2,epsilon],1)
# sg = pickle.dump(sg,open(f"data/{project}/search_grid.p","wb"))
# print(sg[0][0])
# folder_name = get_parameter_suffix(sg[0][0])
msv_data = np.zeros((5,100))
ep1 = 0.25
samples = [[0.4,ep1],[0.8,ep1],[1.2,ep1],[1.6,ep1],[2,ep1]]
fig,ax = plt.subplots()
for i,s in enumerate(samples):
    print(f"i={i},s={s}")
    k2,ep = s
    folder_name = f"pyABP_k2_{k2}_ep_{ep}"
    a = Analysis(f"data/{project}/{folder_name}",pyABP_dict,range(100),"pyABP")
    msv = a.msv()
    msv_data[i,:] = msv
    ax.plot(msv.T,label=str(s))
ax.legend()
plt.show()