from mip import Model, xsum, minimize, BINARY, MINIMIZE, MAXIMIZE, CONTINUOUS, maximize


import technologies.powerPlants as pp
import technologies.electrolyzer as elec
import technologies.storage as stor
import user_input as ui
import technologies.thermal as th

class ModelRunner():
    def __init__(self, scenario):
        
        
        self.nSmpl =scenario.nSmpl
        self.m = Model(sense = MINIMIZE)

        self.demand = scenario.demand.demands
        self.LHV_H2 = scenario.LHV_H2
        
        tL = scenario.techList
        self.tL = tL #List of avaliable technologies in the problem
        self.pL = [tech for tech in tL if isinstance(tech, pp.PowerPlant)]
        self.solarL = [tech for tech in tL if isinstance(tech, pp.SolarPower)]
        self.windL = [tech for tech in tL if isinstance(tech, pp.WindPower)]
        self.nuclearL = [tech for tech in tL if isinstance(tech, pp.Nuclear)]
        self.hydroL = [tech for tech in tL if isinstance(tech, pp.Hydro)]                                               
        self.gtL = [tech for tech in tL if isinstance(tech, pp.GasTurbine)]
        self.eL = [tech for tech in tL if isinstance(tech, elec.Electrolyzer)]
        self.sL = [tech for tech in tL if isinstance(tech, stor.Storage)]
        self.H2L = [tech for tech in tL if isinstance(tech, stor.H2Storage)]   # H2storage list
        self.bL = [tech for tech in tL if isinstance(tech, stor.Battery)]   # battery list
        self.thL = [tech for tech in tL if isinstance(tech, th.HeatPump)]   # thermal generation
        self.thS = [tech for tech in tL if isinstance(tech, stor.HeatStorage)] # thermal storage

        self.G_sum = []
                
    def setupVarsConstr(self):
        # Clear the model
        self.m.clear() 
        

        # Add technology-specific variables and constraints
        for tech in self.tL:
            tech.add_to_model(self)

        # Demand-supply balance
        for t in range(self.nSmpl):
           
            G_elecTot = xsum(i.G_elec[t] for i in self.pL)
            delta_S_elecTot = xsum(i.delta_S[t] for i in self.bL) 

            D_BaseElec = self.demand['D_Elec'][t]
            Conv_ElecToH2AndHeatTot = xsum(i.Conv_ElecToH2AndHeat[t] for i in self.eL) + xsum( i.Conv_ElecToH2[t] for i in self.H2L)
            Conv_ElecToHeatTot = xsum(i.Conv_ElecToHeat[t] for i in self.thL)
            Conv_H2ToElecTot = xsum(i.Conv_H2ToElec[t] for i in self.gtL)
            
            # Constraints depend on the usage of storages
            if len(self.demand.get('D_Elec', [])) > 0:
                if len(self.bL) == 0:
                    self.m.add_constr( G_elecTot - D_BaseElec- Conv_ElecToH2AndHeatTot 
                                      - Conv_ElecToHeatTot >= 0  )    
                else:
                    self.m.add_constr( G_elecTot- delta_S_elecTot- D_BaseElec- Conv_ElecToH2AndHeatTot 
                                      - Conv_ElecToHeatTot == 0  )
            if len(self.demand.get('D_H2', [])) > 0:
                if len(self.H2L) == 0:
                    self.m.add_constr( xsum(i.G_H2[t] for i in self.eL) 
                                     - self.demand['D_H2'][t] - Conv_H2ToElecTot >= 0 )
                else:
                    self.m.add_constr( xsum(i.G_H2[t] for i in self.eL) 
                                      - xsum(i.delta_S[t] for i in self.H2L) - self.demand['D_H2'][t] - Conv_H2ToElecTot == 0 )
            if len(self.demand.get('D_Heat', [])) > 0:
                if len(self.thS) == 0:
                    self.m.add_constr( xsum(i.G_heat[t] for i in self.thL) + xsum(i.G_heat[t] for i in self.eL) 
                                      - self.demand['D_Heat'][t] >= 0)
                else:
                    self.m.add_constr( xsum(i.G_heat[t] for i in self.thL) + xsum(i.G_heat[t] for i in self.eL) 
                                      - xsum(i.delta_S[t] for i in self.thS) - self.demand['D_Heat'][t] == 0)

    def addObjective(self):    
        # Set objective function as sum of expenses
        self.m.objective= minimize( xsum( i.Cost for i in self.tL))


    def run_model(self):
        self.setupVarsConstr()
        self.addObjective()
        self.m.optimize()

