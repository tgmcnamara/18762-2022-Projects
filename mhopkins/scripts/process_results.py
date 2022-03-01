import matplotlib.pyplot as plt
import numpy as np
import random


def get_cmap(n, name='hsv'):
    '''Returns a function that maps each index in 0, 1, ..., n-1 to a distinct 
    RGB color; the keyword argument name must be a standard mpl colormap name.'''
    return plt.cm.get_cmap(name, n)

def create_random_mapping(n):
    mapped_amount = 0
    values_left = list(range(n))
    mapped_values = []
    while (mapped_amount < n):
        v = random.sample(values_left, 1)
        values_left.remove(v[0])
        mapped_values.append(v[0])
        mapped_amount += 1
        
    return mapped_values   
        

def process_results(simulator, SETTINGS):
    
    if (SETTINGS["Plotting"] == False):
        return -1
    
    unknowns = np.array(simulator.v_hist)
    # using the original size (excluding datum node) of the matrix to determine what the voltages are
    N = unknowns.shape[1]
    L = unknowns.shape[0]
    t_final = SETTINGS['Simulation Time']
    
    n = simulator.orig_size - 1
    # first n elements are voltages every other element in the v vector is a source current
    """
    integer_mapping = []
    map = create_random_mapping(N)
    for i,v in enumerate(map):
        integer_mapping.append((i,v))
    """
    
    # determining whether or not we have specific nodes of interest
    try:
        noi = SETTINGS['noi']
        have_noi = (len(noi) > 0)
    except:
        have_noi = False
        noi = []
        
    if (have_noi):
        noi_N = len(noi)
    else:
        noi_N = N
    
    # voltages
    for i in range(n):
        label = ""
        label = "v{}".format(i)
        if ((not have_noi) or (i in noi)):
            label = simulator.node_map_reverse[i]
            plt.plot(np.array(list(range(L))) * simulator.delta_t, unknowns[:,i], 
                     c = get_cmap(N*2)(i*2), label = label)
            plt.legend()
    
    plt.title("Circuit Voltages")
    plt.ylabel("Volts [V]")
    plt.xlabel("Time (seconds)")
    plt.show()
            
    
    # currents
    for i in range(n,N):
        label = ""
        label = "i{}".format(i - n)
        plt.plot(np.array(list(range(L))) * simulator.delta_t, unknowns[:,i], 
                 c = get_cmap((N-n)*2)((i-n)*2), label = label)
        plt.legend()
    
    plt.title("Circuit Currents")
    plt.ylabel("Amps [A]")
    plt.xlabel("Time (seconds)")
    plt.show()
            
    # PLOT THE INDUCTION MOTOR RESULTS
    
    for m in simulator.motor_list:
        fig, ax = plt.subplots(5,1)
        ax[0].plot(np.array(list(range(m.x_hist.shape[0])))*simulator.delta_t, m.x_hist[:,0], label = "ids")
        ax[0].plot(np.array(list(range(m.x_hist.shape[0])))*simulator.delta_t, m.x_hist[:,1], label = "iqs")
        ax[0].legend()
        
        ax[1].plot(np.array(list(range(m.x_hist.shape[0])))*simulator.delta_t, m.x_hist[:,2], label = "idr")
        ax[1].plot(np.array(list(range(m.x_hist.shape[0])))*simulator.delta_t, m.x_hist[:,3], label = "iqr")
        ax[1].legend()
        
        ax[2].plot(np.array(list(range(m.x_hist.shape[0])))*simulator.delta_t, m.x_hist[:,4], label = "wr")
        ax[2].legend()
        
        ax[3].plot(np.array(list(range(m.x_hist.shape[0])))*simulator.delta_t, m.calc_Te(), label = "Te")
        ax[3].legend()
        
        ax[4].plot(np.array(list(range(m.x_hist.shape[0])))*simulator.delta_t, m.x_hist[:,5], label = "vds")
        ax[4].plot(np.array(list(range(m.x_hist.shape[0])))*simulator.delta_t, m.x_hist[:,6], label = "vqs")
        ax[4].legend()
    
        ax[0].set_title("Induction Motor '{}' Results".format(str(m.name)))
        ax[0].set_ylabel("Current [A]")
        ax[1].set_ylabel("Current [A]")
        ax[2].set_ylabel("Ang. Speed [rad/s]")
        ax[3].set_ylabel("Torque [N*m]")
        ax[4].set_ylabel("Voltage [V]")
        ax[4].set_xlabel("Time (s)")
        plt.show()
    