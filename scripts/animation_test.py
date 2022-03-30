import matplotlib
from imports import *
from analysis import Analysis
import matplotlib.pyplot as plt
from parameter_dictionaries import *
from matplotvideo import attach_video_player_to_figure

a = Analysis("./data/pyABP_delta_tests/k_1_epsilon_0.2_delta_0.36",pyABP_delta_dict,range(0,500),"pyABP")
fig,ax = plt.subplots()
fig.set_size_inches(8,8)
def on_frame(video_timestamp,ax):
    ax.set(title = f"timestamp = {video_timestamp}")
    fig.canvas.draw()
attach_video_player_to_figure(fig,"media/alpha_shapes/pyABP_k2_0.4_ep_0.1.mp4",on_frame,ax=ax)
# plt.show()