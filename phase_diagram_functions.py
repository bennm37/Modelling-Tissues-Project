from abp import *
from analysis import *
from parameter_dictionaries import *
from potentials import *
from matplotlib.gridspec import GridSpec
from plotting_potentials import plot_potential

# def plot_particles(k2,epsilon,frame_no,ax,p_dict = k2_test_dict,data_type= "ben"):
#     ax.set(title = f"Particles at {frame_no}000 dt")
#     N = p_dict["N"]
#     if data_type == "ben":
#         folder_name = "./data/k2_tests/"
#         try:
#             data = pd.read_csv(folder_name +f"k2_test_k_1_k2_{k2}_epsilon_{epsilon}/data_{frame_no}.csv")
#             r_data = np.array(data[["x1","x2"]]).reshape(N,2)
#             v_data = np.array(data[["v1","v2"]]).reshape(N,2)
#             d_data = np.array(data[["d1","d2"]]).reshape(N,2)
#         except FileNotFoundError:
#             ax.clear()
#             return 1,None
#     if data_type== "pyABP":
#         try:
#             folder_name = f"./data/pyABP_k2_tests/pyABP_k2_{k2}_ep_{epsilon}"
#             dat_content = [i.strip().split() for i in open(f"{folder_name}/data{frame_no}.dat")]
#             columns = dat_content[0]
#             data = np.array(dat_content[1:])
#             df = pd.DataFrame(data.reshape(N,8),columns=columns)
#             r_data = np.array(df[["x","y"]]).reshape(N,2).astype(np.float64)
#             r_data += p_dict["box_width"]/2
#             v_data = np.array(df[["vx","vy"]]).reshape(N,2).astype(np.float64)
#             theta_data = np.array(df["theta"]).reshape(N,1).astype(np.float64)
#             d_data = np.append(np.cos(theta_data),np.sin(theta_data),axis = 1)
#         except FileNotFoundError:
#             ax.clear()
#             return 1,None

    # asp = [15,15,2,7.5,1]
    # ax.set(xlim=(0,p_dict["box_width"]),ylim=(0,p_dict["box_width"]))
    # directions = ax.quiver(r_data[:,0],r_data[:,1],d_data[:,0],d_data[:,1])
    # velocities = ax.quiver(r_data[:,0],r_data[:,1],v_data[:,0],v_data[:,1],color="r",
    #     headaxislength=asp[0],headlength=asp[1],scale=asp[2],headwidth=asp[3],minshaft=asp[4])
    # for cell in r_data[:,:]:
    #     c = Ellipse(cell,2,2,fill=False,color="k")
    #     p = ax.add_patch(c)
    # return 0,r_data


# def plot_g_r(a,k2,epsilon,ax,data_type="ben"):
#     if data_type == "ben":
#         folder_name = f"./data/g_r/N100_k2_centretests"
#         file_name = f"k2_{k2}_epsilon_{epsilon}"
#     if data_type == "pyABP":
#         folder_name = f"./data/g_r/pyABP_k2"
#         file_name = f"k2_{k2}_epsilon_{epsilon}"
#     a.plot_g_r(ax,folder_name,file_name)
