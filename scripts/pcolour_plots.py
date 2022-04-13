from cv2 import phase
from imports import *
from abp import *
from analysis import *
from parameter_dictionaries import *
from potentials import *
import matplotlib.cm as cm
from matplotlib.ticker import NullLocator
data_type = "pyABP"
project_name = "pyABP_delta_tests"
def pcolor_plot(grid,ax,lut=None,title="phase diagram",v=[0,3]):
    n_p1,n_p2 = 6,7
    p1_range,p2_range  = (0,0.6),(0.05,0.35)
    p1_int,p2_int = (p1_range[1]-p1_range[0])/(n_p1-1),(p2_range[1]-p2_range[0])/(n_p2-1)
    ##shifted so centre of each rectangle is value
    p1 = np.arange(p1_range[0],p1_range[1]+2*p1_int,p1_int)-p1_int/2
    p2 = np.arange(p2_range[0],p2_range[1]+2*p2_int,p2_int)-p2_int/2
    P1,P2 = np.meshgrid(p1,p2)
    ax.set(xlabel="Delta",ylabel="Epsilon",title=title)
    if lut:
        cmap = cm.get_cmap("bone",lut=lut)
    else:
        cmap = cm.get_cmap("bone")
    cmap.min = 1
    pc = ax.pcolormesh(P1,P2,grid,shading="auto",edgecolor="gray",cmap=cmap,vmin=v[0],vmax=v[1])
    plt.colorbar(pc,ax=ax,ticks=NullLocator())
    # plt.savefig("media/pyABP_delta_tests/summary_plots/phase_diagram.svg")

phase_diagram = np.array(pd.read_csv(f"data/{project_name}/phase_diagram.csv"))
f_dim_grid = np.array([[1.37507212,1.38113175,1.38269964,1.43458266,1.34398063,1.28039125],
    [1.41575556,1.44541427,1.38603855,1.43559965,1.28105936,1.29032573],
    [1.48116301,1.39904548,1.21591871,1.14490603,1.09053599,1.02010995],
    [1.34084081,1.18413568,1.07536945,1.02592696,1.00114051,0.99546964],
    [1.1014183,1.02637667,1.00410698,1.00294387,0.99402374,1.13865486],
    [1.02701672,0.99897232,0.98460742,0.98907842,1.15652174,0.],
    [1.01019665,0.99409117,0.95414168,1.07233735,0.,0.],])
R_g_grid = [[64.87617276,62.96215055,61.18936931,59.75331833,58.85164533,56.65589024]
,[58.26580235,52.63076675,49.50763781,45.41677815,42.42364577,40.02688858]
,[47.76365358,42.42664719,38.86311894,35.32574652,34.49711077,33.60358839]
,[40.36153149,35.51661351,33.87002758,33.27171066,33.21806137,33.08286499]
,[34.52049183,33.575001,33.25096217,33.16999134,32.96470953,15.04622373]
,[33.37811704,33.21784671,33.16727896,31.31359176,24.450146,0.,]
,[33.14281915,33.05333739,27.36216626,26.21216825,0.,0.,]]
print(R_g_grid)
fig,axs = plt.subplots(1,3)
fig.set_size_inches(12,4)
pcolor_plot(phase_diagram,axs[0],lut=4,title="Phase Diagram",v=[0,3])
pcolor_plot(R_g_grid,axs[1],lut=None,title="Radius of Gyration",v=[20,55])
pcolor_plot(R_g_grid,axs[2],lut=4,title="Radius of Gyration",v=[20,55])
# pcolor_plot(f_dim_grid,axs[1],title="Fractal Dimension",v=[0.9,1.5])
# pcolor_plot(f_dim_grid,axs[2],lut=2,title="Fractal Dimension",v=[0.9,1.5])
print(f_dim_grid)
plt.show()