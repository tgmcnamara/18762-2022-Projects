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

    nodesvs = ["n3_a","n3_b","n3_c"]
    curr = ["v_a","v_b","v_c"]


    x = np.linspace(0, t_final, V_waveform.shape[0])

    if (SETTINGS['Plots'] == "RL"):

        fig, (ax1,ax2) = plt.subplots(2,1)

        for wav in nodesvs:
            y =  np.transpose(V_waveform[:,lookup_node_index(wav,devices)])
            ax1.plot(x,y,label = wav)

        for wav in curr:
            y =  np.transpose(V_waveform[:,lookup_vs_index(wav,devices)])
            ax2.plot(x,y,label = ("curr from " + wav))

        ax1.legend(bbox_to_anchor=(0,1,1,.1),ncol=3,mode="expand", loc="lower left")
        ax2.legend(bbox_to_anchor=(0,1,1,.1),ncol=3,mode="expand", loc="lower left")

        fig.show()
        fig.savefig("RL.pdf")

    im_index = -1
    for im in devices['induction_motors']:
        im_index = im.index

    if (SETTINGS['Plots'] == "IM") and (im_index != -1):
        fig, (ax1, ax2) = plt.subplots(2,1)
        for i in range(0,4):
            y = np.transpose(V_waveform[:,(im_index + i)])
            ax1.plot(x,y)

        ax2.plot(x,np.transpose(V_waveform[:,(im_index + 4)]))
        fig.show()
        fig.savefig("IM.pdf")

