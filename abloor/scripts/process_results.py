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
    #Plot figures associated with RL_circuit with 3 phases
        fig, (ax1) = plt.subplots(1,1)
        fig2, (ax2) = plt.subplots(1,1)

        for wav in nodesvs:
            #plot voltagess at node from nodesvs
            y =  np.transpose(V_waveform[:,lookup_node_index(wav,devices)])
            ax1.plot(x,y,label = wav)

        for wav in curr:
            #plot currents drawn from voltage sources from curr
            y =  np.transpose(V_waveform[:,lookup_vs_index(wav,devices)])
            ax2.plot(x,y,label = ("curr from " + wav))

        ax1.legend()
        ax1.set_xlabel("Time (s)")
        ax1.set_ylabel("Voltages (V)")
        ax1.set_title("Fig 1: Node Voltages of RL Circuit")

        ax2.legend()
        ax2.set_xlabel("Time(s)")
        ax2.set_ylabel("Currents (A)")
        ax2.set_title("Fig 2: Phase Current of RL Circuit")

        fig.show()
        fig.savefig("RL.pdf")
        fig2.show()
        fig2.savefig("RL2.pdf")

    im_index = -1
    A = 0;
    for im in devices['induction_motors']:
        im_index = im.index
        A = 3*im.n_pole_pairs*im.lm/2

    if (SETTINGS['Plots'] == "IM") and (im_index != -1):
    #Plot figures associated with IM_circuit for single (last) Induction Motor
    #Expects time of simulation/step size >= 500
    #Also reports approximate magnitues of waveforms plotted in steady state
        fig, (ax1) = plt.subplots(1,1)
        fig2, (ax2) = plt.subplots(1,1)
        fig3, (ax3) = plt.subplots(1,1)

        labels = ["ids","iqs","idr","iqr"]
        for i in range(0,4):
            y = np.transpose(V_waveform[:,(im_index + i)])
            ax1.plot(x,y, label = labels[i])
            val = np.amax(y[450:499])
            print("Mag of " + labels[i] + ": ")
            print(val)

        ax1.legend()
        ax1.set_xlabel("Time(s)")
        ax1.set_ylabel("Current (A)")
        ax1.set_title("Fig 3: Induction Motor Currents")

        ax2.plot(x[0:499],np.transpose(V_waveform[:,(im_index + 4)])[0:499])
        print("Mag of wr:")
        print(np.average(np.transpose(V_waveform[:,(im_index + 4)])[450:499]))
        ax2.set_xlabel("Time(s)")
        ax2.set_ylabel("wr (rad/s)")
        ax2.set_title("Fig 4: Induction Motor Speed")


        ids = np.transpose(V_waveform[:,(im_index)])
        iqs = np.transpose(V_waveform[:,(im_index + 1)])
        idr = np.transpose(V_waveform[:,(im_index + 2)])
        iqr = np.transpose(V_waveform[:,(im_index + 3)])
        idrqs = np.multiply(idr, iqs)
        iqrds = np.multiply(iqr, ids)
        T = A*(idrqs - iqrds)
        print("Mag of Te:")
        print(np.amax(T[450:499]))
        ax3.plot(x, T)
        ax3.set_xlabel("Time(s)")
        ax3.set_ylabel("Electrical Torque (Nm)")
        ax3.set_title("Fig 5: Induction Motor Electrical Torque")



        fig.show()
        fig.savefig("IM.pdf")
        fig2.show()
        fig2.savefig("IM2.pdf")
        fig3.show()
        fig3.savefig("IM3.pdf")

