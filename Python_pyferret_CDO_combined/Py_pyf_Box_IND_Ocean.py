from cdo import *
import glob
from  netCDF4 import Dataset as nc
import os 

cdo = Cdo()

input_f = '/incois_ncmrwfx/incois/hycom/ARVIND_SINGH/HYCOM_TS/GFS/Merge_time_d_12-16.nc'
#for input_f in glob.glob(os.path.join(input_p,'*_e.nc')):
     # input_f = '/incois_ncmrwfx/incois/hycom/ARVIND_SINGH/HYCOM_TS/mld_Final.nc'
     #dir = str(i+1)+'_RAMA_FD'
     #parent_dir = '/incois_ncmrwfx/incois/hycom/ARVIND_SINGH'
     #path = os.path.join(parent_dir,dir)
file_t = ['mld*.nc','gfs*.nc']
   #    input_fname = input_f.split('/')
   #  if(input_fname[len(input_fname)-1][0]=='D'):
f=file_t[1]
lon='longitude'
lat='latitude'
   #  else: 
   #     f = file_t[0]
   #     lon ='LONGITUDE'
   #     lat = 'LATITUDE'
     
   #  path_Name = ['Season_Dec-Feb/box/','Season_Jun-Aug/box/','Season_Mar-May/box/','Season_Sep-Nov/box/']
   #  season_f = input_fname[len(input_fname)-1].split('_')[1][0]
   #  if(season_f=='D'):
   #    p_Name = path_Name[0]
   #  if(season_f=='J'):
   #    p_Name = path_Name[1]
   #  if(season_f=='M'):
   #    p_Name = path_Name[2]
   #  if(season_f=='S'):
   #    p_Name = path_Name[3]
     
S_path = '/incois_ncmrwfx/incois/hycom/ARVIND_SINGH/HYCOM_TS/BOX/2012-16/box/'#+p_Name
R_path = '/incois_ncmrwfx/incois/hycom/ARVIND_SINGH/HYCOM_TS/BOX/2012-16/box'
          
for filename in glob.glob(os.path.join(R_path,f)):
    file = filename.split('/')
    fname = file[len(file)-1]
    print(fname)
    df = nc(filename)
        # print(df)
        
    l_lon=len(df.variables[lon])
    l_lat=len(df.variables[lat])
    Lon_i=df.variables[lon][:].data[0]
    Lat_i=df.variables[lat][:].data[0]
    Lon_f=df.variables[lon][:].data[l_lon-1]
    Lat_f=df.variables[lat][:].data[l_lat-1]
    cdo.sellonlatbox(str(Lon_i)+","+str(Lon_f)+","+str(Lat_i)+","+str(Lat_f),input=input_f,output=S_path+'M'+fname) 
