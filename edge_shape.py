from abp import * 
from analysis import Analysis
from parameter_dictionaries import k2_test_dict
from parameter_dictionaries import box_width_from_phi

k2 = 1
epsilon = 0.15
a = Analysis(f"./data/k2_tests/k2_test_k_1_k2_{k2}_epsilon_{epsilon}",k2_test_dict,1000)
N = k2_test_dict["N"]
tri = a.d_triangulation(1)
print(tri.edgess)
fig,ax = plt.subplots()
ax.triplot(tri)
plt.show()