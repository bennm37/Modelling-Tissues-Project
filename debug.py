from abp import * 
def N_given_packing_fraction(phi,box_width):
    N = np.floor((phi*box_width**2)/np.pi)
    return int(N)
box_width = 20
glass = {"N":N_given_packing_fraction(1,box_width),"v_0":0.01,"D":0.1} 