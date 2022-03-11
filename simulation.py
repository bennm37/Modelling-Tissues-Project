import os
import numpy as np
from abp import ABP
from analysis import Analysis
import pandas as pd
import shutil
import pickle

def simulation(project_name,parameters,potential,search_grid,data_type="ben",stats=["rvd","g(r)","anim"]):
    """Search grid is a list of dictionaries of potential parameter values."""
    a = architecture(project_name,search_grid)
    if a == -1:
        if input("Continue (y/n)?   ")=="y":
            print("Populating existing folder")
        else:
            return -1
    if a == 0:
        pickle.dump(search_grid,open(f"data/{project_name}/search_grid.p","wb"))
        n1,n2 = search_grid.shape
        phase_diagram = pd.DataFrame(np.zeros((n1,n2)))
        phase_diagram.to_csv(f"data/{project_name}/phase_diagram.csv",index=False)
    for row in search_grid:
        for dict in row:
            folder_name = f"{project_name}/{get_parameter_suffix(dict)}"
            print(f"Starting {folder_name}")
            potential_parameters = list(dict.values())
            psi = lambda pvec,R: potential(pvec,R,potential_parameters)
            print(stats)
            generate_analyse(psi,parameters,folder_name,data_type,stats)

def delete_project(project_name):
    if input(f"Are you sure you want to delte {project_name}? (y/n)")=="y":
        shutil.rmtree(f"data/{project_name}")
        shutil.rmtree(f"media/{project_name}")
        print(f"Deleted {project_name}")
    else:
        print("Delete aborted.")

def architecture(project_name,search_grid):
    try: 
        os.mkdir(f"data/{project_name}")
        os.mkdir(f"media/{project_name}")
    except FileExistsError:
        print("Project already exists.")
        return -1
    for row in search_grid:
        for dict in row:
            f_name = get_parameter_suffix(dict)
            os.mkdir(f"data/{project_name}/{f_name}")
            os.mkdir(f"data/{project_name}/{f_name}/rvd_data")
            os.mkdir(f"data/{project_name}/{f_name}/alpha_shapes")
            os.mkdir(f"data/{project_name}/{f_name}/g(r)")
            os.mkdir(f"data/{project_name}/{f_name}/msd")
            os.mkdir(f"media/{project_name}/{f_name}")
    return 0 

def make_search_grid(param_names,param_lists,k=None):
    """Param names is a list of p parameter values."""
    shape = [len(l) for l in param_lists]
    sg = np.zeros(shape,dtype=object)
    for i,val0 in enumerate(param_lists[0]):
        for j,val1 in enumerate(param_lists[1]):
            dict = {}
            if k:
                dict["k"] = 1
            dict[param_names[0]] = val0
            dict[param_names[1]] = val1
            sg[i,j] = dict
    return sg

def get_parameter_suffix(dict):
    keys = dict.keys()
    vals = [round(v,2) for v in dict.values()]
    out = "_".join([str(k)+"_"+str(v) for k,v in zip(keys,vals)])
    return out

def generate_analyse(potential,parameters,folder_name,data_type,stats=["rvd","g(r)","anim"]):
    """Possible stats values are rvd,anim,g(r),msd or all"""
    if "rvd" in stats or "all" in stats:
        print("Started rvd")
        particles = ABP(parameters,potential,"rcircle")
        particles.generate_csv(sample_rate = 1000,folder_name = f"{folder_name}/rvd_data")
    a = Analysis(f"data/{folder_name}",parameters,range(parameters["T"]//1000),data_type)
    if "anim" in stats or "all" in stats:
        print("Starting anim")
        anim =  a.animate_movement_patch(sample_rate=1)
        anim.save(f"media/{folder_name}/rvd.mp4")
    if "g(r)" in stats or "all" in stats:
        print("Starting g(r)")
        for i in range(parameters["T"]//1000):
            a.g_r(i,csv=f"data/{folder_name}/g(r)")
    if "msd" in stats or "all" in stats:
        print("msd")
        a.generate_msd_data(csv=f"data/{folder_name}/msd")

def make_param_lists(p1_range,p2_range,n1,n2):
    p1 = np.linspace(p1_range[0],p1_range[1],n1,endpoint=True)
    p2 = np.linspace(p2_range[0],p2_range[1],n2,endpoint=True)
    return p1,p2