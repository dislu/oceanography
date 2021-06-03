'''This file has many functions some function are doing pre-processing, some doing cleaning and some are doing statistical analysis '''
def PDF(x,y,i,j,axs):
    import matplotlib.pyplot as plt   
    import pandas as pd                                                     
    plt.style.use('classic')                  
    import seaborn as sns
    sns.set()
    from netCDF4 import Dataset as nc
    
    #Dir='/home/dislu/Incois_nc/'
    DSWF=nc(x)
    MLD=nc(y)
    df = pd.DataFrame({'x':DSWF.variables['DSWF_AVG'][:],'y':MLD.variables['MLD_AVG'][:]})
    with sns.axes_style('white'):                                                          
         return sns.jointplot("x", "y", df,kind='reg',ax=axs[i,j])
# Create a function we'll use to interpolate and plot

def interpolate_and_plot(df, interpolation_type):
    import pandas as pd
    import matplotlib.pyplot as plt
    # Create a boolean mask for missing values
    missing_values = df.isna()
    # Interpolate the missing values
    df_interp = df.interpolate(interpolation_type)
    # Plot the results, highlighting the interpolated values in black
    fig, ax = plt.subplots(figsize=(10, 5))
    df_interp.plot(color='blue', alpha=.6, ax=ax, legend=False)
                             
    # Now plot the interpolated values on top in red
    df_interp[missing_values].plot(ax=ax, color='red', lw=3, legend=False)
    plt.show()
# Your custom function

def percent_change(series):
      import matplotlib.pyplot as plt
      import numpy as np
      # Collect all *but* the last value of this window, then the final value
      previous_values = series[:len(series)-1]
      last_value = series[-1]
      # Calculate the % difference between the last value and the mean of earlier values
      percent_change = (last_value - np.mean(previous_values)) / np.mean(previous_values)
      return percent_change
      # Apply your custom function and plot
      #df_perc = df.rolling(20).apply(percent_change)
      #df_perc.loc["2014":"2015"].plot()
      #plt.show()
def replace_outliers(series):
      # Calculate the absolute difference of each timepoint from the series mean
      import numpy as np
      absolute_differences_from_mean = np.abs(series - np.mean(series))
              
      # Calculate a mask for the differences that are > 3 standard deviations from zero
      this_mask = absolute_differences_from_mean > (np.std(series) * 3)
                          
      # Replace these values with the median accross the data
      series[this_mask] = np.nanmedian(series)
      return series
      # Apply your preprocessing function to the timeseries and plot the results
      #prices_perc = prices_perc.apply(replace_outliers)
      #prices_perc.loc["2014":"2015"].plot()
      #plt.show()
def adfullertest(series, signif=0.05, name='', verbose=False):
           """Perform ADFuller to test for Stationarity of given series and print report""" 
           import statsmodels
           from statsmodels.tsa.stattools import adfuller
           r= adfuller(series, autolag='AIC') 
           output = {'test_statistic':round(r[0], 4), 'pvalue':round(r[1], 4), 'n_lags':round(r[2], 4), 'n_obs':r[3]}
           p_value = output['pvalue'] 
           def adjust(val, length= 6): return str(val).ljust(length) 
           # Print Summary 
           print(' Augmented Dickey-Fuller Test on '+name, '\n', '-'*47) 
           print(' Null Hypothesis: Data has unit root. Non-Stationary.') 

           print(' Significance Level = ',signif) 
           print(' Test Statistic = ',output['test_statistic']) 
           print(' No. Lags Chosen = ',output['n_lags']) 

           for key,val in r[4].items():
               print(' Critical value ',adjust(key),' =', round(val, 3)) 
          # print(type(p_value),type(sing)
           if (p_value <= signif): 
              print(' => P-Value = ',p_value,'. Rejecting Null Hypothesis.') 
              print(" => Series is Stationary.") 
           else: 
              print(" => P-Value = ",p_value,". Weak evidence to reject the Null Hypothesis.") 
              print(" => Series is Non-Stationary.") 

#from statsmodels.tsa.stattools import grangercausalitytests 
#maxlag=12
#test = 'ssr_chi2test'
def grangers_causation_matrix(data, variables, test='ssr_chi2test', verbose=False):
    import pandas as pd
    import numpy as np
    maxlag=30
    test = 'ssr_chi2test'
    from statsmodels.tsa.stattools import grangercausalitytests
    X_train = pd.DataFrame(np.zeros((len(variables), len(variables))), columns=variables, index=variables)
    for c in X_train.columns: 
        for r in X_train.index:
            test_result = grangercausalitytests(data[[r, c]], maxlag=maxlag, verbose=False)
            p_values = [round(test_result[i+1][0][test][1],4) for i in range(maxlag)] 
            if verbose: 
               print('Y =',r,'X = ',c, 'P Values =',p_valuesy) 
            min_p_value = np.min(p_values) 
            X_train.loc[r, c] = min_p_value 
    X_train.columns = [var + 'x' for var in variables] 
    X_train.index = [var + '_y' for var in variables] 
    return X_train 
#grangers_causation_matrix(Xtrain, variables = Xtrain.columns)


