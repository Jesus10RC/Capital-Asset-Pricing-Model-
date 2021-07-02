# -*- coding: utf-8 -*-
"""
Create classes

"""

import numpy as np
import pandas as pd
import matplotlib as mpl
import scipy
import importlib
import matplotlib.pyplot as plt
from scipy.stats import skew, kurtosis, chi2

# Import our own Function and Class files and Reload
import stream_functions
importlib.reload(stream_functions)

class jarque_bera_test():
    
    def __init__(self, x, x_str):
        self.returns = x
        self.str_name = x_str 
        self.size = len(x) #Size of returns
        self.round_digits = 4
        self.mean = 0.0
        self.stdev = 0.0
        self.skew = 0.0
        self.kurt = 0.0
        self.median = 0.0
        self.var_95 = 0.0
        self.cvar_95 = 0.0
        self.jarque_bera = 0.0
        self.p_value = 0.0
        self.is_normal = 0.0
        
    def compute(self):
        self.mean = np.mean(self.returns)
        self.stdev = np.std(self.returns)    #Volatility 
        self.skew = skew(self.returns)
        self.kurt = kurtosis(self.returns) # excess kurtosis 
        self.sharpe = self. mean / self.stdev * np.sqrt(252)
        self.median = np.median(self.returns)
        self.var_95 = np.percentile(self.returns,5)
        self.cvar_95 = np.mean(self.returns[self.returns <= self.var_95]) 
        self.jarque_bera = self.size/6*(self.skew**2 + 1/4*self.kurt**2)
        self.p_value = 1 - chi2.cdf(self.jarque_bera, df=2) #Degree Freedom 
        self.is_normal = (self.p_value > 0.05 ) #Equivalenty x_jarque_bera < 6
        
        
    def __str__(self):
        str_self = self.str_name + ' / size ' + str(self.size) + '\n' + self.plot_str()
        return str_self
    
        
    def plot_str(self):
        # Print Metrics in Graph
        round_digits = 4
        plot_str = 'mean ' + str(np.round(self.mean,self.round_digits))\
            + ' / std dev ' + str(np.round(self.stdev,self.round_digits))\
            + ' / skewness ' + str(np.round(self.skew, self.round_digits))\
            + ' / kurtosis ' + str(np.round(self.kurt, self.round_digits))\
            + ' / Sharpe ratio ' + str(np.round(self.sharpe, self.round_digits)) + '\n'\
            + 'VaR 95% ' + str(np.round(self.var_95, self.round_digits))\
            + ' / CVaR 95% ' + str(np.round(self.cvar_95, self.round_digits))\
            + ' / Jarque_Bera ' + str(np.round(self.jarque_bera, self.round_digits))\
            + ' / p_value ' + str(np.round(self.p_value, self.round_digits))\
            + ' / is_normal ' + str(self.is_normal)

        return plot_str