import csv

def exportRes(model, filename, capacity = True, cost = True, generation = True, storage = True):
    model.filename = f'results/{filename}.csv'
    with open(model.filename, 'w', newline = '') as csvfile:
        csvwriter = csv.writer(csvfile)
        
        # create header
        csvwriter.writerow(['Technology','Variable', 'Hour','Value'])
        
        # export objective
        csvwriter.writerow(['Objective','Obj', 1, model.m.objective_value])
        
        if capacity == True:
            # export capacity
            for tech in model.tL:
                csvwriter.writerow([f'{tech.name}','C_G', 1, f'{tech.C_G.x}'])
            for tech in model.sL:
                csvwriter.writerow([f'{tech.name}', 'C_S', 1, f'{tech.C_S.x}'])
            for tech in model.hydroL:
                csvwriter.writerow([f'{tech.name}', 'C_S', 1, f'{tech.C_S.x}'])

        if cost == True:
            # export capacity
            for tech in model.tL:
                csvwriter.writerow([f'{tech.name}','Cost', 1, f'{tech.Cost.x}'])
                
        if generation == True:
            # export electricity generation by technology by hour
            for tech in model.pL:
                for t in range(model.nSmpl):
                    if tech.C_G.x > 0:
                        csvwriter.writerow([f'{tech.name}','G_elec', t+1, f'{tech.G_elec[t].x}'])
            
            # export hydrogen generation by technology by hour
            for tech in model.eL:
                for t in range(model.nSmpl):
                    if tech.C_G.x > 0:
                        csvwriter.writerow([f'{tech.name}','G_H2', t+1, f'{tech.G_H2[t].x}']) 
                        
            # export heat generation by technology by hour
            for tech in model.thL:
                for t in range(model.nSmpl):
                    if tech.C_G.x > 0:
                        csvwriter.writerow([f'{tech.name}','G_heat', t+1, f'{tech.G_heat[t].x}'])
            for tech in model.eL:
                for t in range(model.nSmpl):
                    if tech.eta_heat > 0:
                        csvwriter.writerow([f'{tech.name}','G_heat', t+1, f'{tech.G_heat[t].x}'])   
            
        if storage == True:            
            # export storage level and change in storage by technology by hour
            for tech in model.bL:
                if tech.C_S.x > 0:
                    for t in range(model.nSmpl+1):
                        csvwriter.writerow([f'{tech.name}','S_elec', t, f'{tech.S[t].x}'])
                    for t in range(model.nSmpl):
                        csvwriter.writerow([f'{tech.name}','dS_elec', t+1, f'{tech.delta_S[t].x}'])
            for tech in model.H2L:
                if tech.C_S.x > 0:
                    for t in range(model.nSmpl+1):
                        csvwriter.writerow([f'{tech.name}','S_H2', t, f'{tech.S[t].x}'])
                    for t in range(model.nSmpl):
                        csvwriter.writerow([f'{tech.name}','dS_H2', t+1, f'{tech.delta_S[t].x}'])
            for tech in model.thS:
                if tech.C_S.x > 0:
                    for t in range(model.nSmpl+1):
                        csvwriter.writerow([f'{tech.name}','S_heat', t, f'{tech.S[t].x}'])
                    for t in range(model.nSmpl):
                        csvwriter.writerow([f'{tech.name}','dS_heat', t+1, f'{tech.delta_S[t].x}'])
             