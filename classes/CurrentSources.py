from lib.stamp import stamp_current_source

class CurrentSources:
    def __init__(self, name, from_node, to_node, i):
        self.name = name
        self.from_node = from_node
        self.to_node = to_node
        self.i = i
        # You are welcome to / may be required to add additional class variables   
  
    def assign_node_indexes(self, nodeLookup: dict = {}, from_index = -1, to_index = -1):
        self.from_index = nodeLookup[self.from_node]
        self.to_index = nodeLookup[self.to_node]

    def assign_node_indexes_direct(self, from_index, to_index):
        self.from_index = from_index
        self.to_index = to_index

    def get_nodes_connections(self):
        return [self.from_node, self.to_node]

    def stamp_dense(self,  Y, J, v_previous, J_previous, runtime, timestep):
        stamp_current_source(J, self.from_index, self.to_index, self.i)
