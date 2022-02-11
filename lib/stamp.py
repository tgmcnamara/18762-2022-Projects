
def stamp_resistor(Y, from_index, to_index, r):
    Y[from_index, from_index] += 1/r
    Y[to_index, to_index] += 1/r

    Y[from_index, to_index] += -1/r
    Y[to_index, from_index] += -1/r

def stamp_current_source(J, from_index, to_index, i):
    J[from_index] += -i
    J[to_index] += i

def stamp_short(Y, J, from_index, to_index, extension_index):
    stamp_voltage_source(Y, J, to_index, from_index, extension_index, 0)

def stamp_voltage_source(Y, J, vp_index, vn_index, current_index, v):
    Y[current_index, vp_index] = 1
    Y[current_index, vn_index] = -1

    Y[vp_index, current_index] = 1
    Y[vn_index, current_index] = -1

    J[current_index] = v