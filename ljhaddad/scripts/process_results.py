import numpy as np
import matplotlib.pyplot as plt
from classes.Nodes import Nodes
def process_results(V_waveform, devices, t_final):
	x = np.arange(0, t_final, 0.001)

	# For generic file, plots all waveforms
	for n in range(V_waveform.shape[0]):
		plt.plot(x, V_waveform[n, :])
	plt.show()

  # For the RL_circuit.json file
	# Plot load voltages
	va_ind = Nodes.node_index_dict["n3_a"] - 1
	vb_ind = Nodes.node_index_dict["n3_b"] - 1
	vc_ind = Nodes.node_index_dict["n3_c"] - 1

	plt.plot(x, V_waveform[va_ind, :])
	plt.plot(x, V_waveform[vb_ind, :])
	plt.plot(x, V_waveform[vc_ind, :])
	plt.title('Three-Phase Voltages')
	plt.legend(['A', 'B', 'C'])
	plt.xlabel('Time (s)')
	plt.show()
	
	# Plot load currents
	ia_ind = Nodes.node_index_dict["v_a"] - 1
	ib_ind = Nodes.node_index_dict["v_b"] - 1
	ic_ind = Nodes.node_index_dict["v_c"] - 1

	plt.plot(x, -V_waveform[ia_ind, :])
	plt.plot(x, -V_waveform[ib_ind, :])
	plt.plot(x, -V_waveform[ic_ind, :])
	plt.title('Three-Phase Load Currents')
	plt.legend(['A', 'B', 'C'])
	plt.xlabel('Time (s)')
	plt.ylabel('Current (A)')
	plt.show()

	# Plot zero-sequence (neutral) currents
	i0 = (-V_waveform[ia_ind, :] - V_waveform[ib_ind, :] 
			- V_waveform[ic_ind, :])
	plt.plot(x, i0)
	plt.title('Zero-Sequence Current')
	plt.xlabel('Time (s)')
	plt.ylabel('Current (A)')
	plt.show()

	# For the IM_circuit.json file
# 	# Plot the stator currents
# 	ids = Nodes.node_index_dict["im1_ids"] - 1
# 	iqs = Nodes.node_index_dict["im1_iqs"] - 1
# 	plt.plot(x, V_waveform[ids, :])
# 	plt.plot(x, V_waveform[iqs, :])
# 	plt.title("Stator Currents")
# 	plt.legend(['I_ds', 'I_qs'])
# 	plt.xlabel('Time (s)')
# 	plt.ylabel('Current (A)')
# 	plt.show()
# 	
# 	# Plot the rotor currents
# 	idr = Nodes.node_index_dict["im1_idr"] - 1
# 	iqr = Nodes.node_index_dict["im1_iqr"] - 1
# 	plt.plot(x, V_waveform[idr, :])
# 	plt.plot(x, V_waveform[iqr, :])
# 	plt.title("Rotor Currents")
# 	plt.legend(['I_dr', 'I_qr'])
# 	plt.xlabel('Time (s)')
# 	plt.ylabel('Current (A)')
# 	plt.show()
# 
# 	# Plot electrical torque
# 	Te_coeff = 3*0.0761
# 	Te_mat = (np.multiply(V_waveform[idr, :], V_waveform[iqs, :]) -
# 			np.multiply(V_waveform[ids, :], V_waveform[iqr, :]))
# 	Te = Te_coeff * Te_mat
# 	plt.plot(x, Te)
# 	plt.title("Electrical Torque")
# 	plt.legend(['T_e'])
# 	plt.xlabel('Time (s)')
# 	plt.ylabel('Torque (N-m)')
# 	plt.show()
# 
# 	# Plot rotor speed
# 	wr =  Nodes.node_index_dict["im1_mec"] - 1
# 	wr_real = V_waveform[wr, :] * -120 / (8 * np.pi)
# 	plt.plot(x, wr_real)
# 	plt.title("Motor Speed")
# 	plt.legend(['w_r'])
# 	plt.xlabel('Time (s)')
# 	plt.ylabel('Speed (RPM)')
# 	plt.show()
