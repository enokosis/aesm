import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from mip import *

m = Model()

   
"""
          

class AddVariables():
       
    def addContinuous(self):
        m.add_var(self)

        
"""

def AddObjective():
    m.objective = minimize( xsum( (solar[i].CAPEX * solar[i].R + solar[i].FC) * C[i] for i in range(len(solar)) ) )
    
"""
class Test():
    def __init__(self, CAPEX, cst):
        self.CAPEX = CAPEX
    
        self.capacityConst = mip.Constr(m.var_by_name("x")<=cst, "Qw")
    
    def addConsts(self,mod):
        mod+= mod.var_by_name("x") <= 160
        
        
class AddConstraints():
    def __init__(self):
        
        tst = Test(13, 1000)
        #capacityConst = mip.Constr(m.var_by_name("x")<=322, "qw")
                                   
        #m.add_constr(tst.capacityConst.expr, "Test constraint")
        tst.addConsts(m)
        v1 = m.var_by_name("x")
        m.add_constr(v1<=80)
        m.add_constr(v1<=1080)
        """

class Solar():
    
    counter = 0 
    
    def __init__(self, CAPEX, R, FC, CapFac):
        Solar.counter += 1
        self.CAPEX = CAPEX
        self.R = R
        self.FC = FC
        self.CapFac = CapFac
        self.VC = 0

class Wind():
    
    counter = 0 
    
    def __init__(self, CAPEX, R, FC, CapFac):
        Wind.counter += 1
        self.CAPEX = CAPEX
        self.R = R
        self.FC = FC
        self.CapFac = CapFac
        self.VC = 0

timeSteps = 5
T = range(0,timeSteps)
D = [1, 2, 1, 2, 1]
CapFac = [1, 1, 1, 1, 1]
        
solar = []
solar.append(Solar(1,1,1,CapFac))
solar.append(Solar(2,2,2,CapFac))


solar
C = [m.add_var() for i in range( len (solar)) ]
G = [m.add_var() for t in T]


    
for t in T:
    m += G[t] == xsum( solar[i].CapFac[t] * C[i] for i in range( len (solar) ) )

for t in T:
    m += G[t] >= D[t]


AddObjective()

m.optimize()

# printing the solution
print('')
print('Objective value: {m.objective_value:.3}'.format(**locals()))
print('Solution: ', end='')
for v in m.vars:

    print('{v.name} = {v.x}'.format(**locals()))
    print('          ', end='')





