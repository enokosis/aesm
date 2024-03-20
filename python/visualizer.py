import numpy as np
import matplotlib.pyplot as plt

import pandas as pd

font = {'family' : 'serif',
        'weight' : 'normal',
        'size'   : 18}

plt.rc('font', **font)


def plot_combined_electricity(graph, x, model):
    Cons_elec_df = pd.DataFrame(index=x)
    Cons_elec_df["Base demand"]= [var for var in model.demand["D_Elec"]]
    for tech in model.eL:
        Cons_elec_df[tech.name]= [var.x for var in tech.Conv_ElecToH2AndHeat]  
    for tech in model.thL:
        Cons_elec_df[tech.name]= [var.x for var in tech.Conv_ElecToHeat] 
    # Sort the columns by their sums in descending order
    Cons_elec_df = Cons_elec_df[Cons_elec_df.sum().sort_values(ascending=False).index]
    Cons_elec_df.plot(ax=graph, kind='bar', stacked=True, width=0.5, linewidth = 3,
           title='Combined electricity consumption by hour')
    graph.set_ylabel('Electricity consumption [MWh]') 

def plot_battery_level(graph, x, model):
    for tech in model.bL:
        graph.plot(x, [var.x for var in tech.S[0:]], label=tech.name)
    graph.set_ylabel('Battery storage level [MWh]') 
    graph.set_title('Battery storage level by hour')

def plot_stacked_electricity(graph, x, model):
    G_elec_df = pd.DataFrame(index=x)
    for tech in model.pL:
        G_elec_df[tech.name]= [var.x for var in tech.G_elec]   
    for tech in model.bL:
        G_elec_df[tech.name]= [-var.x for var in tech.delta_S]  
    Cons_elec_df_ToT = G_elec_df.sum(axis=1)
    graph.plot(x, Cons_elec_df_ToT, label = "Cons.", zorder =2, linewidth = 3, color = "black")
    G_elec_df.plot(ax=graph, kind='bar', stacked=True, width=0.5,
           title='Stacked electricity supply and consumption by hour', zorder = 1) 
    graph.set_ylabel('Electricity supply and consumption [MWh]') 
    
def plot_stacked_hydrogen_prod(graph, x, model):
    for tech in model.eL:
        graph.bar(x, [var.x for var in tech.G_H2], label=tech.name + " prod.")
    graph.plot(x, model.demand['D_H2'], label = "H2 demand") # base hydrogen demand
    graph.set_xlabel('Hour')
    graph.set_ylabel('H2 production and demand [kg H2]') 
    graph.legend(loc='upper right') 
    graph.set_title('Hydrogen production and demand by hour')

def plot_hydrogen_demand_supply(graph, x, model):
    H2_df = pd.DataFrame(index=x)
    for tech in model.eL:
        H2_df[tech.name]= [var.x for var in tech.G_H2]     
    for tech in model.H2L:
        H2_df[tech.name]= [-var.x for var in tech.delta_S]
    for tech in model.gtL:
        H2_df[tech.name]= [-var.x for var in tech.Conv_H2ToElec]  
    H2_df["Base demand"]= [-var for var in model.demand['D_H2']]
    H2_df.plot(ax= graph, kind='bar', stacked=True, width=0.5, linewidth = 3)
    graph.set_xlabel('Hour')
    graph.set_ylabel('H2 combined supply and demand by hour') 
    graph.legend(loc='upper right') 
    graph.set_title('H2 combined production by hour')
    
def plot_H2_storage_level(graph, x, model):
    for tech in model.H2L:
        graph.plot(x, [var.x for var in tech.S[0:]], label=tech.name)
    graph.set_xlabel('Hour')
    graph.set_ylabel('H2 storage level [kg H2]') 
    graph.legend() 
    graph.set_title('Hydrogen storage level by hour')

def plot_heat_demand_supply(graph, x, model):
    G_heat_df = pd.DataFrame(index=x)
    for tech in model.thL:
        G_heat_df[tech.name]= [var.x for var in tech.G_heat] 
    for tech in model.eL:
        G_heat_df[tech.name]= [var.x for var in tech.G_heat]     
    for tech in model.thS:
        G_heat_df[tech.name]= [-var.x for var in tech.delta_S]
    G_heat_df["Heat demand"] = [-var for var in model.demand['D_Heat']]
    #graph.plot(x, HeatDemand_df, label = "Heat demand", zorder =2, linewidth = 3, color = "black")
    G_heat_df.plot(ax= graph, kind='bar', stacked=True, width=0.5,
           title='Stacked heat supply and demand by hour', zorder = 1)    
    graph.set_xlabel('Hour')
    graph.set_ylabel('Heat supply and demand [MWh]') 
    graph.legend(loc='upper right') 

def apply_common_settings(graph, x):
    graph.legend(loc='upper right')
    graph.set_xlabel('Hour')
    tick_step = max(1, int((max(x) - min(x)) / 20))  # Ensure at least 1
    graph.set_xticks(np.arange(min(x), max(x) + 1, tick_step))

def plotScenario(model, demand, msg, mode="subplot"): 

    x = np.arange(model.nSmpl)
    x1 = np.arange(model.nSmpl+1)

    # List of plotting functions/tasks you want to execute with coordinates
    plotting_tasks = [
        {"func": plot_combined_electricity, "x": x, "coordinates": (0, 0)},
        {"func": plot_stacked_electricity, "x": x, "coordinates": (1, 0)},
        {"func": plot_battery_level, "x": x1, "coordinates": (2, 0)},
        #{"func": plot_stacked_hydrogen_prod, "x": x, "coordinates": (0, 1)},
        #{"func": plot_hydrogen_demand_supply, "x": x, "coordinates": (1, 1)},
        #{"func": plot_H2_storage_level, "x": x1, "coordinates": (2, 1)},
        #{"func": plot_heat_demand_supply, "x": x, "coordinates": (0, 2)},
        # Add more plotting functions if needed
    ]

    # Determines the maximum row and column based on provided coordinates
    max_row = max([task["coordinates"][0] for task in plotting_tasks])
    max_col = max([task["coordinates"][1] for task in plotting_tasks])

    if mode == "subplot":
        fig, axes = plt.subplots(nrows=max(1, max_row+1), ncols= max_col+1, figsize=(33, 7*(max_row+1)))  # Adjusted the figure size
        fig.suptitle(msg, fontsize=18)
        # Ensure axes is always a 2D array
        if max_row == 0:
            axes = np.expand_dims(axes, axis=0)
        if max_col == 0:
            axes = np.expand_dims(axes, axis=1)
        # Iterate through plotting tasks and apply them to the specified subplots
        for task in plotting_tasks:
            row, col = task["coordinates"]
            task["func"](axes[row, col], task["x"], model)
            apply_common_settings(axes[row, col], task["x"])
        # Hide any subplot axes that weren't specified in plotting_tasks
        for row in range(max_row+1):
            for col in range(max_col+1):
                if (row, col) not in [task["coordinates"] for task in plotting_tasks]:
                    axes[row, col].axis('off')
        plt.tight_layout()
        plt.show()

    elif mode == "separate":
        for task in plotting_tasks:
            fig, ax = plt.subplots(figsize=(11, 7))
            fig.suptitle(msg, fontsize=16)
            task["func"](ax, task["x"], model)
            apply_common_settings(ax, task["x"])
            plt.show()  # This will display each figure immediately
