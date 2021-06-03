'''This program create a suitable timeseries data for calculating cross-correlation(xcorr() function in matplotlib)
and plots Window lag cross correlation on heat map'''

def WTLC_plot(file_x,file_y):
    from netCDF4 import Dataset as nc 
#    from Seasonal_WTLC_Corr import WTLC_Corr
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    from Seasonal_WTLC_Corr import SWTLC_Corr
    from pylab import savefig
    df2 = nc('/incois_ncmrwfx/incois/hycom/ARVIND_SINGH/HYCOM_TS/BOX/'+file_y)
    df1 = nc('/incois_ncmrwfx/incois/hycom/ARVIND_SINGH/HYCOM_TS/BOX/'+file_x)
    dfx = df1.variables['DSWF_AVG'][:] 
    dfy = df2.variables['MLD_AVG'][:] 
    sx=pd.Series(dfx)
    sy=pd.Series(dfy)
    datax=sx.interpolate(method='polynomial', order=2)
    datay=sy.interpolate(method='polynomial', order=2) 
    for i in range(len(datax)): 
        if(np.isnan(datax[i])==True): 
           datax[i]=datax[i+1] 
        if(np.isnan(datay[i])==True): 
           datay[i]=datay[i+1]
        if(np.isnan(datax[len(datax)-1])==True):         
           datax[i]=datax[i-1]                
        if(np.isnan(datay[len(datay)-1])==True):                    
           datay[i]=datay[i-1]
    fig = plt.figure()
    Heat_map=SWTLC_Corr(datax,datay)
    dir='/incois_ncmrwfx/incois/hycom/ARVIND_SINGH/HYCOM_TS/IMG/'
    file_s=file_x.split('/')
    file_name=file_s[len(file_s)-1].split('_')[1]
    Heat_map.savefig(dir+file_s[0]+'/'+file_name+'_WLXCorr.png')
    









