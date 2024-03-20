import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from mip import *

m = Model(sense=MAXIMIZE)


class AddVariables():
       
    def addContinuous(self):
        m.add_var(self)
        print("added x")
        
Objective = []

def AddObjective():
    v1= m.var_by_name("x")
    m.objective= v1
    
    
    
          
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

        
        
        
adds= AddVariables
adds.addContinuous("x")
AddObjective()
print(m.var_by_name("x"))
print(adds)
conster= AddConstraints()
m.optimize()




class PowerPlants():
    
    def __init__(self, CAPEX, R, FC):
        self.CAPEX = CAPEX
        self.R = R
        self.FC = FC
     
    
class HydroReservoir(PowerPlants):

    def __init__(self, CAPEX, R, FC, VC_electricity, VC_heat):

        self.g_t=[]
        self.g_capacity=[]
        self.s_t=[]
        self.s_capacity=[]
        self.in_t=[]
        self.out_t=[]
        self.bypass_t=[]
        self.out_minimum_t=[]
        
    def read_FI(self,fname):
        data=pd.read_csv(fname, skiprows=22,
                              sep = '\s+|\t+|\s+\t+|\t+\s+',
                              engine='python')
        # Each data value corresponds to the inflow energy
        # for last 7 day period. Therefore divide by 7*24,
        # assume a constant flow per hour, and convert to hourly
        # values. Use the median values from the data.
        self.in_t=np.zeros((365,24))
        for i in range(24):
            self.in_t[:,i]=data['Median']/(7*24)
        self.in_t=self.in_t.flatten()
        
        print(self.in_t)
        # According to Afry report
        # https://www.fingrid.fi/globalassets/dokumentit/fi/sahkomarkkinat/kehityshankkeet/dalyve-fingrid_flexibility-study_final-report_v300-id-151641.pdf
        # approximately 45% of the hydro capacity is 
