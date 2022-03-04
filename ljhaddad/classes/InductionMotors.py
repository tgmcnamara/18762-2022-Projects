import sys
import numpy as np
from itertools import count
from classes.Nodes import Nodes
# from lib.stamping_functions import stamp_y_sparse, stamp_j_sparse

class InductionMotors:
	def __init__(
		self,
		name,
		phase_a_node,
		phase_b_node,
		phase_c_node,
		power_nom,
		v_nom,
		motor_freq,
		lm,
		rs,
		rr,
		lls,
		llr,
		j,
		tm,
		d_fric,
		n_pole_pairs):
		self.name = name
		self.phase_a_node = phase_a_node
		self.phase_b_node = phase_b_node
		self.phase_c_node = phase_c_node
		self.power_nom = power_nom
		self.v_nom = v_nom
		self.motor_freq = motor_freq
		self.lm = lm
		self.rs = rs
		self.rr = rr
		self.lls = lls
		self.llr = llr
		self.j = j
		self.tm = tm
		self.d_fric = d_fric
		self.n_pole_pairs = n_pole_pairs
		self.lss = self.lls + self.lm
		self.lrr = self.llr + self.lm
		# Below are self-defined
		self.ids_node = name + "_ids"
		self.iqs_node = name + "_iqs"
		self.idr_node = name + "_idr"
		self.iqr_node = name + "_iqr"
		self.mec_node = name + "_mec"
		self.vds_node = name + "_vds"
		self.vqs_node = name + "_vqs"
		self.dt = 0.001
		

	def assign_node_indexes(self,):
		# For convenience
		self.va_index = Nodes.node_index_dict[self.phase_a_node]
		self.vb_index = Nodes.node_index_dict[self.phase_b_node]
		self.vc_index = Nodes.node_index_dict[self.phase_c_node]

		# Entries for each mini-circuit
		Nodes.node_index_dict[self.ids_node] = Nodes.index_counter + 1
		Nodes.node_index_dict[self.iqs_node] = Nodes.index_counter + 2
		Nodes.node_index_dict[self.idr_node] = Nodes.index_counter + 3
		Nodes.node_index_dict[self.iqr_node] = Nodes.index_counter + 4
		Nodes.node_index_dict[self.mec_node] = Nodes.index_counter + 5
		Nodes.node_index_dict[self.vds_node] = Nodes.index_counter + 6
		Nodes.node_index_dict[self.vqs_node] = Nodes.index_counter + 7

		# Indexes for each new element which needs stamping
		self.ids_index = Nodes.index_counter + 1
		self.iqs_index = Nodes.index_counter + 2
		self.idr_index = Nodes.index_counter + 3
		self.iqr_index = Nodes.index_counter + 4
		self.mec_index = Nodes.index_counter + 5
		self.vds_index = Nodes.index_counter + 6
		self.vqs_index = Nodes.index_counter + 7
		
		# Increment index counter
		Nodes.index_counter += 7
		
	def stamp_sparse(self,):
		pass

	# This will be used for the initial stamp which has "old" values
	def stamp_dense(self, Y, J, old_V):
		# EXTRACT OLD QUANTITIES
		va = old_V[self.va_index - 1, 0]
		vb = old_V[self.vb_index - 1, 0]
		vc = old_V[self.vc_index - 1, 0]
		ids = old_V[self.ids_index - 1, 0]
		iqs = old_V[self.iqs_index - 1, 0]
		idr = old_V[self.idr_index - 1, 0]
		iqr = old_V[self.iqr_index - 1, 0]
		vds = old_V[self.vds_index - 1, 0]
		vqs = old_V[self.vqs_index - 1, 0]
		wr = old_V[self.mec_index - 1, 0]
		dt = self.dt/2

		# Calculate historical quantities
		ds_old = self.lss*ids + self.lm*idr + dt*(vds - self.rs*ids)
		qs_old = self.lss*iqs + self.lm*iqr + dt*(vqs - self.rs*iqs)
		dr_old = (self.lrr*idr + self.lm*ids + 
				dt*(-self.rr*idr - (self.lrr*iqr + self.lm*iqs)*wr))
		qr_old = (self.lrr*iqr + self.lm*iqs + 
				dt*(-self.rr*iqr + (self.lrr*idr + self.lm*ids)*wr))
		mec_old = (wr + (dt/self.j)*((3/2)*self.n_pole_pairs*self.lm*
				(idr*iqs - iqr*ids) - self.tm - self.d_fric*wr))

		# Stamp the J matrix with old quantities
		J[self.ids_index - 1, 0] -= ds_old
		J[self.iqs_index - 1, 0] -= qs_old
		J[self.idr_index - 1, 0] -= dr_old
		J[self.iqr_index - 1, 0] -= qr_old
		J[self.mec_index - 1, 0] -= mec_old

		# Stamp the Y matrix with transform coefficients
		# a-phase to d-axis park transform
		# Vds VCVS
		Y[self.vds_index - 1, self.vds_index - 1] += 1
		Y[self.vds_index - 1, self.va_index - 1] += -(2/3)
		Y[self.vds_index - 1, self.vb_index - 1] += -(2/3)*np.cos(-2*np.pi/3)
		Y[self.vds_index - 1, self.vc_index - 1] += -(2/3)*np.cos(2*np.pi/3)
		# Vqs VCVS
		Y[self.vqs_index - 1, self.vqs_index - 1] += 1
		Y[self.vqs_index - 1, self.va_index - 1] += 0
		Y[self.vqs_index - 1, self.vb_index - 1] += -(2/3)*np.sin(-2*np.pi/3)
		Y[self.vqs_index - 1, self.vc_index - 1] += -(2/3)*np.sin(2*np.pi/3)
		# a-phase to d-axis inverse park transform
		# Vas CCCS
		Y[self.va_index - 1, self.ids_index - 1] += 1
		Y[self.va_index - 1, self.iqs_index - 1] += 0
		# Vbs CCCS
		Y[self.vb_index - 1, self.ids_index - 1] += np.cos(-2*np.pi/3)
		Y[self.vb_index - 1, self.iqs_index - 1] += np.sin(-2*np.pi/3)
		# Vcs CCCS
		Y[self.vc_index - 1, self.ids_index - 1] += np.cos(2*np.pi/3)
		Y[self.vc_index - 1, self.iqs_index - 1] += np.sin(2*np.pi/3)
	
	# Called at every iteration of Newton-Raphson
	def stamp_update(self, Y, J, v):
		# "v" is the vector of last iterations' solution
		# Need last iterations gradient in Y, last iterations gradient 
		# multiplied by last iteration's v in J, and last iterations
		# outcome in J as well
		va = v[self.va_index - 1, 0]
		vb = v[self.vb_index - 1, 0]
		vc = v[self.vc_index - 1, 0]
		ids = v[self.ids_index - 1, 0]
		iqs = v[self.iqs_index - 1, 0]
		idr = v[self.idr_index - 1, 0]
		iqr = v[self.iqr_index - 1, 0]
		vds = v[self.vds_index - 1, 0]
		vqs = v[self.vqs_index - 1, 0]
		wr = v[self.mec_index - 1, 0]
		dt = self.dt/2

		# Calculate new quantities
		ds_new = -self.lss*ids - self.lm*idr + dt*(vds - self.rs*ids)
		qs_new = -self.lss*iqs - self.lm*iqr + dt*(vqs - self.rs*iqs)
		dr_new = (-self.lrr*idr - self.lm*ids + 
				dt*(-self.rr*idr - (self.lrr*iqr + self.lm*iqs)*wr))
		qr_new = (-self.lrr*iqr - self.lm*iqs + 
				dt*(-self.rr*iqr + (self.lrr*idr + self.lm*ids)*wr))
		mec_new = (-wr + (dt/self.j)*((3/2)*self.n_pole_pairs*self.lm*
				(idr*iqs - iqr*ids) - self.tm - self.d_fric*wr))

		# Indices so this isn't annoying
		ds = self.ids_index - 1
		qs = self.iqs_index - 1
		dr = self.idr_index - 1
		qr = self.iqr_index - 1
		dsv= self.vds_index - 1
		qsv= self.vqs_index - 1
		mec= self.mec_index - 1

		# Stamp the J matrix with new quantities
		J[ds, 0] -= ds_new
		J[qs, 0] -= qs_new
		J[dr, 0] -= dr_new
		J[qr, 0] -= qr_new
		J[mec, 0] -= mec_new

		# Time to calculate and stamp the partials
		# DS
		Y[ds,ds] += -self.lss - dt*self.rs
		Y[ds,dr] += -self.lm
		Y[ds,dsv] += dt
		
		# QS
		Y[qs,qs] += -self.lss - dt*self.rs
		Y[qs,qr] += -self.lm
		Y[qs,qsv] += dt

		# DR
		Y[dr,ds] += -self.lm
		Y[dr,qs] += -wr*self.lm*dt
		Y[dr,dr] += -self.lrr - dt*self.rr
		Y[dr,qr] += -wr*self.lrr*dt
		Y[dr,mec] += -dt*(self.lrr*iqr + self.lm*iqs)

		# QR
		Y[qr,ds] += wr*self.lm*dt
		Y[qr,qs] += -self.lm
		Y[qr,dr] += wr*self.lrr*dt
		Y[qr,qr] += -self.lrr - dt*self.rr
		Y[qr,mec] += dt*(self.lrr*idr + self.lm*ids)

		# MEC
		Y[mec,ds] += -(dt/self.j)*(3/2)*self.n_pole_pairs*self.lm*iqr
		Y[mec,qs] += (dt/self.j)*(3/2)*self.n_pole_pairs*self.lm*idr
		Y[mec,dr] += (dt/self.j)*(3/2)*self.n_pole_pairs*self.lm*iqs
		Y[mec,qr] += -(dt/self.j)*(3/2)*self.n_pole_pairs*self.lm*ids
		Y[mec,mec] += -1 - (dt/self.j)*self.d_fric

		# Add previous iteration gradient multiplied by previous iteration
		# Now we multiply the previous iteration's solution with this matrix
		# to get the last piece which is stamped in J:
		J_dummy = np.matmul(Y, v)
		J[ds, 0] += J_dummy[ds, 0] 
		J[qs, 0] += J_dummy[qs, 0] 
		J[dr, 0] += J_dummy[dr, 0] 
		J[qr, 0] += J_dummy[qr, 0] 
		J[mec, 0]+= J_dummy[mec, 0]
	
	# Stamp initial conditions for N-R
	def stamp_t0(self, Y, J):
		# Some hot garbage to kick off each simulation
		ds = self.ids_index - 1
		qs = self.iqs_index - 1
		dr = self.idr_index - 1
		qr = self.iqr_index - 1
		mec= self.mec_index - 1
		dsv= self.vds_index - 1
		qsv= self.vqs_index - 1
		Y[ds,ds] = 1
		J[ds, 0] = 0
		Y[qs,qs] = 1
		J[qs, 0] = 0
		Y[dr,dr] = 1
		J[dr, 0] = 0
		Y[qr,qr] = 1
		J[qr, 0] = 0
		Y[mec,mec] = 1
		J[mec, 0] = 0
		J[qsv, 0] = 0
		J[dsv, 0] = 0
		# a-phase to d-axis park transform
		# Vds VCVS
		Y[self.vds_index - 1, self.vds_index - 1] += 1
		Y[self.vds_index - 1, self.va_index - 1] += -(2/3)
		Y[self.vds_index - 1, self.vb_index - 1] += -(2/3)*np.cos(-2*np.pi/3)
		Y[self.vds_index - 1, self.vc_index - 1] += -(2/3)*np.cos(2*np.pi/3)
		# Vqs VCVS
		Y[self.vqs_index - 1, self.vqs_index - 1] += 1
		Y[self.vqs_index - 1, self.va_index - 1] += 0
		Y[self.vqs_index - 1, self.vb_index - 1] += -(2/3)*np.sin(-2*np.pi/3)
		Y[self.vqs_index - 1, self.vc_index - 1] += -(2/3)*np.sin(2*np.pi/3)
		# a-phase to d-axis inverse park transform
		# Vas CCCS
		Y[self.va_index - 1, self.ids_index - 1] += 1
		Y[self.va_index - 1, self.iqs_index - 1] += 0
		# Vbs CCCS
		Y[self.vb_index - 1, self.ids_index - 1] += np.cos(-2*np.pi/3)
		Y[self.vb_index - 1, self.iqs_index - 1] += np.sin(-2*np.pi/3)
		# Vcs CCCS
		Y[self.vc_index - 1, self.ids_index - 1] += np.cos(2*np.pi/3)
		Y[self.vc_index - 1, self.iqs_index - 1] += np.sin(2*np.pi/3)
