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

def lookup_vs_index(name, devices):
    vsources = devices['voltage_sources']
    res = -1
    for vs in vsources:
        if (vs.name == name):
            res = vs.index
    return res


def process_results(V_waveform, devices, SETTINGS, step):
    t_final = SETTINGS['Simulation Time']

    nodesvs = ["n3_a","n4_b","n4_c"]
    curr = ["v_a","v_b","v_c"]


    x = np.linspace(0, t_final, V_waveform.shape[0])
    y1 = np.transpose(V_waveform[:,lookup_node_index(nodesvs[0],devices)])
    y2 = np.transpose(V_waveform[:,lookup_node_index(nodesvs[1],devices)])
    y3 = np.transpose(V_waveform[:,lookup_node_index(nodesvs[2],devices)])

    y1b = -np.transpose(V_waveform[:,lookup_vs_index(nodesvs[0],devices)])
    y2b = -np.transpose(V_waveform[:,lookup_vs_index(nodesvs[1],devices)])
    y3b = -np.transpose(V_waveform[:,lookup_vs_index(nodesvs[2],devices)])


    print(x.shape)
    print(y1.shape)

    fig, (ax1,ax2) = plt.subplots(2,1)
    ax1.plot(x, y1, x, y2, x, y3)

    ax2.plot(x, y1b, x, y2b, x, y3b)

    fig.show()
    fig.savefig("fig1.pdf")
    print(np.pi)
