from sympy import *

#transformer

trcos, trsin = symbols('trcos trsin')
V_BR, V_BI, IR, II, VR, VI = symbols('V_BR V_BI IR II VR VI')
L_BR, L_BI, L_IR, L_II, L_VR, L_VI = symbols('L_BR L_BI L_IR L_II L_VR L_VI')

lagrange = L_BR * IR
lagrange += L_BI * II
lagrange += L_IR * (V_BR - trcos * VR + trsin * VI)
lagrange += L_II * (V_BI - trcos * VI - trsin * VR)
lagrange += L_VR * (-trcos * IR - trsin * II)
lagrange += L_VI * (-trcos * II + trsin * IR)

print("Transformer:")
print(f'dV_BR: {diff(lagrange, V_BR)}')
print(f'dV_BI: {diff(lagrange, V_BI)}')
print(f'dIR: {diff(lagrange, IR)}')
print(f'dII: {diff(lagrange, II)}')
print(f'dVR: {diff(lagrange, VR)}')
print(f'dVI: {diff(lagrange, VI)}')

