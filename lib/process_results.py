import math
from typing import List

from models.Buses import Bus

class BusResult:
    def __init__(self, bus, V_r, V_i, Q) -> None:
        self.bus = bus
        self.V_r = V_r
        self.V_i = V_i
        self.Q = Q
        self.V_mag = math.sqrt(V_r ** 2 + V_i ** 2)
        self.V_ang = math.tanh(V_i / V_r)
    
    def __str__(self) -> str:
        s = f'Bus {self.bus.Bus} Vmag: {round(self.V_mag, 4)}, Vang: {round(self.V_ang, 4)}'

        if self.Q != None:
            s += f' Q: {round(self.Q, 4) * 100}'

        return s

def process_results(buses: List[Bus], v_final):
    results = []
    
    for bus in buses:
        Q = None
        V_r = v_final[bus.node_Vr]
        V_i = v_final[bus.node_Vi]
        if bus.node_Q != None:
            Q = v_final[bus.node_Q]
        
        results.append(BusResult(bus, V_r, V_i, Q))

    return results


