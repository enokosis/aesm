from .technology import Technology #For some reason importing inside package (technoliges here) works better with "from .module import Class_or_Function"
from mip import Model, xsum, minimize, BINARY, mip, MAXIMIZE, MINIMIZE, CONTINUOUS

# Electrolyzer is the super class and there can be different subclasses
# for different types of electrolyzers (e.g. AWE (Alkaline Water Electrolyzer), SOE (Solid Oxide)...)
        
class Electrolyzer(Technology):

    def __init__(self, RampU = 1, RampD = 1, VC_H2=0, eta_elec=1.058, eta_heat = 0,  **kwargs):

        super().__init__(**kwargs)

        self.RampU = RampU
        self.RampD = RampD
        self.eta_elec = eta_elec
        self.eta_heat = eta_heat


    def add_to_model(self, model):
        super().add_to_model(model)

        self.G_H2 = [model.m.add_var(name= self.name + "G_H2", var_type = CONTINUOUS) for t in range(model.nSmpl)]
        self.G_heat = [model.m.add_var(name= self.name + "G_heat", var_type = CONTINUOUS) for t in range(model.nSmpl)]
        self.Conv_ElecToH2AndHeat  = [model.m.add_var(name= self.name + "ElecToH2", var_type = CONTINUOUS) for t in range(model.nSmpl)]
        
        for t in range(model.nSmpl):
            # production cannot exceed capacity
            model.m.add_constr(self.G_H2[t] * model.LHV_H2 / self.eta_elec <= self.C_G)
            
            # electricity consumption constraint
            model.m.add_constr(self.Conv_ElecToH2AndHeat[t] == self.G_H2[t] * model.LHV_H2 / self.eta_elec )
            # heat production constraint
            model.m.add_constr(self.G_heat[t] == self.G_H2[t] * model.LHV_H2 * (1/self.eta_elec - 1/1.058) )
        
        # change in hydrogen production cannot exceed ramp-up / ramp-down time
        for t in range(1,model.nSmpl):
            model.m.add_constr( (self.G_H2[t] - self.G_H2[t-1] ) * model.LHV_H2 / self.eta_elec <= self.C_G * self.RampU)
            model.m.add_constr( (self.G_H2[t-1] - self.G_H2[t] ) * model.LHV_H2 / self.eta_elec <= self.C_G * self.RampD)
        
        # Add objective
        self.Cost = (self.CAPEX_G * self.R + self.FC_G) * self.C_G + xsum(self.VC_G * self.G_H2[t] for t in range(model.nSmpl))
        
class AWE(Electrolyzer):
    
    def add_to_model(self,model):
        super().add_to_model(model)
        
    