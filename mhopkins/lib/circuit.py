import numpy as np
import scipy
import scipy.sparse.linalg
from scipy import sparse as sp
import copy
from classes.CurrentSources import CurrentSources
from classes.Resistors import Resistors

"""
COMPONENT LIST:
stores object circuit element object references
"""
class comp_list():
    def __init__(self):
        self.elements = []
        
    def append(self, val):
        self.elements.append(val)
        
    def remove(self, item):
        self.elements.remove(item)
        
    def get_capacitors(self):
        ref_list = []
        for i in self.elements:
            element_name =  i.__class__.__name__
            if element_name == "Capacitors":
                ref_list.append(i)
        return ref_list
    
    def get_inductors(self):
        ref_list = []
        for i in self.elements:
            element_name = i.__class__.__name__
            if element_name == "Inductors":
                ref_list.append(i)
        return ref_list
                

    def is_null(self):
        if (len(self.elements) == 0):
            return True
        else:
            return False
            
    def __str__(self):
        full_str = "<"
        for i in self.elements:
            full_str += str(i)
            if len(self.elements) > 1:
                full_str += ","
        full_str += ">"
        return full_str
    
    def __repr__(self):
        return self.__str__()

"""
CIRCUIT:
stores groups of circuit elements in a matrix structure.
This is used to generate companion models and update the 
circuit through time. May also be used for visualization
"""
class circuit():
    def __init__(self, size):
        self.obj_mat = []
        for i in range(size):
            new_row = []
            for j in range(size):
                new_row.append(copy.deepcopy(comp_list()))
            self.obj_mat.append(new_row)
        
    def get_size(self):
        return len(self.obj_mat[0])
    
    def __str__(self):
        return str(self.obj_mat)
    
    def __repr__(self):
        return self.__str__()

"""
SIMULATOR:
This parses information from the json, stores circuit models
and solves the circuit output while iterating through time
"""
class Simulator():
    # initialization
    def __init__(self, settings, devices = None, size_Y = 0, node_indices = None):
        """
        the solving dictionary should contain values that help with
        integrations
        """
        self.solving_dict = {"ecm-currents": [],
                             "ecm-voltages": []
                             }
        
        self.t = 0
        self.source_list = []
        self.Y_hist = []
        self.v_hist = []
        self.J_hist = []
        self.t_inc = None
        self.Y = np.zeros((size_Y, size_Y))
        self.v = np.zeros((size_Y, 1))
        self.J = np.zeros((size_Y, 1))
        self.orig_size = size_Y
        self.delta_t = 0.001
        self.settings = settings
        
        if (node_indices != None):
            self.node_map = node_indices
            inv_map = {v: k for k, v in self.node_map.items()}
            self.node_map_reverse = inv_map
            
        if (devices == None):
            pass
        else:
            # creating a list comprehension matrix to store circuit objects
            self.circuit = circuit(size_Y)
            self.create_obj_matrix(devices)
            self.circuit_ecm = copy.deepcopy(self.circuit)
            
            # create list of sources
            for source in devices['voltage_sources']:
                self.source_list.append(source)
                
            self.generate_companion_model(delta_t = self.delta_t)
            self.generate_Y_r()
            self.perform_mna()
            self.delete_ground_node()
            self.solve_Yvj()
            print(self.circuit_ecm)
            
    
    def iterate(self, sparse = False):
        while (self.t < self.settings['Simulation Time']):
            self.iteration(sparse = sparse)
        
    def iteration(self, sparse = False):
        self.update_ecm_values(delta_t = self.delta_t)
        self.init_Yvj(self.orig_size)
        self.generate_Y_r()
        self.perform_mna()
        self.delete_ground_node()
        v_result = self.solve_Yvj(sparse = sparse)
        self.Y_hist.append(self.Y)
        self.J_hist.append(self.J)
        self.v_hist.append(v_result)
        self.t += self.delta_t
    
    def generate_companion_model(self, prev_current = 0, prev_voltage = 0, delta_t = 0.1, norton = True):
        # prev_current and prev_voltage are very important
        for i in range(self.circuit_ecm.get_size()):
            for j in range(self.circuit_ecm.get_size()):
                comp_list = self.circuit_ecm.obj_mat[i][j]
                if (comp_list.is_null() == False):
                    my_inductors = comp_list.get_inductors()
                    my_capacitors = comp_list.get_capacitors()
                    if (norton):
                        # INDUCTORS
                        for x in my_inductors:
                            L = x.l
                            # remove the inductor
                            self.circuit_ecm.obj_mat[i][j].remove(x)
                            # add equivalent circuit
                            ecm_current = CurrentSources("ecm{}{}".format(i,j), self.node_map_reverse[j],
                                                         self.node_map_reverse[i], 
                                                         prev_current + delta_t/ (2*L) + prev_voltage)
                            ecm_current.ecm_type = "l"
                            ecm_current.ecm_val = L
                            # remember the value in the ECM is conductance
                            ecm_resistor = Resistors("ecm{}{}".format(i,j), self.node_map_reverse[i],
                                                      self.node_map_reverse[j], (2*L)/ delta_t)
                            self.circuit_ecm.obj_mat[i][j].append(ecm_current)
                            self.circuit_ecm.obj_mat[i][j].append(ecm_resistor)
                            # log the current source in the solving dictionary so it can be updated
                            self.solving_dict["ecm-currents"].append(ecm_current)
                        # CAPACITORS
                        for x in my_capacitors:
                            C = x.c
                            # remove the inductor
                            self.circuit_ecm.obj_mat[i][j].remove(x)
                            # add equivalent circuit
                            ecm_current = CurrentSources("ecm{}{}".format(i,j), i, j, 
                                                         prev_current + (2*C) / delta_t + prev_voltage)
                            ecm_current.ecm_type = "c"
                            ecm_current.ecm_val = C
                            # remember the value in the ECM is conductance
                            ecm_resistor = Resistors("ecm{}{}".format(i,j), i, j, (2*C) /delta_t)
                            self.circuit_ecm.obj_mat[i][j].append(ecm_current)
                            self.circuit_ecm.obj_mat[i][j].append(ecm_resistor)
                            # log the current source in the solving dictionary so it can be updated
                            self.solving_dict["ecm-currents"].append(ecm_current)
                    
            
            
    def create_obj_matrix(self, devices):
        # add rlc elements
        for i in (devices['resistors'] + devices['inductors'] + devices['capacitors']):
            i_from = i.from_node
            i_to = i.to_node
            self.circuit.obj_mat[self.node_map[i_from]][self.node_map[i_to]].append(copy.deepcopy(i))
        for i in (devices['voltage_sources']):
            i_from = i.vn_node
            i_to = i.vp_node
            self.circuit.obj_mat[self.node_map[i_from]][self.node_map[i_to]].append(copy.deepcopy(i))
            
            
    def _RLC_stamp(self, x, y, matrix, val):
        matrix[x][x] = matrix[x][x] + val
        matrix[y][y] = matrix[y][y] + val
        matrix[x][y] = matrix[x][y] - val
        matrix[y][x] = matrix[y][x] - val
        
        return matrix
    
    def init_Yvj(self, orig_size):
        self.Y = np.zeros((orig_size, orig_size))
        self.v = np.zeros((orig_size, 1))
        self.J = np.zeros((orig_size, 1))
    
    def update_source_list(self):
        for i in range(size):
            for j in range(size):
                element_list = self.circuit_ecm.obj_mat[i][j]
                if (element_list.is_null() == False):
                    for k in element_list.elements:
                        element_name = k.__class__.__name__
                        if (element_name == "VoltageSources"):
                            self.source_list.append()
        
    def update_ecm_values(self, delta_t = 0.1):
        for comp in self.solving_dict["prev-ecm-vals"]:
            # current sources 
            if comp[0] == "I":
                if comp[1].ecm_type == "c":
                    comp[1].amps = 0 # comp[2] + (2 * comp[1].ecm_val / delta_t) * comp[3]
                if comp[1].ecm_type == "l":
                    comp[1].amps = 0 # comp[2] + (delta_t / (2 * comp[1].ecm_val)) * comp[3]
                
                
    def generate_Y_r(self):
        size = len(self.circuit_ecm.obj_mat)
        for i in range(size):
            for j in range(size):
                element_list = self.circuit_ecm.obj_mat[i][j]
                if (element_list.is_null() == False):
                    for k in element_list.elements:
                        element_name = k.__class__.__name__
                        if (element_name == "Resistors" or element_name == "Capacitors" or element_name == "Inductors"):
                            self._RLC_stamp(i,j, self.Y, k.stamp_dense())
                        
        
    def perform_mna(self):
        # preliminaries Y
        size_Y = self.orig_size #self.Y.shape[0]
        new_size = size_Y + len(self.source_list)
        dummy_Y = np.zeros((new_size, new_size))
        dummy_Y[:size_Y,:size_Y] = self.Y
        # preliminaries J
        dummy_J = np.zeros((new_size,1))
        dummy_J[:size_Y] = self.J
        
        s_counter = 0
        # loop through the sources
        for source in self.source_list:
            # update Y
            to_val = source.vp_node
            from_val = source.vn_node
            from_comp = np.eye(new_size)[self.node_map[from_val]]
            to_comp = np.eye(new_size)[self.node_map[to_val]]
            new_row = to_comp - from_comp
            new_col = new_row.T
            dummy_Y[size_Y + s_counter,:] = np.array(new_row)
            dummy_Y[:,size_Y + s_counter] = np.array(new_col)
            # update J
            dummy_J[size_Y + s_counter] = source.get_current_voltage(self.t)
            s_counter += 1
            # add currents
            for cur in self.solving_dict["ecm-currents"]:
                dummy_J[self.node_map[cur.ip_node]] = cur.amps
                dummy_J[self.node_map[cur.in_node]] = -cur.amps
            
            
        self.Y = dummy_Y
        self.J = dummy_J
    
    
    def solve_Yvj(self, sparse = False):
        if (sparse == False):
            # use non-sparse numpy solver
            v = np.linalg.solve(self.Y, self.J)
            print("v", v)
        else:
            self.sY = sp.csr_matrix(self.Y)
            self.sJ = sp.csr_matrix(self.J)
            v = sp.linalg.spsolve(self.sY, self.sJ)
            
        # find ecm values
        
        # CURRENT SOURCES
        self.solving_dict["prev-ecm-vals"] = []
        for i in self.solving_dict["ecm-currents"]:
            prev_cur = i.amps
            vp = vn = 0
            # making sure connections account for ground node being removed
            if (i.ip_node == "gnd"):
                vp = 0
            else:
                vp = v[self.node_map[i.ip_node]]
            #
            if (i.in_node == "gnd"):
                vn = 0
            else:
                vn = v[self.node_map[i.in_node]]
                
            prev_vdrop = float(vp - vn)
            self.solving_dict["prev-ecm-vals"].append(["I", i, prev_cur, prev_vdrop])
        
        return v  
            
    
    def delete_ground_node(self):
        datum = self.node_map["gnd"]
        # delete rows and columns associated with datum/ground node
        self.Y = np.delete(np.delete(self.Y, datum, 0), datum, 1)
        self.J = np.delete(self.J, datum, 0)
         
                