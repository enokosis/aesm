from model import ModelRunner
import visualizer as visu
from mip import Model, xsum, minimize, BINARY, MINIMIZE, MAXIMIZE, CONTINUOUS, maximize
from resultExport import exportRes
import yamled

import user_input as ui

#Process results, graph them and output to file
def resultProcessor(model, msg):
    def getRes():
        #Short console report about required capacity per technology and total cost
        print("---Required generation capacity:")
        for tech in model.tL:
            print(f'{tech.name} = {tech.C_G.x}')
        print("---Required storage capacity:")
        for tech in model.sL:
            print(f'{tech.name} = {tech.C_S.x}')
        for tech in model.hydroL:
            print(f'{tech.name} = {tech.C_S.x}')

        print("---Objective value = ", model.m.objective_value)
        #By making console report more verbose value of ever MIP variable is displayed along with electriicty generation
        #Useful when xdebugging
        verbose = False
        if verbose:
            for v in model.m.vars:
                print('{} : {}'.format(v.name, v.x))
            for t in range(model.nSmpl):
                model.G_sum.append(xsum(i.G_elec[t].x for i in model.pL)) 
                print( model.G_sum[t])   
    getRes()
    exportRes(model, msg, capacity=True, generation=True, storage = True) 
    visu.plotScenario(model, model.demand, msg, mode="subplot")

# Create model runner 
YAML_to_RUN = 'yaml_files/example2.yaml'
YAML_mode = False  # True = YAML used as user input, FALSE = user_input.py used as user input


def main_function():
    if(YAML_mode):
        scenariosToRun = yamled.scenarios
        for scenario_name, scenario_obj in scenariosToRun(file= YAML_to_RUN).items():
        
            runner = ModelRunner(scenario_obj)
            runner.run_model()
            resultProcessor(runner, scenario_obj.scenarioName)
    else:
        
        for scenario in ui.scenariosToRun:
            runner = ModelRunner(scenario)
            runner.run_model()

            resultProcessor(runner, scenario.scenarioName)

if __name__ == "__main__":
    main_function()
