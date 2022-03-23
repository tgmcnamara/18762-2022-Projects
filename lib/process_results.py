import math

class PowerFlowResults:
    def __init__(self, bus_results):
        self.bus_results = bus_results

class GeneratorResult:
    def __init__(self, generator, P, Q, is_slack):
        self.generator = generator
        self.P = P
        self.Q = Q
        self.is_slack = is_slack

class BusResult:
    def __init__(self, bus, V_r, V_i, Q):
        self.bus = bus
        self.V_r = V_r
        self.V_i = V_i
        self.V_mag = math.sqrt(V_r ** 2 + V_i ** 2)
        self.V_ang = math.tanh(V_i / V_r)  * 57.3
    
    def __str__(self) -> str:
        return f'Bus {self.bus.Bus} V_mag (pu): {"{:10.3f}".format(self.V_mag)}, V_ang (deg): {"{:10.3f}".format(self.V_ang)}'

def process_results(raw_data, v_final):
    bus_results = []
    
    for bus in raw_data['buses']:
        Q = None
        V_r = v_final[bus.node_Vr]
        V_i = v_final[bus.node_Vi]
        if bus.node_Q != None:
            Q = v_final[bus.node_Q]
        
        bus_results.append(BusResult(bus, V_r, V_i, Q))

    return PowerFlowResults(bus_results)

