import math

class PowerFlowResults:
    def __init__(self, bus_results, generator_results, duration_seconds):
        self.bus_results = bus_results
        self.generator_results = generator_results
        self.duration_seconds = duration_seconds

    def display(self):
        print("Bus Results:")

        for bus in self.bus_results:
            print(bus)

        print("Generator Results:")

        for gen in self.generator_results:
            print(gen)

class GeneratorResult:
    def __init__(self, generator, P, Q, is_slack):
        self.generator = generator
        self.P = P * 100
        self.Q = Q * 100
        self.is_slack = is_slack

    def __str__(self) -> str:
        name = "Slack" if self.is_slack else "Generator"
        return f'{name} @ bus {self.generator.bus.Bus} P (MW): {"{:.2f}".format(self.P)}, Q (MVar): {"{:.2f}".format(self.Q)}'

class BusResult:
    def __init__(self, bus, V_r, V_i):
        self.bus = bus
        self.V_r = V_r
        self.V_i = V_i
        self.V_mag = math.sqrt(V_r ** 2 + V_i ** 2)
        self.V_ang = math.tanh(V_i / V_r)  * 57.3
    
    def __str__(self) -> str:
        return f'Bus {self.bus.Bus} V_mag (pu): {"{:.3f}".format(self.V_mag)}, V_ang (deg): {"{:.3f}".format(self.V_ang)}'

def process_results(raw_data, v_final, duration_seconds):
    bus_results = []
    
    for bus in raw_data['buses']:
        V_r = v_final[bus.node_Vr]
        V_i = v_final[bus.node_Vi]
        
        bus_results.append(BusResult(bus, V_r, V_i))

    generator_results = []

    for generator in raw_data["generators"]:
        Q = v_final[generator.bus.node_Q]
        P = generator.P

        generator_results.append(GeneratorResult(generator, P, Q, False))

    slack = raw_data["slack"][0]
    slack_Ir = v_final[slack.slack_Ir]
    slack_Vr = slack.Vr_set
    P = slack_Vr * slack_Ir * math.cos(slack.ang)
    Q = slack_Vr * slack_Ir * math.sin(slack.ang)
    generator_results.append(GeneratorResult(generator, P, Q, True))

    return PowerFlowResults(bus_results, generator_results, duration_seconds)


def display_mat_comparison(mat, results: PowerFlowResults):
    for idx in range(len(mat['sol']['bus'][0][0])):
        bus = mat['sol']['bus'][0][0][idx][0]
        V_mag = mat['sol']['bus'][0][0][idx][7]
        V_ang = mat['sol']['bus'][0][0][idx][8]

        simulator_V_mag = results.bus_results[idx].V_mag
        simulator_V_ang = results.bus_results[idx].V_ang

        print(f'Bus: {int(bus)} V_mag diff: {"{:.2f}".format(simulator_V_mag - V_mag)} V_ang diff: {"{:.2f}".format(simulator_V_ang - V_ang)}')
