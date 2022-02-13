from lib.stamp import stamp_resistor, stamp_short, stamp_voltage_source

class Capacitors:
    def __init__(self, name, from_node, to_node, c):
        self.name = name
        self.c = c
        self.from_node = from_node
        self.to_node = to_node
        # You are welcome to / may be required to add additional class variables   

    def assign_node_indexes(self, nodeLookup: dict):
        self.from_index = nodeLookup[self.from_node]
        self.to_index = nodeLookup[self.to_node]

        modified_index = len(nodeLookup)
        nodeLookup[self.name + "-1"] = modified_index
        self.extension_index_1 = modified_index
        modified_index += 1
        nodeLookup[self.name + "-2"] = modified_index
        self.extension_index_2 = modified_index
        modified_index += 1
        nodeLookup[self.name + "-3"] = modified_index
        self.extension_index_3 = modified_index
        modified_index += 1
        nodeLookup[self.name + "-4"] = modified_index
        self.extension_index_4 = modified_index

    def get_nodes_connections(self):
        return [self.from_node, self.to_node]

    def stamp_dense(self, Y, J, v_previous, J_previous, runtime, timestep):
        
        companion_r = timestep / (2 * self.c)

        stamp_short(Y, J, self.extension_index_1, self.from_index, self.extension_index_2)

        stamp_resistor(Y, self.extension_index_1, self.extension_index_3, companion_r)

        previous_current = v_previous[self.extension_index_2]

        previous_resistor_voltage = previous_current * companion_r
        previous_voltage_source_voltage = J_previous[self.extension_index_4]
        previous_voltage = previous_voltage_source_voltage + previous_resistor_voltage
        
        companion_v = previous_voltage + companion_r * previous_current

        stamp_voltage_source(Y, J, self.extension_index_3, self.to_index, self.extension_index_4, companion_v)

    def stamp_sparse(self,):
        pass

    def stamp_open(self,):
        pass