
def test(a):
    a += 1
#
#  MULTIVARIABLE NEWTON RAPHSON
#
import numpy as np


# Defining Function
def f(x):
    fx1 = x[0]**2 + x[1]**1 - 4
    fx2 = 4*x[0]**2 - x[1]**2 - 4
    f = np.array([fx1, fx2])
    return f

# Defining derivative of function
def J(x):
    j = np.array([[2*x[0], 2*x[1]], [8*x[0], 2*x[1]]])
    return j

# Implementing Newton Raphson Method

def newtonRaphson(x0,e,N):
    print('\n\n*** NEWTON RAPHSON METHOD IMPLEMENTATION ***')
    step = 1
    flag = 1
    condition = True
    while condition:
        
        x1 = x0 - np.linalg.inv(J(x0)) @ f(x0)
        print('Iteration:{}, x1 = {} and f(x1) = {}'.format(step,x1,f(x1)))
        x0 = x1
        
        step = step + 1
        
        if step > N:
            flag = 0
            break
        
        condition = (abs(f(x1)) > e).all()
    
    if flag==1:
        print('\nRequired root is:{}'.format(x1))
    else:
        print('\nNot Convergent.')


# Input Section
N = input('Maximum Steps: ')

# Converting x0 and e to float
x0 = np.array([1, 1])
e = 0.02

# Converting N to integer
N = int(N)


#Note: You can combine above three section like this
# x0 = float(input('Enter Guess: '))
# e = float(input('Tolerable Error: '))
# N = int(input('Maximum Step: '))

# Starting Newton Raphson Method
newtonRaphson(x0,e,N)

a = 1
test(a)

print(a)