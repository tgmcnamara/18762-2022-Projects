import numpy as np
import math
from classes.Devices import Devices
from classes.Settings import Settings

class Simulator:    
    def __init__(self, devices: Devices, settings: Settings, y_size: int):
        self.devices = devices
        self.settings = settings
        self.y_size = y_size
        self.timestep = settings.timestep

    def execute_simulation(self, v_init):
        runtime = 0
        v_previous = v_init
        J_previous = np.zeros(self.y_size)

        v_waveform = [v_previous]
        J_waveform = [J_previous]

        while runtime <= self.settings.simulationTime:
            runtime += self.timestep
            (v_next, J_next) = self.execute_time_step(v_previous, J_previous, runtime)
            v_waveform.append(v_next)
            J_waveform.append(J_next)
            v_previous = v_next
            J_previous = J_next

        return (v_waveform, J_waveform)

    def execute_time_step(self, v_previous, J_previous, runtime: float):
        Y = np.zeros((self.y_size, self.y_size))
        J = np.zeros(self.y_size)

        self.stamp_NR_invariant_devices(Y, J, v_previous, J_previous, runtime)

        self.clear_ground(Y, J)

        (Y, J) = self.execute_newtonraphson_iterations(Y, J, v_previous, runtime)

        v_next = np.linalg.solve(Y, J)

        return (v_next, J)

    def stamp_NR_invariant_devices(self, Y, J, v_previous, J_previous, runtime):
        for device in self.devices.all_NR_invariant_devices():
            device.stamp_dense(Y, J, v_previous, J_previous, runtime, self.timestep)

    def execute_newtonraphson_iterations(self, Y, J, v_t_previous, runtime):
        nr_devices = self.devices.all_NR_dependent_devices()
        if len(nr_devices) == 0:
            return (Y, J)

        v_k_minus = np.copy(v_t_previous)

        for _ in range(self.settings.maxNewtonIterations):
            Y_k = np.copy(Y)
            J_k = np.copy(J)

            for nr_device in nr_devices:
                nr_device.stamp_dense(Y_k, J_k, v_t_previous, v_k_minus, self.timestep)
            
            self.clear_ground(Y_k, J_k)

            v_k_plus = np.linalg.solve(Y_k, J_k)

            error = np.amax(np.abs(v_k_plus - v_k_minus))

            if error < self.settings.tolerance:
                return (Y_k, J_k)

            v_k_minus = v_k_plus
        
        raise Exception("Max newton iterations exceeeded.")
        

    def clear_ground(self, Y, J):
        J[0] = 0
        Y[0] = np.zeros(self.y_size)
        Y[:,0] = np.zeros(self.y_size)
        Y[0, 0] = 1