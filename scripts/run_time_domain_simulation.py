import numpy as np
from numpy import ndarray
from classes.Devices import Devices
from classes.Settings import Settings

def execute_simulation(devices: Devices, v_init, settings: Settings):
    node_count = len(v_init)

    v_waveform = [v_init]

    runtime = 0
    v_previous = v_init
    J_previous = np.zeros(node_count)

    while runtime <= settings.simulationTime:
        runtime += settings.timestep
        (v_next, J_next) = execute_time_step(devices, node_count, v_previous, J_previous, runtime, settings)
        v_waveform.append(v_next)
        v_previous = v_next
        J_previous = J_next

    return v_waveform

def execute_time_step(devices: Devices, node_count, v_previous, J_previous, runtime: float, settings: Settings):
    Y = np.zeros((node_count, node_count))
    J = np.zeros(node_count)

    stamp_devices(devices, Y, J, v_previous, J_previous, runtime, settings.timestep)

    clear_ground(Y, J, node_count)

    v_next = np.linalg.solve(Y, J)

    return (v_next, J)

def stamp_devices(devices, Y, J, v_previous, J_previous, runtime, timestep):
    for device in devices.all_devices_but_nodes():
        device.stamp_dense(Y, J, v_previous, J_previous, runtime, timestep)

def clear_ground(Y, J, node_count):
    J[0] = 1
    Y[0] = np.zeros(node_count)
    Y[:,0] = np.zeros(node_count)
    Y[0, 0] = 1