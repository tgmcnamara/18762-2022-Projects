import numpy as np

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
