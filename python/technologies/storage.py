from .technology import Technology
from mip import Model, xsum, minimize, BINARY, mip, MAXIMIZE, MINIMIZE, CONTINUOUS

import numpy as np
import math



class Storage(Technology):
    def __init__(self, CAPEX_S = 0, FC_S = 0, eta_charge = 1, eta_discharge = 1, eta_selfDischarge = 0, **kwargs):

        ## add parameters
        super().__init__(**kwargs)
        self.CAPEX_S = CAPEX_S
        self.FC_S = FC_S
        self.eta_charge = eta_charge
        self.eta_discharge = eta_discharge
        self.eta_selfDischarge = eta_selfDischarge
        
    def add_to_model(self, model):
        super().add_to_model(model)
        ## add variables
        self.C_S = model.m.add_var(name= self.name + " C_S", var_type = CONTINUOUS)
        self.delta_S = [model.m.add_var(name= self.name + " delta_S", var_type = CONTINUOUS, lb = -math.inf, ub = math.inf) for t in range(model.nSmpl)]
        self.S = [model.m.add_var(name= self.name + " S", var_type = CONTINUOUS) for t in range(model.nSmpl+1)]
        self.charge = [model.m.add_var(name= self.name + " Charge", var_type = CONTINUOUS) for t in range(model.nSmpl)]
        self.discharge = [model.m.add_var(name= self.name + " Discharge", var_type = CONTINUOUS) for t in range(model.nSmpl)]
        
        ## add constraints
        for t in range(model.nSmpl+1):
            # storage cannot exceed capacity
            model.m.add_constr(self.S[t] <= self.C_S)

        for t in range(model.nSmpl):

            # next storage level accounts for self-discharge and charging / discharing and their losses
            model.m.add_constr(self.S[t+1] == self.S[t] * (1-self.eta_selfDischarge) + self.charge[t] - self.discharge[t])  
            
            # change in storage (inpput to electricity and H2 balance)
            model.m.add_constr(self.delta_S[t] == self.charge[t] / self.eta_charge - self.discharge[t] * self.eta_discharge)
                  
            # change in storage cannot exceed power capacity
            model.m.add_constr(self.delta_S[t] >= -self.C_G)
            model.m.add_constr(self.delta_S[t] <= self.C_G)
        
        # the model becomes cyclical by setting the initital and final storage levels equal 
        model.m.add_constr(self.S[0] == self.S[model.nSmpl])

        ## add objective
        self.Cost = (self.CAPEX_G * self.R + self.FC_G) * self.C_G + (self.CAPEX_S * self.R + self.FC_S) * self.C_S
 
class Battery(Storage):
    
    def __init__(self, DOD = 1, **kwargs):
        super().__init__(**kwargs)    
        # Add depth of discharge
        self.DOD = DOD
        
    def add_to_model(self, model):
        super().add_to_model(model)
        for t in range(model.nSmpl+1):
            # Usually all battery capacity is not used to avoid degradation.
            # Depth of discharge limits battery usage to a certain percentage of total capacity.
            model.m.add_constr(self.S[t] <= self.C_S * self.DOD)        
        
            
class H2Storage(Storage):
    
    def __init__(self, alpha_pump = 0, **kwargs):
        super().__init__(**kwargs)
        self.alpha_pump = alpha_pump
        
    def add_to_model(self,model):
        super().add_to_model(model)
        self.Conv_ElecToH2 = [model.m.add_var(name= self.name + " ElecToH2", var_type = CONTINUOUS) for t in range(model.nSmpl)]
        
        # Electricity generation is defnied by capacity factor and installed capacity
        for t in range(model.nSmpl):
            model.m.add_constr(self.Conv_ElecToH2[t] == self.charge[t] * self.alpha_pump)

        
class HeatStorage(Storage):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)     
    def add_to_model(self,model):
        super().add_to_model(model)  

