

class CurrentSources:
    def __init__(self, name, from_node, to_node, i):
        self.name = name
        self.from_node = from_node
        self.to_node = to_node
        self.i = i
        # You are welcome to / may be required to add additional class variables   
  
    def assign_node_indexes(self, nodeLookup: dict):
        self.from_index = nodeLookup[self.from_node]
        self.to_index = nodeLookup[self.to_node]

    def stamp_dense(self,  Y, J, v_previous, timestep):
        J[self.from_index] += -self.i
        J[self.to_index] += self.i
