from sympy import *
import numpy as np

#transformer

trcos, trsin = symbols('trcos trsin')
variables = [V_BR, V_BI, IR, II, VR, VI] = symbols('V_BR V_BI IR II VR VI')
lambdas = [L_BR, L_BI, L_IR, L_II, L_VR, L_VI] = symbols('L_BR L_BI L_IR L_II L_VR L_VI')

eqns = [
    IR,
    II,
    V_BR - trcos * VR + trsin * VI,
    V_BI - trcos * VI - trsin * VR,
    -trcos * IR - trsin * II,
    -trcos * II + trsin * IR
]

lagrange = np.dot(np.transpose(lambdas), eqns)

print("Transformer:")
for variable in variables:
    print(f'{variable}: {diff(lagrange, variable)}')


#Load


