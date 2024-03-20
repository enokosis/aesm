import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

class HydroReservoir():

    def __init__(self):

        self.g_t=[]
        self.g_capacity=[]
        self.s_t=[]
        self.s_capacity=[]
        self.in_t=[]
        self.out_t=[]
        self.bypass_t=[]
        self.out_minimum_t=[]
        
    
    def read_FI(self,fname):
        data=pd.read_csv(fname, skiprows=22,
                              sep = '\s+|\t+|\s+\t+|\t+\s+',
                              engine='python')
        # Each data value corresponds to the inflow energy
        # for last 7 day period. Therefore divide by 7*24,
        # assume a constant flow per hour, and convert to hourly
        # values. Use the median values from the data.
        self.in_t=np.zeros((365,24))
        for i in range(24):
            self.in_t[:,i]=data['Median']/(7*24)
        self.in_t=self.in_t.flatten()
        
        print(self.in_t)
        # According to Afry report
        # https://www.fingrid.fi/globalassets/dokumentit/fi/sahkomarkkinat/kehityshankkeet/dalyve-fingrid_flexibility-study_final-report_v300-id-151641.pdf
        # approximately 45% of the hydro capacity is 
        
        
        
        
