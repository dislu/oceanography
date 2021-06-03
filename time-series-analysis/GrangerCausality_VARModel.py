x='/incois_ncmrwfx/incois/hycom/ARVIND_SINGH/HYCOM_TS/BOX/2012-16/avg/Weekly_gfs_BOB_avg.nc'
y='/incois_ncmrwfx/incois/hycom/ARVIND_SINGH/HYCOM_TS/BOX/2012-16/avg/Weekly_mld_BOB_avg.nc'
# %load Pdf_reg.py 
import matplotlib.pyplot as plt    
import pandas as pd                                                      
plt.style.use('classic')                   
import seaborn as sns 
sns.set() 
from netCDF4 import Dataset as nc 
    
 #Dir='/home/dislu/Incois_nc/' 
GFS=nc(x) 
MLD=nc(y) 
df = pd.DataFrame({'MLD_AVG':MLD.variables['MLD_AVG'][:]})
for var in GFS.variables.keys()-GFS.dimensions.keys():
    df[var]=GFS.variables[var][:]
df.index=pd.date_range(start='1/1/2012',end='30/12/2016',freq='W')
df.head(20)

#df.index=pd.date_range('2012-01-01','30-12-2016',freq='W')
# plot all the variables in separate figures
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
# Plot
fig, axes = plt.subplots(nrows=3, ncols=2, dpi=120, figsize=(10,6))
for i, ax in enumerate(axes.flatten()):
  data = df[df.columns[i]]
  ax.plot(data, color='red', linewidth=1)
  # Decorations
  ax.set_title(df.columns[i])
  ax.xaxis.set_ticks_position('none')
  ax.yaxis.set_ticks_position('none')
  ax.spines['top'].set_alpha(0)
  ax.tick_params(labelsize=6)
  plt.tight_layout();

import numpy as np 
date = np.array('2012-01-01', dtype=np.datetime64) 
date 
df.index=date+np.arange(1826)
#interpolate_and_plot(df,'zero') 
df_inter=df.interpolate('zero')
df_inter['y'][0]=df_inter['y'][1]
df_trans=df.diff().dropna()
# agumented dickey-Fuller test
from Pdf_reg import adfullertest
for name, column in df_trans.iteritems(): 
          adfullertest(column,name=column.name) 
          print('\n')
# Granger's causation test
from Pdf_reg import grangers_causation_matrix
Granger_mat=grangers_causation_matrix(df_trans, variables = df_trans.columns)
print(Granger_mat)
# VAR model
import statsmodels.tsa.api as smt
from statsmodels.tsa.api import VAR
mod = smt.VAR(df_trans)
#first method
res = mod.fit(maxlags=30, ic='AIC')
print(res.summary())
# second method
x1 = mod.select_order(maxlags=30) 
print(x1.summary())
# after selecting the log having Minimum AIC
model_fitted = mod.fit(29) 
model_fitted.summary()
# adjust function
def adjust(val, length= 6): return str(val).ljust(length)
# durbin watson test
from statsmodels.stats.stattools import durbin_watson 
out = durbin_watson(model_fitted.resid) 
  
for col, val in zip(df_trans.columns, out): 
     print(adjust(col), ':', round(val, 2))

# transform data into percent change
from Pdf_reg import interpolate_and_plot, percent_change, replace_outliers
interpolate_and_plot(df,'zero')
df_perc = df.rolling(50).apply(percent_change) 
df_perc.loc["2014":"2015"].plot() 
plt.show()
# replace outlier 
df_perc = df_perc.apply(replace_outliers) 
df_perc.loc["2014":"2015"].plot() 
plt.show()

