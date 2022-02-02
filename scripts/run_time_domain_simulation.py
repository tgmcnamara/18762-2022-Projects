import numpy as np
from numpy import ndarray
from classes.Devices import Devices
from classes.Settings import Settings

def execute_simulation(devices: Devices, v_init, settings: Settings):
    node_count = len(v_init)

    v_waveform = [v_init]

    timestep = 0
    v_previous = v_init

    while timestep <= settings.simulationTime:
        timestep += 0.001 #wild guess
        v_next = execute_time_step(devices, node_count, v_previous, timestep, settings)
        v_waveform.append(v_next)
        v_previous = v_next

    return v_waveform

def execute_time_step(devices: Devices, node_count, v_previous, timestep: float, settings: Settings):
    Y = np.zeros((node_count, node_count))
    J = np.zeros(node_count)

    stamp_devices(devices, Y, J, v_previous, timestep)

    clear_ground(Y, J, node_count)

    Y_inverse = np.linalg.inv(Y)

    v_next = np.dot(J, Y_inverse)

    return v_next

def stamp_devices(devices, Y, J, v_previous, timestep):
    for device in devices.all_devices_but_nodes():
        device.stamp_dense(Y, J, v_previous, timestep)

def clear_ground(Y, J, node_count):
    J[0] = 1
    Y[0] = np.zeros(node_count)
    Y[:,0] = np.zeros(node_count)
    Y[0, 0] = 1