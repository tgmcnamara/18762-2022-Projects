import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

def lookup_node_index(name, devices):
    nodes = devices['nodes']
    res = -1
    for node in nodes:
        if (node.name == name):
            res = node.index
    return res

def process_results(V_waveform, devices, SETTINGS, step):
    t_final = SETTINGS['Simulation Time']

    nodesvs = ["n3_a","n4_b","n4_c"]
    curr = ["v_a","v_b","v_c"]


    x = np.linspace(0, t_final, V_waveform.shape[0])
    y1 = np.transpose(V_waveform[:,lookup_node_index(nodesvs[0],devices)])

    print(x.shape)
    print(y1.shape)
    fig, ax = plt.subplots()
    ax.plot(x, y1)

    fig.show()
    fig.savefig("fig1.pdf")
    print(np.pi)
