from imports import *
from abp import *
from analysis import *
from parameter_dictionaries import *
from potentials import *

data_type = "pyABP"
project_name = "pyABP_delta_tests"

fig,ax = plt.subplots()
phase_diagram = np.array(pd.read_csv(f"data/{project_name}/phase_diagram.csv"))
n_p1,n_p2 = 6,7
p1_range,p2_range  = (0,0.6),(0.05,0.35)
p1_int,p2_int = (p1_range[1]-p1_range[0])/(n_p1-1),(p2_range[1]-p2_range[0])/(n_p2-1)
##shifted so centre of each rectangle is value
p1 = np.arange(p1_range[0],p1_range[1]+2*p1_int,p1_int)-p1_int/2
p2 = np.arange(p2_range[0],p2_range[1]+2*p2_int,p2_int)-p2_int/2
P1,P2 = np.meshgrid(p1,p2)
ax.set(xlabel="Delta",ylabel="Epsilon",title="Phase Diagram")
ax.pcolormesh(P1,P2,phase_diagram,shading="auto",edgecolor="k")
plt.show()