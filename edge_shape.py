from matplotlib.patches import Polygon
import matplotlib.animation as animation
from matplotlib.pyplot import plot
from abp import * 
from analysis import Analysis
from parameter_dictionaries import box_width_from_phi,k2_test_dict,pyABP_dict
import pickle

##SETUP
# bw = k2_test_dict["box_width"]
k2 = 0.4
epsilon = 0.15
frame_no = 51
def get_verticies_data(k2,epsilon,frame_no,data_type="ben"):
    try:
        if data_type == "ben":
            folder_name = f"data/alpha_shapes/k2_tests/k2_{k2}_ep_{epsilon}"
            ##UNPICKLING
            verticies = pickle.load(open(f"{folder_name}/as_{frame_no}.p","rb"))
            return verticies
        if data_type == "pyABP":
                folder_name = f"./data/alpha_shapes/pyABP_k2_tests/k2_{k2}_ep_{epsilon}"
                verticies = pickle.load(open(f"{folder_name}/as_{frame_no}.p","rb"))
                return verticies
    except FileNotFoundError:
        print(f"couldn't find file for k2 = {k2},epsilon = {epsilon}, as_{frame_no}.p")
        return None


def get_r_data(k2,epsilon,frame_no,data_type="ben"):
    try:
        if data_type == "ben":
            folder_name = f"data/alpha_shapes/k2_tests/k2_{k2}_ep_{epsilon}"
            ##GETTING R_DATA
            r_data_folder_name = f"k2_tests/k2_test_k_1_k2_{k2}_epsilon_{epsilon}"
            df = pd.read_csv(f"./data/{r_data_folder_name}/data_{frame_no}.csv")
            r_data = np.array(df[["x1","x2"]])
            return r_data
        if data_type == "pyABP":
            root_r_data = f"./data/pyABP_k2_tests/pyABP_k2_{k2}_ep_{epsilon}"
            data = [i.strip().split() for i in open(f"{root_r_data}/data{frame_no}.dat")]
            cols = data[0]
            df = pd.DataFrame(data[1:],columns=cols)
            r_data = np.array(df[["x","y"]],dtype=np.float64).reshape(2000,2)+pyABP_dict["box_width"]/2
            return r_data
    except FileNotFoundError:
        print(f"couldn't find file {folder_name}/as_{frame_no}.p")
        return None
    
def plot_alpha_shape(k2,epsilon,frame_no,ax,data_type="ben",r_data=None):
    ax.set(title="Alpha Shape of Particles")
    verticies = get_verticies_data(k2,epsilon,frame_no,data_type)
    if np.any(r_data == None):
        # print("getting r_data")
        r_data = get_r_data(k2,epsilon,frame_no,data_type)
    if np.any(verticies!=None) and np.any(r_data!=None):
        if data_type =="ben":
            bw = k2_test_dict["box_width"]
        if data_type == "pyABP":
            bw = pyABP_dict["box_width"]
        ps = [Polygon(v+bw/2, fill = False,edgecolor="k") for v in verticies]
        ax.axis("equal")
        ax.set(xlim=(0,bw),ylim=(0,bw))
        ax.scatter(r_data[:,0],r_data[:,1],s=1)
        for p in ps:
            ax.add_patch(p)

# fig,ax = plt.subplots()
# plot_alpha_shape(0.4,0.05,50,ax,"pyABP")
# plt.show()

# #ANIMATING 
# k2s = [0.4,0.8,1.2,1.6,2]
# epsilons = [0.05,0.1,0.15,0.2,0.25,0.3] 
# # k2s = [0.4]
# # epsilons = [0.05]
# for k2 in k2s:
#     print(f"Starting k2 = {k2}")
#     for epsilon in epsilons:
#         print(f"Starting epsilon = {epsilon}")
#         fig,ax = plt.subplots()
#         plot_alpha_shape(k2,epsilon,0,ax)
#         def update(i):
#             ax.clear()
#             plot_alpha_shape(k2,epsilon,i,ax,data_type="pyABP")
#         anim = animation.FuncAnimation(fig,update,frames =100,interval=30)
#         anim.save(f"./media/alpha_shapes/pyABP_k2_{k2}_ep_{epsilon}.mp4")
#         plt.close(fig)
