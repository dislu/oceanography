import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pycwt as wavelet
from netCDF4 import Dataset as nc
#from WTCorr_e import 
# Data
#data1 = dict(name='Long Wave', nick='LW', 
 #            file='filt_30-120days_lw_gfs_dly_15N65E_2012-2016.csv')
#data2 = dict(name='Sea Surface Temp', nick='SST', 
 #            file='filt_30-120days_sst_hycom_dly_15N65E_2012-2016.csv')

#t1, s1, date1 = np.loadtxt(data1['file'], unpack=True)
#t2, s2, date2 = np.loadtxt(data2['file'], unpack=True)
df1 = nc('/incois_ncmrwfx/incois/hycom/ARVIND_SINGH/HYCOM_TS/BOX/2012-16/avg/gfs_BOB_avg.nc')
df2 = nc('/incois_ncmrwfx/incois/hycom/ARVIND_SINGH/HYCOM_TS/BOX/2012-16/avg/mld_BOB_avg.nc')

dfx =df1.variables['DSWRF_AVG'][:]
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
t1 = df1.variables['TIME'][:]
t2 = df2.variables['TAX'][:]
date1 = [2012,2013,2014,2015,2016]
date2 = [2012,2013,2014,2015,2016]
date1=np.asarray(date1)
date2 = np.asarray(date2)
# Requirements for Wavelet
dt = 1
n1 = len(datax)
n2 = len(datay)
n = min(n1, n2)
mother = wavelet.Morlet(6)
s1 =datax
s2 =datay
# Normalization (see arguments of XWT & WCT)
std1 = s1.std()
std2 = s2.std()
#s1 = (s1 - s1.mean()) / std1
#s2 = (s2 - s2.mean()) / std2


# Power Spectrum : XWT finds regions in time frequency space where 
# the time series show high common power.
W12, cross_coi, freq, signif = wavelet.xwt(s1, s2, dt,
                                           significance_level=0.95,
                                           wavelet='morlet', normalize='True')


cross_power = np.abs(W12)**2
cross_sig = np.ones([1, n]) * signif[:, None]
cross_sig = cross_power / cross_sig  # Power is significant where ratio > 1
cross_period = 1/freq
avg_W12=np.average(W12)

# Coherence : WCT finds regions in time frequency space where the two 
# time series co-vary, but do not necessarily have high power.
WCT, aWCT, corr_coi, freq, sig = wavelet.wct(s1, s2, dt, 
                                             significance_level=0.95,
                                             wavelet='morlet', normalize=True,
                                             cache=True)

cor_sig = np.ones([1, n]) * sig[:, None]
cor_sig = np.abs(WCT) / cor_sig  # Power is significant where ratio > 1
cor_period = 1 / freq
avg_WCT=np.average(WCT)
#print(WCT.shape)

# Calculates the phase between both time series. 
#u, v = np.sin(aWCT), np.cos(aWCT)	#NORTH is in-phase
u, v = np.cos(aWCT), np.sin(aWCT)	#EAST is in-phase
#np.savetxt("phaseangle.csv",aWCT.T[0:,0:],delimiter="\t",fmt="%.4f") 
				 #Transpose to write in Excel



# Time Delay from Phase Angle
phase_diff = aWCT #(120,1827) matrix
periodmat = np.tile(cross_period,(1826,1)) #cross_sig was (1,120).Duplicate to (1827,120)
period = periodmat.T #Transpose to (120,1827)
time_diff = (phase_diff*period) / (2*np.pi) #timelag = phasediff / (2*pi*freq)
#np.savetxt("time_diff_T.csv",time_diff.T[0:,0:],delimiter="\t",fmt="%.4f")
					#Transpose to write in Excel


# First sub-figure
pow_levels = np.arange(np.floor(np.log2(cross_power).min()), 
			np.ceil(np.log2(cross_power).max())+10, 10)

ax1 = plt.axes([0.1, 0.55, 0.75, 0.35])
xwt_spect = ax1.contourf(t1, np.log2(cross_period), np.log2(cross_power),
			  levels = pow_levels, cmap=plt.cm.jet)
ax1.contour(t1, np.log2(cross_period), cross_sig, [-99,1], colors='k',
            linewidths=1.5)
ax1.fill(np.concatenate([t1, t1[-1:]+dt, t1[-1:]+dt, t1[:1]-dt, t1[:1]-dt]),
         np.concatenate([np.log2(cross_coi), [1e-9], np.log2(cross_period[-1:]),
                         np.log2(cross_period[-1:]), [1e-9]]),
         'k', alpha=0.5)
ax1.quiver(t1[::15], np.log2(cross_period[::15]), u[::15,::15], v[::15,::15],
           units='width', angles='uv', pivot='mid', linewidth=0.25, scale=70,
           edgecolor='k', width=0.002, headwidth=3, headlength=5,
           headaxislength=4.5, minshaft=1, minlength=1)

ax1.set_title('Cross-Wavelet Power')
ax1.set_ylabel('Period (days)')
Yticks_cross = 2 ** np.arange(np.log2(cross_period).min(), 
				np.log2(cross_period).max(),0.5)
#print(Yticks_cross)
#print(np.log2(Yticks_cross))
#Yticks_cross[0]=1

Y_tickcross=np.delete(Yticks_cross,np.where(Yticks_cross.astype(int)&(Yticks_cross.astype(int)-1)!=0))
Y_tickcross[1]=1
ax1.set_yticks(np.log2(Y_tickcross))
ax1.set_yticklabels(Y_tickcross.astype(int))
ax1.set_xticks(t1[::366]) 
ax1.set_xticklabels(date1[::366].astype(int))
ax1.set_xticklabels(["2012","2013","2014","2015","2016","2017"])
plt.colorbar(xwt_spect, ax=ax1, location='right')


# Second sub-figure
coh_levels = np.arange(np.floor(WCT.min()), np.ceil(WCT.max())+0.1, 0.1)

ax2 = plt.axes([0.1, 0.1, 0.75, 0.35], sharex=ax1)
wct_coh = ax2.contourf(t1, np.log2(cor_period), WCT, levels=coh_levels, 
			cmap=plt.cm.jet)
ax2.contour(t1, np.log2(cor_period), cor_sig, [-99, 1], colors='k', 
            linewidths=1.5)
ax2.fill(np.concatenate([t1, t1[-1:]+dt, t1[-1:]+dt, t1[:1]-dt, t1[:1]-dt]),
         np.concatenate([np.log2(corr_coi), [1e-9], np.log2(cor_period[-1:]), 
                         np.log2(cor_period[-1:]), [1e-9]]),
         'k', alpha=0.5)
ax2.quiver(t1[::15], np.log2(cor_period[::15]), u[::15,::15], v[::15,::15],
           units='width', angles='uv', pivot='mid', linewidth=0.25, scale=70,
           edgecolor='k', width=0.002, headwidth=3, headlength=5,
           headaxislength=4.5, minshaft=1, minlength=1)

ax2.set_title('Wavelet Coherence Transform')
ax2.set_ylabel('Period (days)')
Yticks_cor = 2 ** np.arange(np.log2(cor_period).min(),np.log2(cor_period).max(), 0.5)
Y_tickcor=np.delete(Yticks_cor,np.where(Yticks_cor.astype(int)&(Yticks_cor.astype(int)-1)!=0))
Y_tickcor[1]=1
ax2.set_yticks(np.log2(Y_tickcor))
ax2.set_yticklabels(Y_tickcor.astype(int))
plt.colorbar(wct_coh, ax=ax2, location="right")


ax1.set_ylim(np.log2(2), np.log2(512))
ax2.set_ylim(np.log2(2), np.log2(512))
#ax1.set_ylim(np.log2(period.min()),np.log2(period.max()))
# Third sub-figure
print(np.mean(WCT,axis=1))
print(cross_period)
ax3 = plt.axes([0.8,0.1,0.15,0.35])
ax3.plot(np.mean(WCT,axis=1),np.log2(cor_period))
S_cor = 2 ** np.arange(np.log2(cor_period).min(),np.log2(cor_period).max(), 0.5)
ax3.set_xlabel('average coherence')
ax3.set_xticks([0.2,0.4,0.6,0.8,0.9,1])
ax3.set_xticklabels([0.2,0.4,0.6,0.8,0.9,1])
plt.show()

