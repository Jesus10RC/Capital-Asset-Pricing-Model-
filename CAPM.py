# -*- coding: utf-8 -*-
"""
CAPM

"""

import numpy as np
import pandas as pd
import matplotlib as mpl
import scipy
import importlib
import matplotlib.pyplot as plt
from scipy.stats import skew, kurtosis, chi2, linregress

import stream_functions
importlib.reload(stream_functions)
import stream_classes
importlib.reload(stream_classes)

#Input Parameters 
ric = '^VIX' # SAN.MC BBVA.MC VWS.CO MXN=X AMZN ^VIX
benchmark = '^S&P'  #^STOXX50E ^STOXX ^S&P ^NASD ^IPC ^CAC40 
file_extension = 'scv'
nb_decimals = 4

# Loading data from csv or Excel file 
x1, str1, t1 = stream_functions.load_time_series(ric)
x2, str2, t2 = stream_functions.load_time_series(benchmark)

#Synchronize Timetamps
timetamp1 = list(t1['date'].values)
timetamp2 = list(t2['date'].values)
timetamps =list(set(timetamp1) & set(timetamp2))

# Synchronised Time Series for x1 or ric
t1_sync = t1[t1['date'].isin(timetamps)]
t1_sync.sort_values(by='date', ascending=True)
t1_sync = t1_sync.reset_index(drop=True)

#Synchronised Time Series for x2 or Benchmark
t2_sync = t2[t2['date'].isin(timetamps)]
t2_sync.sort_values(by='date', ascending=True)
t2_sync = t2_sync.reset_index(drop=True)

#Table of Returns for ric and benchmark
t = pd.DataFrame()
t['data'] = t1_sync['date']
t['price_1'] = t1_sync['close']
t['price_2'] = t2_sync['close']
t['return_1'] = t1_sync['returns_close']
t['return_2'] = t2_sync['returns_close']

#Compute Vectors of Returns
y = t['return_1'].values
x = t['return_2'].values 

# Linear Regression of ric  with respect to benchmark
slope, intercept, r_value, p_value, std_err = linregress(x,y)
slope = np.round(slope, nb_decimals)
intercept = np.round(intercept, nb_decimals)
p_value = np.round(p_value, nb_decimals)
null_hypothesis = p_value > 0.05 #p_value<0.05 Reject null hypothesis
r_value = np.round(r_value, nb_decimals) #Correlation Coefficient
r_squared = np.round(r_value**2, nb_decimals) # Pct of Variance of "y" explained by "x"
predictor_linreg = slope*x + intercept

#Scatterplot of returns
str_title = 'Scaterplot of returns' + '\n'\
    + 'linear regression / ric ' + ric\
    + '/ benchmark ' + benchmark + '\n'\
    + 'alpha (intercept)' + str(intercept)\
    + '/ beta (slope) ' + str(slope) + '\n'\
    + 'p-value ' + str(p_value)\
    + '/ null hypothesis ' + str(null_hypothesis) + '\n'\
    + 'r-value ' + str(r_value)\
    + ' / r_squared ' + str(r_squared)
plt.figure()
plt.title(str_title)
plt.scatter(x, y)
plt.plot(x, predictor_linreg, color='green')
plt.ylabel(ric)
plt.xlabel(benchmark)
plt.grid()
plt.show()


