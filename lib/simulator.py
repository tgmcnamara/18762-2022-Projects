from classes.Devices import Devices
from classes.Settings import Settings
from lib.matrixprovider import MatrixProvider

class Simulator:    
    def __init__(self, devices: Devices, settings: Settings, y_size: int, matrixprovider: MatrixProvider):
        self.devices = devices
        self.settings = settings
        self.y_size = y_size
        self.timestep = settings.timestep
        self.matrixprovider = matrixprovider

    def execute_simulation(self, v_init):
        runtime = 0
        v_previous = v_init
        J_previous = self.matrixprovider.generate_zero_vector()

        v_waveform = [v_previous]
        J_waveform = [J_previous]

        while runtime <= self.settings.simulationTime:
            runtime += self.timestep
            (v_next, J_next) = self.execute_time_step(v_previous, runtime)
            v_waveform.append(v_next)
            J_waveform.append(J_next)
            v_previous = v_next
            J_previous = J_next

        return (v_waveform, J_waveform)

    def execute_time_step(self, v_previous, runtime: float):
        Y = self.matrixprovider.generate_zero_matrix()
        J = self.matrixprovider.generate_zero_vector()

        self.stamp_NR_invariant_devices(Y, J, v_previous, runtime)

        self.clear_ground(Y, J)

        (Y, J) = self.execute_newtonraphson_iterations(Y, J, v_previous, runtime)

        v_next = self.matrixprovider.solve(Y, J)

        return (v_next, J)

    def stamp_NR_invariant_devices(self, Y, J, v_previous, runtime):
        for device in self.devices.all_NR_invariant_devices():
            device.stamp_dense(Y, J, v_previous, runtime, self.timestep)

    def execute_newtonraphson_iterations(self, Y, J, v_t_previous, runtime):
        nr_devices = self.devices.all_NR_dependent_devices()
        if len(nr_devices) == 0:
            return (Y, J)

        v_k_minus = self.matrixprovider.copy(v_t_previous)

        for _ in range(self.settings.maxNewtonIterations):
            Y_k = self.matrixprovider.copy(Y)
            J_k = self.matrixprovider.copy(J)

            for nr_device in nr_devices:
                nr_device.stamp_dense(Y_k, J_k, v_t_previous, v_k_minus, self.timestep)
            
            self.clear_ground(Y_k, J_k)

            v_k_plus = self.matrixprovider.solve(Y_k, J_k)

            error = self.matrixprovider.max_difference(v_k_plus, v_k_minus)

            if error < self.settings.tolerance:
                return (Y_k, J_k)

            v_k_minus = v_k_plus
        
        raise Exception("Max newton iterations exceeeded.")
        

    def clear_ground(self, Y, J):
        J[0] = 0
        Y[0] = self.matrixprovider.generate_zero_vector()
        Y[:,0] = self.matrixprovider.generate_zero_vector()
        Y[0, 0] = 1
