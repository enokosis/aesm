import numpy as np
import pandas as pd
from cfg import nSmpl
from mip import Model, xsum, minimize, BINARY, mip, MAXIMIZE, MINIMIZE, CONTINUOUS
import math

class Technology:
    def __init__(self, name, CAPEX, R=0, FC=0):
        self.name = name
        self.CAPEX = CAPEX
        self.R = R
        self.FC = FC
        
    def add_to_model(self, model):

        self.C = model.add_var(name= self.name + " C", var_type = CONTINUOUS)
        

class PowerPlant(Technology):
    def __init__(self,  VC_electricity=0, VC_heat=0, aP= np.zeros(nSmpl) , **kwargs):
        super().__init__(**kwargs)
        
        self.VC_electricity = VC_electricity #VC - variable cost like Fuel
        self.VC_heat = VC_heat
        self.aP= aP #aP - power capacity factor at every hour of the year 
               
    def add_to_model(self, model):
        super().add_to_model(model)
        self.G_elec = [model.add_var(name= self.name + " G_elec", var_type = CONTINUOUS) for t in range(nSmpl)]
        

      
class HydroReservoir(PowerPlant):

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
        self.in_t=np.zeros(nSmpl)
        for i in range(24):
            self.in_t[:,i]=data['Median']/(7*24)
            #print(self.in_t)
            # According to Afry report
            # https://www.fingrid.fi/globalassets/dokumentit/fi/sahkomarkkinat/kehityshankkeet/dalyve-fingrid_flexibility-study_final-report_v300-id-151641.pdf
            # approximately 45% of the hydro capacity is 
        self.in_t=self.in_t.flatten()

class WindPower(PowerPlant):
    
    def __init__(self, Cmin = 0, Cmax = 1000000, **kwargs):
        super().__init__(**kwargs)

        self.Cmin = Cmin
        self.Cmax = Cmax
        
    def add_to_model(self, model):
        super().add_to_model(model)
        
        # Curtailment allows for the shut down of the wind power plant
        self.Curtail = [model.add_var(name= self.name + " Curtail", var_type = CONTINUOUS) for t in range(nSmpl)]
        
        # Electricity generation is defnied by capacity factor and installed capacity
        for t in range(nSmpl):
            model.add_constr(self.G_elec[t] + self.Curtail[t] == self.aP[t] * self.C)

        model.add_constr(self.C >= self.Cmin)
        model.add_constr(self.C <= self.Cmax)
    
        
class SolarPanel(PowerPlant):
    
    def add_to_model(self,model):
        super().add_to_model(model)
        # Electricity generation is defnied by capacity factor and installed capacity
        for t in range(nSmpl):
            model.add_constr(self.G_elec[t] == self.aP[t] * self.C)
        
def hourlyProfile(mode="Const", value=1):
    period = [0]*nSmpl
    for i in range(nSmpl):
        match mode:
            case "Const":
                period[i]= value
            case "Rising":
                period[i]= value*i/(nSmpl)
            case "Falling":
                period[i]= value- value*i/(nSmpl)
            case "Sin":
                period[i]= value*(1 + math.sin(i) / 2)
            case "Cos":
                period[i]= value*(1 + math.cos(i) / 2 )
            case "Arch":
                x = np.linspace(0, np.pi, nSmpl)
                period[i]= np.absolute(math.sin(x[i]))

    return period

    
    
    
    
    
    
    
    
    