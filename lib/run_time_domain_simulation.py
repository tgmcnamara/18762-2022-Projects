import numpy as np
import math
from classes.Devices import Devices
from classes.Settings import Settings

def execute_simulation(devices: Devices, v_init, settings: Settings):
    node_count = len(v_init)

    runtime = 0
    v_previous = v_init
    J_previous = np.zeros(node_count)

    v_waveform = [v_previous]
    J_waveform = [J_previous]

    while runtime <= settings.simulationTime:
        runtime += settings.timestep
        (v_next, J_next) = execute_time_step(devices, node_count, v_previous, J_previous, runtime, settings)
        v_waveform.append(v_next)
        J_waveform.append(J_next)
        v_previous = v_next
        J_previous = J_next

    return (v_waveform, J_waveform)

def execute_time_step(devices: Devices, node_count, v_previous, J_previous, runtime: float, settings: Settings):
    Y = np.zeros((node_count, node_count))
    J = np.zeros(node_count)

    stamp_NR_invariant_devices(devices, Y, J, v_previous, J_previous, runtime, settings.timestep)

    clear_ground(Y, J, node_count)

    (Y, J) = execute_newtonraphson_iterations(devices, Y, J, v_previous, runtime, settings, node_count)

    v_next = np.linalg.solve(Y, J)

    return (v_next, J)

def stamp_NR_invariant_devices(devices, Y, J, v_previous, J_previous, runtime, timestep):
    for device in devices.all_NR_invariant_devices():
        device.stamp_dense(Y, J, v_previous, J_previous, runtime, timestep)

def execute_newtonraphson_iterations(devices: Devices, Y, J, v_previous, runtime, settings: Settings, node_count):
    nr_devices = devices.all_NR_dependent_devices()
    if len(nr_devices) == 0:
        return (Y, J)

    v_k_minus = np.copy(v_previous)

    for _ in range(settings.maxNewtonIterations):
        Y_k = np.copy(Y)
        J_k = np.copy(J)

        for nr_device in nr_devices:
            nr_device.stamp_dense(Y_k, J_k, v_previous, v_k_minus, runtime, settings.timestep)
        
        clear_ground(Y, J, node_count)

        v_k_plus = np.linalg.solve(Y, J)

        tolerance_reached = True

        for nr_device in nr_devices:
            #assume we only have one NR-dependent variable from any single element.
            variable_plus = nr_device.return_nr_variable(v_k_plus)
            variable_minus = nr_device.return_nr_variable(v_k_minus)
            if math.abs(variable_plus - variable_minus) > settings.tolerance:
                tolerance_reached = False

        if tolerance_reached:
            return (Y_k, J_k)

        v_k_minus = v_k_plus
    
    raise Exception("Max newton iterations exceeeded.")
    

def clear_ground(Y, J, node_count):
    J[0] = 1
    Y[0] = np.zeros(node_count)
    Y[:,0] = np.zeros(node_count)
    Y[0, 0] = 1