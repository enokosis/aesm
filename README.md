# An Energy System Model


## Description
This is an energy system modelling tool for the modelling of electricity, hydrogen, and heat production. The model was built with Python MIP using object oriented programming. The object oriented strucutre allows for the addition of many instances of the same class, e.g. wind power plants with different parameters. 

The model uses linear optimization to allow for fast execution. The model assumes that each time step is ONE HOUR. If other time step is used, the model constraints should be revised.

The model can be found in the 'python' folder. Please refer to the instructions manual for detailed documentation of the model.

## Installation
The model is implemented entirely with Python. We however recommend installing Anaconda as this comes with helpful programs and packages, including Python, Jupyter (detailed modelling example instructions are in Jupyter Notebook), and Spyder (an IDE).

Python-MIP can be easily installed with Python Package Index by entering in the command prompt:

    pip install mip

## Examples
We have added three modelling examples to help you get started with the tool. Here is a short description on how to execute the examples using <mark>user_input.py</mark>. The example is also available in YAML format. You can toggle between YAML based input and 'user_input.py' by changing YAML_mode either True or False in <mark>main.py</mark>. For further instructions, refer to the instructions manual or to the Jupyter Notebook.

### Modelling Example 1

In the first example, only electricity prodction is modelled with one wind turbine technology. The model is initialized by creating instances of demand and scenario classes. Scenario name, number of time steps (nSmpl = 720 hours, or one month in hours), and lower heating value of hydrogen (0.0333 MWh / kg H2) are given as the scenario inputs.


    # set up scenario
    demand = Demand()
    scenarioExample1 = Scenario(techList =[], demand =demand, scenarioName = "My First Scenario", nSmpl=720, LHV_H2 = 0.0333)

Next we will set a constant electricity demand of 100 MW per hour by calling <mark>hourlyProfile</mark> in <mark>scenario.py</mark>. With <mark>hourlyProfile</mark>, you can easily simulate different demand or generation profiles. The default profile is a constant of one for each hour, but here the demand is set to 100 with input parameter <mark>value=100</mark>. Varying profiles are introduced in the second example.
    
    # add electricity demand of 100 MW for each time step
    scenarioExample1.demand.setDemand('D_Elec', scenarioExample1.hourlyProfile(value =100))

Next, a wind power technology is added. We assume a CAPEX of 1 200 000 EUR / MW, expected capital return of 0.5% per month, fixed costs of 1 200 EUR / MW per month and constat availability factor of 0.8. 

Please note that fixed costs and annuity factor should be adjusted based on the simulation time. CAPEX and variable costs should be independent of the simulation time.

    # add wind power
    scenarioExample1.techList.append(pp.WindPower( CAPEX_G = 1200000, R = 0.005, FC_G = 1200, AF = scenarioExample1.hourlyProfile(value = 0.8), name = "Wind Power plant 1"))

Finally, the scenario is added to scenarioToRun list.

    scenariosToRun = [scenarioExample1] # Modelling Examples 1 and 2

Now we should be all set. You can now run the model in <mark>main.py</mark>.


### Modelling Example 2

Let's continue with a bit more advanced scenario. Again, the demand and scenario need to be initialized first. Let's again set a simulation time of one month (720 hours). 
    
    demand = Demand()
    # Define the scenario
    advanced_energy_scenario = Scenario( techList=[], demand=demand, scenarioName="Advanced Energy Mix Scenario", nSmpl=720, LHV_H2=0.0333)

Next we add a varying electricity demand by calling <mark>mode="Cos"</mark> in <mark>hourlyProfile</mark>. Constant hydrogen demand of 30 kg per hour is also added. 
    
    # Setting demand values
    advanced_energy_scenario.demand.setDemand('D_Elec', advanced_energy_scenario.hourlyProfile(value=100, mode="Cos"))
    advanced_energy_scenario.demand.setDemand('D_H2', advanced_energy_scenario.hourlyProfile(value=30, mode="Const"))

Next we add nuclear, offshore wind, and solar power plants. You can see from the 'technologies' folder all the available technologies and their possible input arguments. Note that certain parameters are inherited from the parent (super) classes.

    # Adding Nuclear Power Plant
    advanced_energy_scenario.techList.append(pp.Nuclear( CAPEX_G=1600000, R=0.004, FC_G=1800, VC_G=9, RampU=0.05, RampD=0.05, AF_max=0.94, AF_min=0, C_Gmin=20, name="Nuclear power plant" ))
    
    # Adding Offshore Wind Power Plant
    advanced_energy_scenario.techList.append(pp.WindPower( CAPEX_G=1100000, R=0.005, FC_G=1200, VC_G=0, name="Offshore Wind power plant", AF=advanced_energy_scenario.hourlyProfile(value=0.8, mode="Arch") ))
    
    # Adding Solar Power Plant
    advanced_energy_scenario.techList.append(pp.SolarPower( CAPEX_G=600000, R=0.005, FC_G=400, VC_G=0, name="Solar power plant", AF=advanced_energy_scenario.hourlyProfile(value=0.8, mode="Sin"), C_Gmax=30 ))

Next we add a battery system and an alkaline water electrolyzer to the technology mix Please note that the battery has both storage and power components.

    # Adding Battery System
    advanced_energy_scenario.techList.append(stor.Battery( CAPEX_S=320000, CAPEX_G=240000, R=0.0012, FC_S=500, FC_G=400, eta_discharge=0.927, eta_charge=0.927, eta_selfDischarge=0.000071, DOD=0.8, name="Battery 1" ))
    
    # Adding Electrolyzer (AWE Type)
    advanced_energy_scenario.techList.append(elec.AWE( CAPEX_G=500000, R=0.01, FC_G=900, VC_G=0, RampU=1, RampD=1, eta_elec=0.67, name="AWE electrolyzer" ))

Finally, the scenario is added to scenarioToRun list.

    scenariosToRun = [advanced_energy_scenario] # Modelling Examples 1 and 2

You can now run the model in <mark>main</mark>.

You might have noticed that the plots do not include plots on hydrogen production. To visualize these, go to the function <mark>plotScenario</mark> in <mark>visualizer.py</mark> and uncomment the lines including hydrogen. You can also create plots of your own or modify the existing plots in visualizer.

Now all the plots are shown as subplots in one figure. You can display the plots separately by going to <mark>main</mark> and by changing the input argument <mark>mode</mark> from "subplot" to "separate" when calling <mark>visu.plotScenario</mark>.

### Modelling Example 3

Let's assume that you would like to study how nuclear power's investment costs might affect the optimal technology mix in an energy system. In this case, running scenarios in a loop becomes useful.

First, a list of scenarios is added and demand is initialized.

    # set up
    scenarioExample3 = []
    demand = Demand()

We add three scenarios to the list in a loop. Again, simulation time of 720 hours is set to allow for fast run time. Full year simulations take typically a couple minutes for each scenario.

    for i in range(3):
        # add new scenario to list
        scenarioExample3.append( Scenario(techList =[], demand = demand, scenarioName = "Scenario Example 3 iter "+f"{i+1}", nSmpl=720, LHV_H2 = 0.0333) )

This time we use real world data from Finland for the demand profiles. External CSV and Excel files can be read easily using the readCsv and readExcel functions defined in the <mark>Scenario</mark> class in <mark>scenario.py</mark>. You can specify the column and the first row from which data is downloaded for both file types. Additionally, the sheet can be specified for CSV files. These functionalities are demonstrated with wind and solar data.
        
        # add demand profiles for electricity and hydrogen. Electricity demand is taken from external external file. 
        scenarioExample3[i].demand.setDemand('D_Elec', scenarioExample3[i].readExcel('data/electricityDemand_FI.xlsx', "E"))
        scenarioExample3[i].demand.setDemand('D_H2', scenarioExample3[i].hourlyProfile(value = 17000)) 
        
Let's also add wind and solar power technologies with real world availability factor data. Availability / capacity factors can be downloaded e.g. from renewables.ninja. 
        
        # add wind power with real world availability factors
        scenarioExample3[i].techList.append(pp.WindPower( CAPEX_G = 1200000, R = 0.005, FC_G = 1200, AF = scenarioExample3[i].readCsv("data/wind_FI.csv", col=1, start_row=2), name = "Wind1"))
        # add solar power with real world availability factors
        scenarioExample3[i].techList.append(pp.SolarPower( CAPEX_G = 750000, R= 0.005, FC_G = 880, C_Gmax = 1000, C_Gmin = 100, AF = scenarioExample3[i].readExcel("data/solar_FI.xlsx", "B", sheet_name="Ark1"), name= "Solar1"))

We also add nuclear and hydro power plant as well as gas turbine using pure hydrogen to the power mix. Please note that nuclear power's CAPEX increases with every iteration. Hydro power plant is assumed to have both storage and power components. Data on hydro energy inflow in Finland is available at ymparisto.fi.

        # add nuclear power. CAPEX increases with every iteration
        scenarioExample3[i].techList.append(pp.Nuclear( CAPEX_G = 2500000 + 500000*i, R= 0.006, FC_G = 5000, VC_G=10, RampU= 0.4, RampD= 0.4, AF_min = 0, AF_max= 0.94, name= "Nuclear"))
        # add gas turbine using pure hydrogen
        scenarioExample3[i].techList.append(pp.GasTurbine( CAPEX_G = 1100000, R= 0.005, FC_G = 1000, eta_turbine = 0.45, name= "GasTurbine"))
        # add hydro power
        scenarioExample3[i].techList.append(pp.Hydro( CAPEX_G = 1300000, CAPEX_S = 220000, R= 0.005, FC_G = 1000, FC_S = 900, Inflow = scenarioExample3[i].readExcel("data/hydro_FI.xlsx", "B"), Outflow_min = 200, C_Gmax = 3300, name= "Hydro"))

Next, we add electrolyzer, electric battery, and hydrogen storage to the technology mix.

        # add electrolyzer
        scenarioExample3[i].techList.append(elec.AWE(CAPEX_G = 900000, R = 0.006, FC_G = 900, RampU = 1, RampD = 1, eta_elec = 0.70,  name = "AWE"))
        
        # add electric battery and hydrogen storage
        scenarioExample3[i].techList.append(stor.Battery(CAPEX_G = 250000, CAPEX_S = 280000, R= 0.007, FC_G = 250, FC_S = 250, eta_charge = 0.90, eta_discharge = 0.90, eta_selfDischarge = 0.0001, DOD = 0.8, name = "Battery"))
        scenarioExample3[i].techList.append(stor.H2Storage(CAPEX_G = 5000, CAPEX_S = 50, R= 0.005, FC_G = 80,  FC_S = 0.8, eta_charge = 1, eta_discharge = 1, eta_selfDischarge = 0, alpha_pump = 0.003, name = "H2Storage"))

Finally, the list of scenarios is added to scenariosToRun.

    scenariosToRun = scenarioExample3[0:] # Modelling Example 3

You can now run the model in <mark>main</mark>.

The model results are exported to the results folder. In <mark>main</mark>, you can specify in the <mark>exportRes</mark> function what type of results are exported. Just set the parameter to True or False depending on whether you want to export capacities, hourly generation or storage levels by technology type.

You can try adding heat production and demand to the sytem. Currently we have included electrolyzers and heat pumps as heat production technologies. Please refer to the Jupyter Notebook or the instructions manual for more information on the model.

## Authors
Authors: Eero Hirvijoki, Sami Tarvainen, and Arkadii Kolchin.
