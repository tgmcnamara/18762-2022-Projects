import numpy as np
import scipy
import copy

"""
COMPONENT LIST:
stores object circuit element object references
"""
class comp_list():
    def __init__(self):
        self.elements = []
        
    def append(self, val):
        self.elements.append(val)

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
        self.solving_dict = {}
        
        self.timestep = 0
        self.source_list = []
        self.Y_hist = None
        self.v_hist = None
        self.J_hist = None
        self.t_inc = None
        self.Y = np.zeros((size_Y, size_Y))
        self.v = np.zeros((size_Y, 1))
        self.J = np.zeros((size_Y, 1))
        
        if (node_indices != None):
            self.node_map = node_indices
            
        if (devices == None):
            pass
        else:
            # creating a list comprehension matrix to store circuit objects
            self.circuit = circuit(size_Y)
            self.create_obj_matrix(devices)
            
            # create list of sources
            for source in devices['voltage_sources']:
                self.source_list.append(source)
                
            #self.init_Y(devices)
            self.generate_Y_r()
            self.perform_mna()
     
    def init_solver(self, settings):   
        self.solving_dict["sim_time"] = settings['Simulation Time']
        self.solving_dict["tol"] = settings['Tolerance']  # NR solver tolerance
        self.solving_dict["max_iters"] = settings['Max Iters']  # maximum NR iterations
            
    def update_Y(self, devices):
        # this should update y from the object matrix which could be helfpul later on for
        # Newton-Raphson, switches and companion models
        pass    
        
    def create_source_list(self, sources):
        for i in sources:
            self.source_list.append(i)
            
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
    
    def generate_Y_r(self):
        size = len(self.circuit.obj_mat)
        for i in range(size):
            for j in range(size):
                element_list = self.circuit.obj_mat[i][j]
                if (element_list.is_null() == False):
                    for k in element_list.elements:
                        self._RLC_stamp(i,j, self.Y, k.stamp_dense())
                        
        
    def perform_mna(self):
        # loop through sources
        # numpy.append(arr, values, axis=None)[source]
        size_Y = self.Y.shape[0]
        for source in self.source_list:
            from_val = source.vp_node
            to_val = source.vn_node
            new_row = np.eye(size_Y)[self.node_map[from_val]]
            new_col = np.eye(size_Y)[self.node_map[to_val]]
            #
            print("new row:{}\n new col:{}\n from:{}\n to:{}".format(new_row, new_col, from_val, to_val))
    
    def delete_ground_node(self):
        datum = self.node_map["gnd"]
        # delete rows and columns associated with datum/ground node
        self.Y = np.delete(np.delete(self.Y, datum, 0), datum, 1)
         
                
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