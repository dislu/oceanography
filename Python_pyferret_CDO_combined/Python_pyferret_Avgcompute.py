#%pyferret -python -quiet
#%load_ext ferretmagic
import os
import pyferret
import glob
from  netCDF4 import Dataset as nc

dir='/incois_ncmrwfx/incois/hycom/ARVIND_SINGH/HYCOM_TS/BOX/'
#R_path = ['Season_Dec-Feb/','Season_Jun-Aug/','Season_Mar-May/','Season_Sep-Nov/']
#for r_path in R_path:
for input_f in glob.glob(os.path.join(dir+'2012-16/box','Mgfs*.nc')):
    input_fname = input_f.split('/')
    print(input_fname[len(input_fname)-1])
    f_name = input_fname[len(input_fname)-1].split('_')
       # if(input_fname[len(input_fname)-1][0]=='m'):
       #   l_var = 'mld_avg'
       #   s_var = 'MLD[x=@ave,y=@ave]'
       # else : 
    df=nc(input_f)
    N_vars=list(df.variables.keys()-df.dimensions.keys())
    for var in N_vars:
        l_var = var+'_avg'
        s_var = var+'[x=@ave,y=@ave]'
        fname = f_name[0]+'_'+f_name[1]+'_avg.nc'
        output_f = dir+'2012-16/avg/'+fname
        output = '"'+output_f+'"'
        input = '"'+input_f+'"'
        pyferret.run('use '+input)
        print(l_var,s_var)
        pyferret.run('let '+l_var+'='+s_var)
        print(output)
        pyferret.run('save/file='+output+'/append '+l_var)
        pyferret.run('cancel data '+input)
