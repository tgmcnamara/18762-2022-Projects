from platform import node
from telnetlib import SE
from typing import Set
import numpy as np #think need to call np.linalg.solve(Y_mtx,J_mtx)
import scipy as sp
from classes.Capacitors import Capacitors #tried importning scipy but said it was already installed
from classes.Inductors import Inductors
from classes.Nodes import Nodes
from matplotlib import pyplot as plt

def run_time_domain_simulation(devices, V_init, size_Y, SETTINGS):
    d_t = .00001# detlat t time step
    #time = np.linspace((0,SETTINGS['Simulation Time'],d_t)) ####ANNOTHER WAY i WAS TRYING TO INCREMENT MY TIME
    time = np.arange(0,SETTINGS['Simulation Time'],d_t)
    NR = np.arange(0,SETTINGS['Max Iters']) ####setting the maximume number of NR iterations
    size_t = len(time)
    V_waveform =np.zeros((size_Y, size_t)) #INITIALIZES THE WAVEFORM SO I CAN ADD V VECT EACH TIME STEP
    Te_waveform = []#np.zeros((size_Y, 1))
    t_init = 0

    #FIRST CONSTRUCT INITIAL Y AND J matrix
    #THis constructs the overall y and J matrixes
    Y= np.zeros((size_Y,size_Y),dtype=float) #creates the Y matrix of 0s Matrix seems incorrect several rows and columbs of 0
    J = np.zeros((size_Y,1))
    ##initialize linear an non linear y and j matrixs (not sure if any of this is correct for)
    Y_lin = np.copy(Y)
    Y_non_lin =np.copy(Y)
    J_lin = np.copy(J)
    J_non_lin = np.copy(J)

    ########WAS ATTEMPTING TO SEE IF JUST HOW MY INDUCTORS WERE STAMPING
    #for inductors in devices['inductors']:
        #inductors.stamp_short(Y)#,J,d_t,V_init, t)
    #    inductors.stamp_dense(Y,J,d_t,V_init,t_init)
    #    print(inductors)
    #    print(Y)
    #    print(J)
    ############################################
######

    for t_ind in range(len(time)): #going over the entire time
        t = time[t_ind]
        #J = Y*V_init #matrix mupliplication
        
        if t == 0:#####WAS AT TIMES TRYING DO DC ANALYSIS WHEN I T=0
            for resistor in devices['resistors']:
                resistor.stamp_dense(Y_lin)
                #print(Y)
                #print(J)
            for capacitors in devices['capacitors']:
                #capacitors.stamp_open(Y)
                capacitors.stamp_dense(Y_lin,J_lin,d_t,V_init,t)
                #print(Y)
                #print(J)
            for inductors in devices['inductors']:
                #inductors.stamp_short(Y)#,J,d_t,V_init, t)
                inductors.stamp_dense(Y_lin,J_lin,d_t,V_init,t)
                #print(Y)
                #print(J)
            for voltage_sources in devices['voltage_sources']:
                voltage_sources.stamp_dense(Y_lin,J_lin, t)
                #print(Y)
                #print(J)
            ###INDUCTION MOTOR USING T0 STAMP AT FOR T=0
            
            for InductionMotors in devices['induction_motors']:
                InductionMotors.stamp_t0(Y_non_lin)#, 
            Y = Y_lin + Y_non_lin #adds the linear matrix and non lear matrix together
            J = J_lin + J_non_lin
            Y[Nodes.node_index_dict['gnd'],:] = 0
            Y[:,Nodes.node_index_dict['gnd']] = 0
            Y[Nodes.node_index_dict['gnd'], Nodes.node_index_dict['gnd']] = 1
            #induction motor with out using T0 stamp AT T = 0

            # for k in range(len(NR)): #since induction motor is only non linear device  
            # ######INDUCTION  Motor
            #prevkh = V_init
            #     for InductionMotors in devices['induction_motors']:
            #         InductionMotors.stamp_dense(Y_non_lin, J_non_lin, V_init, prevkh,d_t)#, hist,time)#not sure what to do with the T0 stamp
            #     #######
        
            #     Y_nr = Y_lin + Y_non_lin #adds the linear matrix and non lear matrix together
            #     J_nr = J_lin + J_non_lin
            #     #J[Nodes.node_index_dict['gnd'],:] = 0 ###WAS NOT SURE IF I ALSO NEEDED TO SET GND INDX IN JMATRIX TO 0
            #     ######BECAUSE I INDEX GROUND NODES I NEED TO SET GND ROW AND COLM TO 0 BUT THE AT [GND,GND] NEED TO SET TO ONE TO AVOID LINSOLV ERROR
            #     Y_nr[Nodes.node_index_dict['gnd'],:] = 0
            #     Y_nr[:,Nodes.node_index_dict['gnd']] = 0
            #     Y_nr[Nodes.node_index_dict['gnd'], Nodes.node_index_dict['gnd']] = 1
            #     hist_nr =np.amax(prevkh)
            #     prevkh = np.linalg.solve(Y_nr,J_nr)
            #     print(np.amax(prevkh)-hist_nr)
            #     if k == len(NR) or (np.amax(prevkh)-hist_nr)<= SETTINGS["Tolerance"]: #need to add an or condition about if it is below the tollerance
            #         Y = Y_nr
            #         J = J_nr
            #         Y_nr = np.zeros((size_Y,size_Y),dtype=float)#resets Y_nr to zero matrix
            #         J_nr = np.zeros((size_Y,1))
            #         print("k " + str(k))
            #         #HERE WE UPDATE COMPANION MODELS
            #         #need a command to get out of for loop
            #         break
            #     else: 
            #         Y_non_lin =np.zeros((size_Y,size_Y),dtype=float)
            #         J_non_lin = np.zeros((size_Y,1))
            #         Y_nr = np.zeros((size_Y,size_Y),dtype=float)#resets Y_nr to zero matrix
            #         J_nr = np.zeros((size_Y,1))
                
            #print(Y)
            #From what I can tell it seems my last to columbs are zersos if I use cap_open and ind_short commands(THIS IS AN OLD COMMENT)
            
            v = np.linalg.solve(Y,J)
            print(type(v))
            V_waveform[:,t_ind] = v.reshape(-1)#V_waveform[v,t_ind] 
            #print(V_waveform)
            Te_waveform.append(((3/2)*2*0.0761)*(v[10]*v[11]-v[12]*v[9]))
            Prevs_v = v
            prevkh = v
            print(v)

            ######MAY NEED NEWTON RAPHSON HERER#############################
            
            ################################################################

            ############THIS PART WAS WHEN I WAS TRYING TO USE SHORTS AND OPENS FOR DC ANALYSIS AND THEN NEEDED TO RESTAMP BEFORE GOING FORWARD
            #####(reset Y and Z)
            #Y= np.zeros((size_Y,size_Y),dtype=float) #creates the Y matrix of 0s Matrix seems incorrect several rows and columbs of 0
            #J = np.zeros((size_Y,1))
            ##restap it Y and jmatrix 
            #for resistor in devices['resistors']:
            #    resistor.stamp_dense(Y)
            #for capacitors in devices['capacitors']:
            #    capacitors.stamp_dense(Y, J, d_t, Prevs_v, t)
            #for inductors in devices['inductors']:
            #    inductors.stamp_dense(Y,J, d_t, Prevs_v, t)
            #for voltage_sources in devices['voltage_sources']:
            #    voltage_sources.stamp_dense(Y,J, t)
            #################################################
        else:
            ##################Implement Newton Raphson (this may need to go before linsolve)##################################
            
            Y= np.zeros((size_Y,size_Y),dtype=float) #####RESETS Y AND J TO BEING MATRIXES OF 0 AFTER EACH ITERATATION
            J = np.zeros((size_Y,1))
            Y_non_lin =np.zeros((size_Y,size_Y),dtype=float)
            J_non_lin = np.zeros((size_Y,1))
            Y_lin = np.zeros((size_Y,size_Y),dtype=float)#resets Y_nr to zero matrix
            J_lin = np.zeros((size_Y,1))
            for resistor in devices['resistors']:
                 resistor.stamp_dense(Y_lin)
                    #print(Y)
                    #print(J)
            for capacitors in devices['capacitors']:
                capacitors.stamp_dense(Y_lin, J_lin, d_t, Prevs_v, t)
                    #print(Y)
                    #print(J)
            for inductors in devices['inductors']:
                inductors.stamp_dense(Y_lin,J_lin, d_t, Prevs_v, t)
                    #print(Y)
                    #print(J)

            #######
            for voltage_sources in devices['voltage_sources']:
                voltage_sources.stamp_dense(Y_lin,J_lin, t)
                    #print(Y)
                    #print(J)
            for k in range(len(NR)):    
                ######INDUCTION  Motor
                for InductionMotors in devices['induction_motors']:
                    InductionMotors.stamp_dense(Y_non_lin, J_non_lin, Prevs_v, prevkh,d_t)
               
                Y_nr = Y_lin + Y_non_lin #adds the linear matrix and non lear matrix together
                J_nr = J_lin + J_non_lin
                #####(SAME AS COMMENT ON LINE 73)
                Y_nr[Nodes.node_index_dict['gnd'],:] = 0
                Y_nr[:,Nodes.node_index_dict['gnd']] = 0
                Y_nr[Nodes.node_index_dict['gnd'], Nodes.node_index_dict['gnd']] = 1
                hist_nr =np.amax(np.abs(prevkh)) #initially np.amax(prevkh)
                prevkh = np.linalg.solve(Y_nr,J_nr)
                
                #print("approach " + str(np.amax(np.abs(prevkh))-hist_nr))
                #initially was np.abs(np.amax(prevkh)-hist_nr)
                if k == len(NR) or np.abs(np.amax(np.abs(prevkh))-hist_nr)<= SETTINGS["Tolerance"]: #need to add an or condition about if it is below the tollerance
                    #print("k " +str(k))
                    Y = Y_nr
                    J = J_nr
                    #Y_nr = np.zeros((size_Y,size_Y),dtype=float)#resets Y_nr to zero matrix
                    #J_nr = np.zeros((size_Y,1))
                    break
                else:
                    #print("k " +str(k))
                    Y_non_lin =np.zeros((size_Y,size_Y),dtype=float)
                    J_non_lin = np.zeros((size_Y,1))
                    Y_nr = np.zeros((size_Y,size_Y),dtype=float)#resets Y_nr to zero matrix
                    J_nr = np.zeros((size_Y,1))
            #J[Nodes.node_index_dict['gnd'],:] = 0
            v = np.linalg.solve(Y,J)
            #Tm_waveform.append(((((3/2)*InductionMotors[self.n_pole_pairs]*self.lm*prev[self.idr_index])*((3/2)*self.n_pole_pairs*self.lm*prev[self.iqs_index]))-(((3/2)*self.n_pole_pairs*self.lm*prev[self.iqr_index])*((3/2)*self.n_pole_pairs*self.lm*prev[self.ids_index]))))
            #####WAS ATTEMPTING TO MAKE ABSOLUTLY SURE THAT 0 VOLTAGE SOURCE FROM INDCUTOR STAMP WERE REALLY 0
            #print(v[13]-v[6])
            #print(v[15]-v[7])
            #print(v[17]-v[8])
            #print(v[19]-v[12])
            #print(v[21]-v[12])
            #print(v[23]-v[12])
            #print("next")

            #############################################################
            #V_waveform.append(v)
            V_waveform[:,t_ind] = v.reshape(-1)
            Te_waveform.append(((3/2)*2*0.0761)*(v[10]*v[11]-v[12]*v[9]))
            #print(V_waveform)
            Prevs_v = v
            #print(v)
        
    #print(V_waveform)
    
    #################EVERYTHING BELOW THIS POINT IS MY PLOTTING AND PROCESSING
    V_waveform_T = np.transpose(V_waveform)########IF I DID NOT TAKE THE TRANSPOSE I WOULD GET AN ERROR 
    TE = np.array(Te_waveform)
    ####Entire simulation
    plt.plot(time,V_waveform_T)
    #plt.plot(time,V_waveform_T[:,4])
    plt.plot(time,TE)
    plt.xlabel("time")
    plt.ylabel("amplitude")
    plt.title("Induction motor circuit with out L and R over 1 second")
    plt.show()
    
    ##########
    plt.plot(time,V_waveform_T[:,9],label="ids")
    plt.plot(time,V_waveform_T[:,11],label = "iqs")
    #plt.plot(time,V_waveform_T[:,24],label = "I2c")
    plt.xlabel("time")
    plt.ylabel("Amps")
    plt.title("Induction motor stator Current")
    plt.legend()
    plt.show()


    plt.plot(time,V_waveform_T[:,10],label = "idr")
    plt.plot(time,V_waveform_T[:,12],label = "iqr")
    plt.xlabel("time")
    plt.ylabel("Amps")
    plt.title("Induction motor rotor Current")
    plt.legend()
    plt.show()

    plt.plot(time,TE,label = "Te")
    plt.xlabel("time")
    plt.ylabel("Nm")
    plt.title("Induction motor electrical torque")
    plt.legend()
    plt.show()

    plt.plot(time,V_waveform_T[:,13],label = "wr")
    plt.xlabel("time")
    plt.ylabel("rpm")
    plt.title("Induction motor rotor speed")
    plt.legend()
    plt.show()

    #USED FOR WHEN WANT TO FIND VOLTAGE ACCROSS SPECIFIC ELEMENT
    V_load_2a = V_waveform_T[:,6] #- V_waveform_T[:,9] #V_waveform_T[:,12] #- V_waveform_T[:,6] 
    V_load_2b = V_waveform_T[:,7] #- V_waveform_T[:,10]#V_waveform_T[:,12] #- V_waveform_T[:,7]  
    V_load_2c = V_waveform_T[:,8] #- V_waveform_T[:,11]#V_waveform_T[:,12] #- V_waveform_T[:,8]
    plt.plot(time,V_load_2a,label="Va_load")
    plt.plot(time,V_load_2b,label="Vb_load")
    plt.plot(time,V_load_2c,label="Vc_load")
    plt.plot(time,V_waveform_T[:,12])
    #plt.set_title("load voltages")
    #plt.tight_layout()
    #plt.legend()
    #plt.show()#This seems to give the same current plot as simulink even though expecting voltages

    #plt.plot(time,V_waveform_T[:,20],label="phase a")
    #plt.plot(time,V_waveform_T[:,22],label="phase b")
    #plt.plot(time,V_waveform_T[:,24],label="phase c")
    #plt.legend()
    #plt.show()


    #plt.plot(time,V_waveform_T[:,1],label="1")
    #plt.plot(time,V_waveform_T[:,4], label="2")#current
    #plt.legend()
    #plt.show()
    figure, axis = plt.subplots(2,1) ######THIS WAS WORKING BUT NOW GIVES ME A LOT OF ERRORS
    #note only need on set of labels
    ##l1 inductor voltages phase a b c
    axis[1,1].plot(time,V_waveform_T[:,6])#, label='l1_a')
    axis[1,1].plot(time,V_waveform_T[:,7])#, label='l1_b')
    axis[1,1].plot(time,V_waveform_T[:,8])#, label='l1_c')
    #axis[1,0].set_title("v_load voltages")
    ##l1 inductor current phase a b c
    axis[2,1].plot(time,V_waveform_T[:,20])#, label='l1_a')
    axis[2,1].plot(time,V_waveform_T[:,22])#, label='l1_b')
    axis[2,1].plot(time,V_waveform_T[:,24])#, label='l1_c')
    #axis[1,1].set_title("load currents")
    ##l2 inductor voltages phase a b c
    #axis[1,0].plot(time,V_waveform_T[:,6], label='l2_a')
    #axis[1,0].plot(time,V_waveform_T[:,7], label='l2_b')
    #axis[1,0].plot(time,V_waveform_T[:,8], label='l2_c')
    #axis[1,0].set_title("load voltages")
    ##l2 inductor currents phase a b c
    #axis[1,1].plot(time,V_waveform_T[:,9], label='l2_a')
    #axis[1,1].plot(time,V_waveform_T[:,10], label='l2_b')
    #axis[1,1].plot(time,V_waveform_T[:,11], label='l2_c')
    #axis[1,1].set_title("inductor 2 currents")
    ##voltage source voltages phase a b c
    #axis[2,0].plot(time,V_waveform_T[:,12], label='v_a')
    #axis[2,0].plot(time,V_waveform_T[:,13], label='v_b')
    #axis[2,0].plot(time,V_waveform_T[:,14], label='v_c')
    #axis[2,0].set_title("voltage sources voltages")
    ##voltage source currents phase a b c
    #axis[2,1].plot(time,V_waveform_T[:,25], label='phase_a')
    #axis[2,1].plot(time,V_waveform_T[:,26], label='phase_b')
    #axis[2,1].plot(time,V_waveform_T[:,27], label='phase_c')
    #axis[2,1].set_title("voltage sources currents")
    ##load voltages
    #axis[3,0].plot(time,V_waveform_T[:,6], label='phase_a')
    #axis[3,0].plot(time,V_waveform_T[:,7], label='phase_b')
    #axis[3,0].plot(time,V_waveform_T[:,8], label='phase_c')
    #axis[3,0].set_title("load voltages")
    ##Load currents
    #L_curra = V_waveform_T[:,20] + V_waveform_T[:,14] + V_waveform_T[:,25]
    #L_currb = V_waveform_T[:,22] + V_waveform_T[:,16] + V_waveform_T[:,26]
    #L_currc = V_waveform_T[:,24] + V_waveform_T[:,18] + V_waveform_T[:,27]
    #axis[3,1].plot(time,V_load_2a, label='phase_a')
    #axis[3,1].plot(time,, label='phase_b')
    #axis[3,1].plot(time,L_currc, label='phase_c')
    #axis[3,1].set_title("load currents")
    #plt.tight_layout()
    plt.legend()
    plt.show()
    
    #don't really need to return anything
    return V_waveform