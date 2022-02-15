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
                 c = get_cmap(N*2)(i*2), label = label)
        plt.legend()
    
    plt.title("Circuit Currents")
    plt.ylabel("Amps [A]")
    plt.xlabel("Time (seconds)")
    plt.show()
            
    
    