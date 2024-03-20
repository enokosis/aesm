import numpy as np
import pandas as pd
from technologies.technology import Technology

from mip import Model, xsum, minimize, BINARY, mip, MAXIMIZE, MINIMIZE, CONTINUOUS
import math


class PowerPlant(Technology):
    def __init__(self, AF=0, C_Gmin = 0, C_Gmax = math.inf, **kwargs):
        ## add parameters
        super().__init__(**kwargs) # add super class level parameters
        self.AF = AF #AF - availability factor at every hour of the year 
        self.C_Gmin = C_Gmin
        self.C_Gmax = C_Gmax
               
    def add_to_model(self, model):
        ## add variables
        super().add_to_model(model) # add super class level variables
        self.G_elec = [model.m.add_var(name= self.name + " G_elec", var_type = CONTINUOUS) for t in range(model.nSmpl)]
        
        # capacity constraints
        model.m.add_constr(self.C_G >= self.C_Gmin)
        model.m.add_constr(self.C_G <= self.C_Gmax)
   
class WindPower(PowerPlant):
    
    def __init__(self,  **kwargs):
        ## add parameters
        super().__init__(**kwargs) # add super class level parameters


    def add_to_model(self, model):
        ## add variables
        super().add_to_model(model) # add super class level variables
        
        # Curtailment allows for the shut down of the wind power plant
        self.Curtail = [model.m.add_var(name= self.name + " Curtail", var_type = CONTINUOUS) for t in range(model.nSmpl)]

        ## add constraints                
        # Electricity generation is defnied by capacity factor and installed capacity
        for t in range(model.nSmpl):
            model.m.add_constr(self.G_elec[t] + self.Curtail[t] == self.AF[t] * self.C_G)


        
        ## add objective
        self.Cost = self.Cost + xsum(self.VC_G * self.G_elec[t] for t in range(model.nSmpl))
        

class SolarPower(PowerPlant):
    # Solar module is asuumed to be similar to wind power module. However a separate
    # class is defined for solar so that user can make changes straight to SolarPower
    # or wind class if necessary
    
    def __init__(self,  **kwargs):
        ## add parameters
        super().__init__(**kwargs) # add super class level parameters


    def add_to_model(self, model):
        ## add variables
        super().add_to_model(model) # add super class level variables

        # Curtailment allows for the shut down of the solar power plant
        self.Curtail = [model.m.add_var(name= self.name + " Curtail", var_type = CONTINUOUS) for t in range(model.nSmpl)]
        
        ## add constraints        
        # Electricity generation is defnied by capacity factor and installed capacity
        for t in range(model.nSmpl):
            model.m.add_constr(self.G_elec[t] + self.Curtail[t] == self.AF[t] * self.C_G)
        
        ## add objective
        self.Cost = self.Cost + xsum(self.VC_G * self.G_elec[t] for t in range(model.nSmpl))

class Hydro(PowerPlant):
    
    def __init__(self, Inflow, Outflow_min, CAPEX_S = 0, FC_S = 0, C_Smax = math.inf, **kwargs):
        super().__init__(**kwargs) # add super class level parameters
        # add parameters
        self.Inflow = Inflow
        self.Outflow_min = Outflow_min
        self.CAPEX_S = CAPEX_S
        self.FC_S = FC_S

        self.C_Smax = C_Smax

    def add_to_model(self, model):
        ## Add variables
        super().add_to_model(model) # add super class level variables
        self.C_S = model.m.add_var(name= self.name + " C_S", var_type = CONTINUOUS)
        self.S = [model.m.add_var(name= self.name + " S", var_type = CONTINUOUS) for t in range(model.nSmpl+1)]
        self.Outflow = [model.m.add_var(name= self.name + " Outflow", var_type = CONTINUOUS) for t in range(model.nSmpl)]
        self.Bypass = [model.m.add_var(name= self.name + " Bypass", var_type = CONTINUOUS) for t in range(model.nSmpl)]
        
        ## Add contstraints
        for t in range(model.nSmpl):
            # Electricity generation is limited by the installed capacity
            model.m.add_constr(self.G_elec[t] <= self.C_G)
            # Chnage in storage is determnied by inflow and outflow
            model.m.add_constr(self.S[t+1] == self.S[t] + self.Inflow[t] - self.Outflow[t])
            # Outflow constraints
            model.m.add_constr(self.Outflow[t] == self.G_elec[t] + self.Bypass[t])
            model.m.add_constr(self.Outflow[t] >= self.Outflow_min)
            
        # Storage level is limited by the installed storage capacity
        for t in range(model.nSmpl+1):
            model.m.add_constr(self.S[t] <= self.C_S)        
            
        # Maximum capacity cannot be exceeded
        model.m.add_constr(self.C_S <= self.C_Smax)
        
        # the model becomes cyclical by setting the initital and final storage levels equal 
        model.m.add_constr(self.S[0] == self.S[model.nSmpl])
        
        ## Add objective
        self.Cost = (self.CAPEX_G * self.R + self.FC_G) * self.C_G + (self.CAPEX_S * self.R + self.FC_S) * self.C_S + xsum(self.VC_G * self.G_elec[t] for t in range(model.nSmpl))


class Nuclear(PowerPlant):
    def __init__(self, RampU = 1, RampD = 1, AF_min = 0, AF_max = 1, **kwargs):
        ## add parameters
        super().__init__(**kwargs) # add super class level parameters
        self.RampU = RampU 
        self.RampD = RampD
        self.AF_min = AF_min
        self.AF_max = AF_max
        
    def add_to_model(self, model):
        ## add variables
        super().add_to_model(model) # add super class level variables
        
        ## add constraints
        #The plant generation can be ramped up or down by certain percent, but not get lower that AFMin
        for t in range(model.nSmpl):
            model.m.add_constr(self.G_elec[t] >= self.C_G * self.AF_min)
            model.m.add_constr(self.G_elec[t] <= self.C_G * self.AF_max)
        
        for t in range(1,model.nSmpl):
            model.m.add_constr( (self.G_elec[t] - self.G_elec[t-1] ) <= self.C_G * self.RampU)
            model.m.add_constr( (self.G_elec[t-1] - self.G_elec[t] ) <= self.C_G * self.RampD)
        
        ## add objective
        self.Cost = self.Cost + xsum(self.VC_G * self.G_elec[t] for t in range(model.nSmpl))

class GasTurbine(PowerPlant):

    def __init__(self, eta_turbine = 0.945,  **kwargs):
        ## add parameters
        super().__init__(**kwargs) # add super class level parameters
        self.eta_turbine = eta_turbine

    def add_to_model(self, model):
        ## add variables
        super().add_to_model(model) # add super class level variables
        self.Conv_H2ToElec = [model.m.add_var(name= self.name + "H2ToElec", var_type = CONTINUOUS) for t in range(model.nSmpl)]
        
        ## add constraints
        # Electricity generation is limited by the installed capacity
        for t in range(model.nSmpl):
            model.m.add_constr(self.G_elec[t] <= self.C_G)

            # Hydrogen consumption constraint
            model.m.add_constr(self.Conv_H2ToElec[t] == self.G_elec[t] / ( model.LHV_H2 * self.eta_turbine ) )
    
        ## Add objective
        self.Cost = self.Cost + xsum(self.VC_G * self.G_elec[t] for t in range(model.nSmpl))
    



