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
        print("values left", values_left)
        print("v",v[0])
        print("mapped values", mapped_values)
        values_left.remove(v[0])
        mapped_values.append(v[0])
        mapped_amount += 1
        
    return mapped_values   
        

def process_results(simulator, SETTINGS):
    print("v", simulator.v_hist[0])
    unknowns = np.array(simulator.v_hist)
    # using the original size (excluding datum node) of the matrix to determine what the voltages are
    N = unknowns.shape[1]
    L = unknowns.shape[0]
    t_final = SETTINGS['Simulation Time']
    
    n = simulator.orig_size - 1
    print("simulator orig size", n)
    # first n elements are voltages every other element in the v vector is a source current
    print("unknowns:", unknowns)
    print("unknown shape", unknowns.shape)
    
    integer_mapping = []
    map = create_random_mapping(N)
    for i,v in enumerate(map):
        integer_mapping.append((i,v))
        
    print("map", map)
    print("integer color code mapping", integer_mapping)
    print("N", N)
    print("unknowns", unknowns[:,0])
    
    for i in range(N):
        label = ""
        if (i < n):
            label = "v{}".format(i)
        else:
            label = "i{}".format(i - n)
        print("did")
        plt.plot(np.array(list(range(L))) * simulator.delta_t, unknowns[:,i], 
                 c = get_cmap(N*2)(integer_mapping[i][1]*2), label = label)
        plt.legend()
    
    plt.ylabel("Volts [v]/ Amps [i]")
    plt.xlabel("Time (seconds)")
    plt.title("")
    plt.show()
            
            
    
    