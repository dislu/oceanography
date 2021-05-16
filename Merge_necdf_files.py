'''This program is for merging daily netCDF files, comprising missing files, into a one large netCDF file'''
from netCDF4 import Dataset as nc
from netCDF4 import num2date, date2num
from datetime import datetime, timedelta
import numpy as np
import time
import os
import numpy.ma as ma
import glob
#path for reading files
path= '/incois_ncmrwfx/incois/hycom/ARVIND_SINGH/HYCOM_TS/GFS/2015T'
#path for writting files
path_write ='/incois_ncmrwfx/incois/hycom/ARVIND_SINGH/HYCOM_TS/GFS/'
files = [filename for filename in glob.glob(os.path.join(path,'gfs*.nc'))]
Sort_files = sorted(files)

# Read the source file
nf = nc('/incois_ncmrwfx/incois/hycom/ARVIND_SINGH/HYCOM_TS/GFS/2014/gfs0001.nc')
S_nf=nc(Sort_files[0])
df = nc(path_write+'Merge_time_2015T.nc','w')
#create dimensions
L_Dimensions = list(S_nf.dimensions.keys())# store names of dimensions in a list
# Time is unlimited dimension, so create TIME dimension separately
L_Dimensions.remove('time')
df.createDimension('time',None)
for var in L_Dimensions:
    df.createDimension(var,len(S_nf.dimensions[var]))
#create variables
# store names of variables in a list
Variable_Names = [var for var in S_nf.variables.keys()]
for Name in Variable_Names:
#    if(len(nf.variables[var].dimensions)==1):
      df.createVariable(Name,nf.variables[Name].dtype.name,nf.variables[Name].dimensions)
 #   else : 
  #    temp = list(nf.variables[Name].dimensions)
   #   temp.insert(0,'time')
    #  Tem = tuple(temp)
     # df.createVariable(Name,nf.variables[Name].dtype.name,Tem)
#create attributes
# create global attributes
# Loop for assigning attributes from nf to df
for Name in nf.ncattrs():
    df.setncattr(Name, getattr(nf,Name))
#df.variables['time'].units='seconds since 1970-01-01 00:00:00.00:00'
# create attributes of variables
for var in Variable_Names:
    for Name in nf.variables[var].ncattrs():
 #     if(var!='time' or Name!='units'):
          df.variables[var].setncattr(Name,getattr(nf.variables[var],Name))

# Assigning the variables
# Loop for traversing through variables in nc file
# variable assignment
# assigning time variable
for var in Variable_Names:
    if(var=='time'):
      continue
    if(len(S_nf.variables[var].dimensions)==1):
      df.variables[var][:]= S_nf.variables[var][:]

End_nf = nc(Sort_files[len(Sort_files)-1])
Start_date = num2date(S_nf.variables['time'][0],units = nf.variables['time'].units)
End_date = num2date(End_nf.variables['time'][0],units=nf.variables['time'].units)
 
NO_days,No_seconds = (End_date-Start_date).days,(End_date-Start_date).seconds
print(Start_date,End_date)
No_hours = NO_days*24 + No_seconds// 3600
print("No_observation=",No_hours)
real_dates= [datetime(Start_date.year,Start_date.month,Start_date.day,Start_date.hour,Start_date.minute,Start_date.second)+n*timedelta(hours=3) for n in range(int(No_hours/3)+1)]
df.variables['time'][:] = date2num(real_dates,units = nf.variables['time'].units)
 #code for checking missing files
T_start = Start_date
Total_file=0

for files in Sort_files:
    file = nc(files)
    for var in Variable_Names:
      try:
        if(len(file.variables[var].dimensions)!=len(nf.variables[var].dimensions)):
            print(files,var,"Dimensions not equal")
      except:
        print(files,var,"Variable name doesn't exist")
    T_end = num2date(file.variables['time'][0],units = nf.variables['time'].units)
    duration = T_end-T_start
    days, seconds = duration.days, duration.seconds
    hours = days * 24 + seconds // 3600
            
    Miss_files=int(hours/3)-1
      # code for filling missing files as masked values
    print(len(real_dates),T_start,T_end,Miss_files)
    #    print(Miss_files)
    if(Miss_files<0):
      continue

    if(Miss_files>0):
       for i in range(Miss_files):
           for Name in Variable_Names:
               print(Name,"Masked","Total_file:",Total_file)
               if(len(nf.variables[Name].dimensions)>1):
                  # for i in range(Miss_files):
                 if(df.variables[Name].dimensions==4):
                   df.variables[Name][Total_file,:,:,:]=ma.masked_where(nf.variables[Name][0,:,:,:]>-280,nf.variables[Name][0,:,:,:],True)
                 if(df.variables[Name].dimensions==3):
                   df.variables[Name][Total_file,:,:]=ma.masked_where(nf.variables[Name][0,:,:]>-280,nf.variables[Name][0,:,:],True)
           Total_file=Total_file+1
    print(Total_file,Variable_Names)
    for Name in Variable_Names:
        print(" time_len ",len(file.variables['time']),files)
        if(len(df.variables[Name].dimensions)>1):
          if(len(df.variables[Name].dimensions)==4):
            df.variables[Name][Total_file,:,:,:]=file.variables[Name][:,:,:]
          if(len(df.variables[Name].dimensions)==3):
            df.variables[Name][Total_file,:,:]=file.variables[Name][:,:]
    Total_file=Total_file+1
    T_start = T_end
    file.close()

    
nf.close()
S_nf.close()
df.close()
