import technologies.powerPlants as pp
import technologies.electrolyzer as elec
import technologies.storage as stor
import technologies.thermal as th
from scenario import Demand, Scenario
import numpy as np
import math



## Modelling Example 1

# set up scenario
demand = Demand()
scenarioExample1 = Scenario(techList =[], demand =demand, scenarioName = "My First Scenario", nSmpl=720, LHV_H2 = 0.0333)

# add electricity demand of 100 MW for each time step
scenarioExample1.demand.setDemand('D_Elec', scenarioExample1.hourlyProfile(value =100))

# add wind power
scenarioExample1.techList.append(pp.WindPower( CAPEX_G = 1200000, R = 0.005, FC_G = 1200, AF = scenarioExample1.hourlyProfile(value = 0.8), name = "Wind Power plant 1"))


##Modelling example 2

demand = Demand()
# Define the scenario
advanced_energy_scenario = Scenario( techList=[], demand=demand, scenarioName="Advanced Energy Mix Scenario", nSmpl=720, LHV_H2=0.0333)

# Setting demand values
advanced_energy_scenario.demand.setDemand('D_Elec', advanced_energy_scenario.hourlyProfile(value=100, mode="Cos"))
advanced_energy_scenario.demand.setDemand('D_H2', advanced_energy_scenario.hourlyProfile(value=30, mode="Const"))

# Adding Nuclear Power Plant
advanced_energy_scenario.techList.append(pp.Nuclear( CAPEX_G=1600000, R=0.004, FC_G=1800, VC_G=9, RampU=0.05, RampD=0.05, AF_max=0.94, AF_min=0, C_Gmin=20, name="Nuclear power plant" ))

# Adding Offshore Wind Power Plant
advanced_energy_scenario.techList.append(pp.WindPower( CAPEX_G=1100000, R=0.005, FC_G=1200, VC_G=0, name="Offshore Wind power plant", AF=advanced_energy_scenario.hourlyProfile(value=0.8, mode="Arch") ))

# Adding Solar Power Plant
advanced_energy_scenario.techList.append(pp.SolarPower( CAPEX_G=600000, R=0.005, FC_G=400, VC_G=0, name="Solar power plant", AF=advanced_energy_scenario.hourlyProfile(value=0.8, mode="Sin"), C_Gmax=30 ))

# Adding Battery System
advanced_energy_scenario.techList.append(stor.Battery( CAPEX_S=320000, CAPEX_G=240000, R=0.0012, FC_S=500, FC_G=400, eta_discharge=0.927, eta_charge=0.927, eta_selfDischarge=0.000071, DOD=0.8, name="Battery 1" ))

# Adding Electrolyzer (AWE Type)
advanced_energy_scenario.techList.append(elec.AWE( CAPEX_G=500000, R=0.01, FC_G=900, VC_G=0, RampU=1, RampD=1, eta_elec=0.67, name="AWE electrolyzer" ))


## Modelling Example 3

# set up
scenarioExample3 = []
demand = Demand()
for i in range(3):
    # add new scenario to list
    scenarioExample3.append( Scenario(techList =[], demand = demand, scenarioName = "Scenario Example 3 iter "+f"{i+1}", nSmpl=720, LHV_H2 = 0.0333) )
    
    # add demand profiles for electricity and hydrogen. Electricity demand is taken from external file
    scenarioExample3[i].demand.setDemand('D_Elec', scenarioExample3[i].readExcel('data/electricityDemand_FI.xlsx', "E"))
    scenarioExample3[i].demand.setDemand('D_H2', scenarioExample3[i].hourlyProfile(value = 17000)) 
    
    # add wind power with real world availability factors
    scenarioExample3[i].techList.append(pp.WindPower( CAPEX_G = 1200000, R = 0.005, FC_G = 1200, AF = scenarioExample3[i].readCsv("data/wind_FI.csv", col=2, start_row=2), name = "Wind1"))
    # add solar power with real world availability factors
    scenarioExample3[i].techList.append(pp.SolarPower( CAPEX_G = 750000, R= 0.005, FC_G = 880, C_Gmax = 1000, C_Gmin = 100, AF = scenarioExample3[i].readExcel("data/solar_FI.xlsx", "B", sheet_name="Ark1"), name= "Solar1"))
    # add nuclear power. CAPEX increases with every iteration
    scenarioExample3[i].techList.append(pp.Nuclear( CAPEX_G = 2500000 + 500000*i, R= 0.006, FC_G = 5000, VC_G=10, RampU= 0.4, RampD= 0.4, AF_min = 0, AF_max= 0.94, name= "Nuclear"))
    # add gas turbine using pure hydrogen
    scenarioExample3[i].techList.append(pp.GasTurbine( CAPEX_G = 1100000, R= 0.005, FC_G = 1000, eta_turbine = 0.45, name= "GasTurbine"))
    # add hydro power
    scenarioExample3[i].techList.append(pp.Hydro( CAPEX_G = 1300000, CAPEX_S = 220000, R= 0.005, FC_G = 1000, FC_S = 900, Inflow = scenarioExample3[i].readExcel("data/hydro_FI.xlsx", "B"), Outflow_min = 200, C_Gmax = 3300, name= "Hydro"))
    
    # add electrolyzer
    scenarioExample3[i].techList.append(elec.AWE(CAPEX_G = 900000, R = 0.006, FC_G = 900, RampU = 1, RampD = 1, eta_elec = 0.70,  name = "AWE"))
    
    # add electric battery and hydrogen storage
    scenarioExample3[i].techList.append(stor.Battery(CAPEX_G = 250000, CAPEX_S = 280000, R= 0.007, FC_G = 250, FC_S = 250, eta_charge = 0.90, eta_discharge = 0.90, eta_selfDischarge = 0.0001, DOD = 0.8, name = "Battery"))
    scenarioExample3[i].techList.append(stor.H2Storage(CAPEX_G = 5000, CAPEX_S = 50, R= 0.005, FC_G = 80,  FC_S = 0.8, eta_charge = 1, eta_discharge = 1, eta_selfDischarge = 0, alpha_pump = 0.003, name = "H2Storage"))


scenariosToRun = [scenarioExample1] # Modelling Examples 1

#scenariosToRun = scenarioExample3[0:] # Modelling Example 3



