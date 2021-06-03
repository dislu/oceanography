#!/usr/bin/python
'''This programme converts excel files having uneven timesteps into an even timesteps netcdf files   '''
import pandas as pd
import time
import datetime as dt
import numpy as np
import os,glob
import sys
from datetime import datetime as dt
from netCDF4 import Dataset as ncd
from mknc_omni_3d_uvts import make_ncuv
from mknc_omni_3d_uvts import make_ncts
from netcdftime import utime
# this function convert time from string format to numerical format
def dt2jd(dte):
    import time
    import datetime as dt
    idtg=str(dte)
    idtgref=str(1900123100)
    format = '%Y%m%d%H'
    dtgref=dt.datetime.strptime(idtgref,format)
    dtg=dt.datetime.strptime(idtg,format)
    ndtg=dtg.strftime(format)
    dateDiff = dtg - dtgref
    jd=dateDiff.days
    return(jd,ndtg)
# convert excel file to netCDF file format
def excel2nc(infl):
    nctime=utime('days since 1900-12-31 00:00:00')
    dfrmt=('%d.%m.%y %H:%M:%S')
    dhfmt=('%Y-%m-%dH%H')
    decimal_fmt = "{:.3f}"
    in_excel=infl
    print in_excel
    db=pd.read_excel(in_excel)
    df=db.replace('-',-9999.0)
    ii=-1
    for mb in df[df.dtypes.index[0]].T[:]:
        ii=ii+1
        try:
            print df[df.dtypes.index[2]].T[:].values[ii]
	    nct=dt.strptime(str(df[df.dtypes.index[2]].T[:].values[ii]),dfrmt)
	    tstmp=nctime.date2num(nct)
	    ftstmp=decimal_fmt.format(tstmp)
	    print nct.strftime(dhfmt),ftstmp
	    ncfl_A=mb +"_"+str(ftstmp) +'_uvsd.nc'
	    ncfl_B=mb +"_"+str(ftstmp) +'_ts.nc'
	    curspd=df[df.dtypes.index[16:23]].T[ii].values
	    curdir=df[df.dtypes.index[23:30]].T[ii].values
	    temp=df[df.dtypes.index[32:42]].T[ii].values
	    salt=df[df.dtypes.index[43:53]].T[ii].values
	    raddir=np.radians(curdir)
	    omu=curspd*np.cos(raddir)
	    omv=curspd*np.sin(raddir)
	    lat=df[df.dtypes.index[6]][ii]
	    lon=df[df.dtypes.index[7]][ii]
	    print ncfl_A,tstmp,lon,lat,'dir= ',len(curdir),'spd= ',len(curspd)
	    print ncfl_B,tstmp,lon,lat,'temp= ',len(temp),'salt= ',len(curspd)
	    if os.path.exists(ncfl_A)==False : make_ncuv(ncfl_A,tstmp)
	    if os.path.exists(ncfl_B)==False : make_ncts(ncfl_B,tstmp)
	    ncf_A=ncd(ncfl_A,'a','NETCDF4_CLASSIC')
	    ncf_B=ncd(ncfl_B,'a','NETCDF4_CLASSIC')
	    print mb,curdir
	    #UVSD
	    ncf_A['latitude'][:]=lat
	    ncf_A['longitude'][:]=lon
	    ncf_A['time'][:]=tstmp
	    ncf_A['curspd'][0,:,0,0]=curspd
            ncf_A['curdir'][0,:,0,0]=curdir
            ncf_A['omu'][0,:,0,0]=omu
	    ncf_A['omv'][0,:,0,0]=omv
	    #TS
	    ncf_B['latitude'][:]=lat
	    ncf_B['longitude'][:]=lon
	    ncf_B['time'][:]=tstmp
	    ncf_B['temp'][0,:,0,0]=temp
	    ncf_B['salt'][0,:,0,0]=salt
            ncf_A.close()
            ncf_B.close()
        except ValueError:
           print("Oops!  That was no valid number.  Try again...")
    return
for file in glob.glob("*.xls"):
    print(file)
    excel2nc(file)
