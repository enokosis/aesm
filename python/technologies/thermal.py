from .technology import Technology #For some reason importing inside package (technoliges here) works better with "from .module import Class_or_Function"
from mip import Model, xsum, minimize, BINARY, mip, MAXIMIZE, MINIMIZE, CONTINUOUS


        
class HeatingTech(Technology):

    def __init__(self, COP_relative, COP_max = 1, **kwargs):
        super().__init__(**kwargs)
        self.COP_max = COP_max
        self.COP_relative = COP_relative


    def add_to_model(self, model):
        super().add_to_model(model)
        self.G_heat = [model.m.add_var(name= self.name + " G_heat", var_type = CONTINUOUS) for t in range(model.nSmpl)]
        self.Conv_ElecToHeat  = [model.m.add_var(name= self.name + " ElecToHeat", var_type = CONTINUOUS) for t in range(model.nSmpl)]
        
        
        for t in range(model.nSmpl):
            model.m.add_constr(self.Conv_ElecToHeat[t] <= self.C_G)
            model.m.add_constr(self.Conv_ElecToHeat[t] == self.G_heat[t] / (self.COP_max * self.COP_relative[t]) )
       
        self.Cost = (self.CAPEX_G * self.R + self.FC_G) * self.C_G + xsum(self.VC_G * self.G_heat[t] for t in range(model.nSmpl))
             
class HeatPump(HeatingTech):
    
    def add_to_model(self,model):
        super().add_to_model(model)
        
