from lib.stamp import stamp_resistor, stamp_current_source, stamp_short

class Inductors:
    def __init__(self, name, from_node, to_node, l):
        self.name = name
        self.from_node = from_node
        self.to_node = to_node
        self.l = l  

    def assign_node_indexes(self, nodeLookup: dict):
        self.from_index = nodeLookup[self.from_node]
        self.to_index = nodeLookup[self.to_node]

        modified_index = len(nodeLookup)
        nodeLookup[self.name + "-1"] = modified_index
        self.extension_index_1 = modified_index
        modified_index += 1
        nodeLookup[self.name + "-2"] = modified_index
        self.extension_index_2 = modified_index
        
    def get_nodes_connections(self):
        return [self.from_node, self.to_node]

    def stamp_dense(self, Y, J, v_previous, J_previous, runtime, timestep):
        conductance = timestep / (2 * self.l)

        companion_r = 1 / conductance

        stamp_resistor(Y, self.from_index, self.extension_index_1, companion_r)

        previous_voltage = v_previous[self.from_index] - v_previous[self.extension_index_1]

        previous_current = J_previous[self.extension_index_1]

        companion_i = previous_current + conductance * previous_voltage
        
        stamp_current_source(J, self.from_index, self.extension_index_1, companion_i)

        stamp_short(Y, J, self.extension_index_1, self.to_index, self.extension_index_2)

    def stamp_sparse(self,):
        pass

    def stamp_short(self,):
        pass