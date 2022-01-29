from numpy import float64, ndarray
from classes.CircuitFrame import CircuitFrame
from classes.Devices import Devices
from classes.Settings import Settings

def execute_simulation(devices: Devices, initialFrame: CircuitFrame, nodeLookup: dict, settings: Settings):
    circuitFrames = [CircuitFrame]

    timestep = 0
    previousFrame = initialFrame

    while timestep <= settings.simulationTime:
        nextFrame = execute_time_step(devices, previousFrame, timestep, nodeLookup, settings)
        circuitFrames.append(nextFrame)
        previousFrame = nextFrame
        timestep += 0.0001 #wild guess

    return circuitFrames

def execute_time_step(devices: Devices, previousFrame: CircuitFrame, nodeLookup: dict, settings: Settings):
    pass