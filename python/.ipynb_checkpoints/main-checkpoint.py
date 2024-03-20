from hydroReservoir import HydroReservoir
import powerPlants as pp
from model import ModelRunner
import visualizer as visu

import user_input as ui



def capFacGraph(model):
    visu.plotScenario(model, ui.demand)
    #visu.graphAllCapFac(model.pL)
    #visu.graphStorage(model.sL)
    #visu.demandSupply(demand.D_BaseElec)
fname='data/FI-hydro-inflow.txt'
h=HydroReservoir()
h.read_FI(fname)


# Create model runner 


#Set up and run scenrio with power demand of 1000
#runner.run_scenario(G=1000)ö
#capFacGraph(runner)
#runner.getRes()
for scenario in ui.scenariosToRun:
    runner = ModelRunner(scenario.techList, scenario.demand)
    runner.run_model()
    runner.getRes()
    capFacGraph(runner)
    

