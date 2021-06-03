from netCDF4 import Dataset as nc
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
#df1=nc("")
from pylab import savefig
def SWTLC_Corr(datax,datay):
    #windowed time lagged cross correlation
    days = 1
    fps = 30
    no_splits = 12
    samples_per_split = len(datax)/no_splits
    S_days=[60,90,90,90,91]
    sum=0
    S_sum=[0]*len(S_days)
    for i in range(len(S_days)):
        sum = sum+S_days[i]
        S_sum[i] = sum
   # samples_per_split = len(month_days)/no_splits
    rss=[]
    Days=0
    for t in S_sum:
        #  Days=Days+t
        #  d1 = df['S1_Joy'].loc[(t)*samples_per_split:(t+1)*samples_per_split]
          d1 = datax[Days:t]
        #  print(d1)
          d1x=(d1-np.mean(d1))/np.std(d1)
        #  d2 = df['S2_Joy'].loc[(t)*samples_per_split:(t+1)*samples_per_split]
          d2 = datay[Days:t]
          d2y= (d2-np.mean(d2))/np.std(d2)
          rs =[plt.xcorr(d1x,d2y,maxlags=30) for lag in range(-30,31)] 
          rss.append(rs[0][1])
          print(rs[0][1],Days,t,fps)
          Days = t
    rss = pd.DataFrame(rss)
  #  fig = plt.figure()
    print(rss)
    f,ax = plt.subplots(figsize=(10,5)) 
    Heat_map=sns.heatmap(rss,cmap='RdBu_r',ax=ax)
    ax.set(title='Windowed Time Lagged Cross Correlation',xlim=[0,60], xlabel='Offset',ylabel='Window epochs')
    ax.set_xticks([0, 2, 4, 6, 8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,38,40,42,44,46,48,50,52,54,56,58,60])
    ax.set_xticklabels([-30,-28,-26,-24,-22,-20,-18,-16,-14,-12,-10,-8,-6, -4, -2, 0, 2,4,6,8,10,12,14,16,18,20,22,24,26,28,30]);
    ax.set_yticks([0,1,2,3,4])
    ax.set_yticklabels(["JF'12","DJF'13","DJF'14","DJF'15","DJF'16"])
    return Heat_map.get_figure()
# Rolling window time lagged cross correlation
def RWTLC_Corr():
    seconds = 5
    fps = 30
    window_size = 300 #samples
    t_start = 0
    t_end = t_start + window_size
    step_size = 30
    rss=[]
    while t_end < 5400:
          d1 = df['S1_Joy'].iloc[t_start:t_end]
          d2 = df['S2_Joy'].iloc[t_start:t_end]
          rs = [plt.xcorr(d1,d2, lag) for lag in range(-int(seconds*fps),int(seconds*fps+1))]
          rss.append(rs)
          t_start = t_start + step_size
          t_end = t_end + step_size
    rss = pd.DataFrame(rss)
  
    f,ax = plt.subplots(figsize=(10,10))
    sns.heatmap(rss,cmap='RdBu_r',ax=ax)
    ax.set(title='Rolling Windowed Time Lagged Cross Correlation',xlim=[0,301], xlabel='Offset',ylabel='Epochs')
    ax.set_xticks([0, 50, 100, 151, 201, 251, 301])
    ax.set_xticklabels([-150, -100, -50, 0, 50, 100, 150]);

