import numpy as np
from mip import Model, xsum, minimize, BINARY, mip, MAXIMIZE, MINIMIZE, CONTINUOUS


import pandas as pd
import math

class Demand():
    # The class stores demand for electricity (D_elec), hydrogen (D_H2) and heat (D_heat) 
    def __init__(self):
        self.demands = {
            'D_Elec' :[],   # e.g. MWh electricity
            'D_H2' :[],     # e.g. kg H2
            'D_Heat' :[]    # e.g. MWh heat
        }
        
    def setDemand(self, D_Type, arr):
        if D_Type in self.demands:
            self.demands[D_Type] = arr
        else:
            raise ValueError(f"Unknown demand type: {D_Type}")

class Scenario:
    def __init__(self, techList, demand, scenarioName = "New scenario", nSmpl=20, LHV_H2 = 0.0333):
        self.externFiles= False
        self.techList=techList
        self.demand=demand 
        self.scenarioName = scenarioName 
        self.nSmpl =nSmpl
        self.LHV_H2 = LHV_H2

    def readCsv(self, fname, col, start_row = None):
        """
        Parameters:
            fname (str): file path
            col (int): column number from which data is downloaded (1-index)
            start_row (int): first row of data (1-index) (optional)
        """
        if start_row is None:
            df=pd.read_csv(fname, usecols = [col-1])
        else:
            df=pd.read_csv(fname, usecols = [col], skiprows = start_row -2)            
            
        data=df[0:self.nSmpl].values.flatten()
        return data

    def readExcel(self, fname, col, start_row = None, sheet_name = None):
        """
        Parameters:
            fname (str): file path
            col (str): column from which data is downloaded
            start_row (int): first row of data (1-index) (optional)
            sheet_name (str): sheet name from which data is downloaded (if more than one sheet)
        """
        if start_row is None:
            if sheet_name is None:
                df=pd.read_excel(fname, usecols=col)       
            else:
                df=pd.read_excel(fname, usecols=col, sheet_name = sheet_name)    
        else:
            if sheet_name is None:
                print(start_row)
                df=pd.read_excel(fname, usecols=col, skiprows = start_row-2)
            else:
                df=pd.read_excel(fname, usecols=col, skiprows = start_row-2, sheet_name = sheet_name)
                
        data = df[0:self.nSmpl].values.flatten()
        return data

    def hourlyProfile(self, mode="Const", value=1):
        period = [0]*self.nSmpl
        for i in range(self.nSmpl):
            match mode:
                case "Const":
                    period[i]= value
                case "Rising":
                    period[i]= value*i/(self.nSmpl)
                case "Falling":
                    period[i]= value- value*i/(self.nSmpl)
                case "Sin":
                    period[i]= value*(1 + math.sin(i/4) / 2)
                case "Cos":
                    period[i]= value*(1 + math.cos(i/5) / 2 )
                case "Arch":
                    x = np.linspace(0, np.pi, self.nSmpl)
                    period[i]= np.absolute(math.sin(x[i]))
        return period

