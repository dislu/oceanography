def Decompose(df,x):
  from statsmodels.tsa.seasonal import seasonal_decompose
  from dateutil.parser import parse
  import matplotlib.pyplot as plt
  # Multiplicative Decomposition 
  result_mul = seasonal_decompose(df[x], model='multiplicative', extrapolate_trend='freq')

  # Additive Decomposition
  result_add = seasonal_decompose(df[x], model='additive', extrapolate_trend='freq')

  # Plot
  plt.rcParams.update({'figure.figsize': (10,10)})
  result_mul.plot().suptitle('Multiplicative Decompose', fontsize=22)
  result_add.plot().suptitle('Additive Decompose', fontsize=22)
  plt.show()
