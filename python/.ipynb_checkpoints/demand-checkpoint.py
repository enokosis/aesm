import numpy as np
from mip import Model, xsum, minimize, BINARY, mip, MAXIMIZE, MINIMIZE, CONTINUOUS
from cfg import nSmpl

class Demand():
    # The class stores demand for electricity (D_elec), hydrogen (D_H2) and heat (D_heat)
    
    def __init__(self):
        self.D_BaseElec = []   # e.g. MWh electricity
        self.D_H2 = []       # e.g. kg H2
        self.D_heat = []   # e.g. MWh heat

    def const_demand(self, D_BaseElec=0, D_H2=0, D_heat=0):    
        for t in range(nSmpl):
            self.add_demand(D_BaseElec[t], D_H2[t], D_heat[t])


    def add_demand (self, D_ElecUnit=0, D_H2Unit=0, D_heatUnit=0):
        self.D_BaseElec.append(D_ElecUnit)  # e.g. MWh electricity
        self.D_H2.append(D_H2Unit)     # e.g. kg H2
        self.D_heat.append(D_heatUnit)  # e.g. MWh heat
        
class Scenario:
    def __init__(self, techList, demand, message = "New scenario"):
        self.techList=techList
        self.demand=demand 
        self.message = message 
