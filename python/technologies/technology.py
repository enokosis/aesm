import numpy as np
import pandas as pd

from mip import Model, xsum, minimize, BINARY, mip, MAXIMIZE, MINIMIZE, CONTINUOUS
import math



class Technology:
    def __init__(self, name, CAPEX_G = 0, FC_G = 0, VC_G = 0, R = 0):
        self.name = name
        self.R = R
        self.CAPEX_G = CAPEX_G
        self.FC_G = FC_G
        self.VC_G = VC_G

    def add_to_model(self, model):
        
        # Generation capacity is added for each technology
        self.C_G = model.m.add_var(name= self.name + " C_G", var_type = CONTINUOUS)
        
        # Add objective
        self.Cost = (self.CAPEX_G * self.R + self.FC_G) * self.C_G 
