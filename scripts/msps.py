from imports import *
from analysis import *
from parameter_dictionaries import pyABP_delta_dict
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pickle 

# ep = 0.35
# delta = 0.24
epsilons = [0.05,0.1,0.15,0.2,0.25]
deltas = [0.0,0.12,0.24,0.36,0.48,0.6]
project = "C:/Users/bennm/Documents/UNI/Year3/Modelling Tissues Project/data/pyABP_delta_tests"
for ep in epsilons:
    for delta in deltas:
        print(f"Starting epsilon {ep}, delta {delta}.")
        folder_name = f"k_1_epsilon_{ep}_delta_{delta}"
        a = Analysis(f"{project}/{folder_name}",pyABP_delta_dict,range(500),"pyABP")
        file_name = f"C:/Users/bennm/Documents/UNI/Year3/Modelling Tissues Project/data/pyABP_delta_tests/k_1_epsilon_{ep}_delta_{delta}/msps"
        dists,msps = a.generate_msps_data([250,300])
        pickle.dump({"dists":dists,"msps":msps},open(file_name,"wb"))
data = pickle.load(open(file_name,"rb"))
dists = data["dists"]
def histogram_anim(data):
    n = len(data)
    fig,ax = plt.subplots()
    ax.set(xlim=(0,6),ylim=(0,3500))
    hist = ax.hist(data[0],bins=np.linspace(0,6,30))
    def update(i):
        ax.clear()
        ax.set(xlim=(0,6),ylim=(0,3500))
        ax.hist(data[i],bins=np.linspace(0,6,30))
    anim = animation.FuncAnimation(fig,update,n,interval=100)
    return anim 
anim = histogram_anim(dists)
anim.save(file_name+".mp4")
# print(msps)
# print(a.generate_msps_data([100]))
# msps = [3.4830677,3.5363592,3.59017436,3.65558006,3.70191011,3.74345377
# ,3.77808714,3.81222761,3.84671029,3.89441743,3.93186128,3.98124416
# ,4.01551964,4.05984301,4.12701649,4.17726429,4.22532726,4.26647614
# ,4.33893293,4.38196217]
# msps = [4.4652581 ,4.51352725,4.57173366,4.62189095,4.59725754,4.63924145
# ,4.70359401,4.75770695,4.7523359,4.80386573,4.86952245,4.8974456
# ,4.93215283,4.95724681,5.01891604,5.05397461,5.14260332,5.17612001
# ,5.25332799,5.29763967]
# plt.plot(msps)
# plt.show()


