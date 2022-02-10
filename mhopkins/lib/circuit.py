import numpy as np
import scipy
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
    def __init__(self, devices = None, size_Y = 0, node_indices = None):
        """
        the solving dictionary should contain values that help with
        integrations
        """
        self.solving_dict = {"ecm-currents": [],
                             "ecm-voltages": []
                             }
        
        self.timestep = 0
        self.source_list = []
        self.Y_hist = None
        self.v_hist = None
        self.J_hist = None
        self.t_inc = None
        self.Y = np.zeros((size_Y, size_Y))
        self.v = np.zeros((size_Y, 1))
        self.J = np.zeros((size_Y, 1))
        self.orig_size = size_Y
        
        if (node_indices != None):
            self.node_map = node_indices
            
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
                
            #self.init_Y(devices)
            self.generate_companion_model()
            self.generate_Y_r()
            self.perform_mna()
            self.delete_ground_node()
            print(self.circuit_ecm)
     
    def init_solver(self, settings):   
        self.solving_dict["sim_time"] = settings['Simulation Time']
        self.solving_dict["tol"] = settings['Tolerance']  # NR solver tolerance
        self.solving_dict["max_iters"] = settings['Max Iters']  # maximum NR iteration
    
    def generate_companion_model(self, prev_current = 0.1, prev_voltage = 0.1, delta_t = 0.1, norton = True):
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
                            ecm_current = CurrentSources("ecm{}{}".format(i,j), j, i, 
                                                         prev_current + delta_t/ (2*L) + prev_voltage)
                            ecm_resistor = Resistors("ecm{}{}".format(i,j), i, j, delta_t/ (2*L))
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
            print("create_obj_matrix debug", self.circuit.obj_mat[self.node_map[i_from]][self.node_map[i_to]])
            self.circuit.obj_mat[self.node_map[i_from]][self.node_map[i_to]].append(copy.deepcopy(i))
            print("circuit object matrix", self.circuit.obj_mat)
            
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
    
    def generate_Y_r(self):
        size = len(self.circuit_ecm.obj_mat)
        print("size", size)
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
            dummy_J[size_Y + s_counter] = source.get_nom_voltage()
            s_counter += 1
            # add currents
            for cur in self.solving_dict["ecm-currents"]:
                print("cur amps", cur.amps)
                dummy_J[cur.ip_node] = cur.amps
                dummy_J[cur.in_node] = -cur.amps
            
            
            print("new row:{}\n new col:{}\n from:{}\n to:{}".format(new_row, new_col, from_val, to_val))
        print("dummy Y", dummy_Y, "dummy J", dummy_J)
        self.Y = dummy_Y
        self.J = dummy_J
    
    def delete_ground_node(self):
        datum = self.node_map["gnd"]
        # delete rows and columns associated with datum/ground node
        self.Y = np.delete(np.delete(self.Y, datum, 0), datum, 1)
        self.J = np.delete(self.J, datum, 0)
         
                
    def init_Y(self, devices):
        """
        nodes = devices['nodes']
        voltage_sources = devices['voltage_sources']
        resistors = devices['resistors']
        capacitors = devices['capacitors']
        inductors = devices['inductors']
        switches = devices['switches']
        induction_motors = devices['induction_motors']
        """
        for i in (devices['resistors'] + devices['inductors'] + devices['capacitors']):
            i_from = i.from_node
            i_to = i.to_node
            
            # this will change depending on whether we are using dense or sparse matrices
            self._RLC_stamp(self.node_map(i_from), self.node_map(i_to), self.Y, i.stamp_dense())
            
        datum = self.node_map["gnd"]
        # delete rows and columns associated with datum/ground node
        self.Y = np.delete(np.delete(self.Y, datum, 0), datum, 1)