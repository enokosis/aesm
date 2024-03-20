
import math
from mip import Model, xsum, minimize, BINARY, mip, MAXIMIZE, MINIMIZE, CONTINUOUS
from .powerPlants import PowerPlant
from .storage import HydroReservoir


class Dam(PowerPlant):

    def __init__(self, outflow, initStorage, inflow, CAPEX_S = 0, FC_S = 0, Cmin = 0, Cmax = math.inf, **kwargs):
        super().__init__(**kwargs)
        self.reservoir = HydroReservoir(outflow_min=outflow, name= "Dam reservoir", CAPEX = CAPEX_S, FC = FC_S, initStorage = 0.2)
        self.inflow = inflow#Inflow of energy to the reservoir at time t

        self.Cmin = Cmin
        self.Cmax = Cmax
    
    def add_to_model(self, model):
        super().add_to_model(model)  
        self.reservoir.add_to_model(model, inflow = self.inflow )
        
        self.Bypass = [model.m.add_var(name= self.name + " Bypass", var_type = CONTINUOUS) for t in range(model.nSmpl)]
        
        for t in range(model.nSmpl):
            model.m.add_constr(self.G_elec[t] <= self.C)
            model.m.add_constr(self.reservoir.discharge[t] == self.G_elec[t] + self.Bypass[t])
        
        model.m.add_constr(self.C >= self.Cmin)
        model.m.add_constr(self.C <= self.Cmax)
        

        