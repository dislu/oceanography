from netCDF4 import Dataset as nc
from netCDF4 import num2date
import numpy as np
import time
import os

path = os.getcwd()
File_Name = 'rtofs_201904'+str(File_No)+'_fcast'
# Read the source file
nf = nc(File_Name + '.nc')
os.mkdir(path+'/'+File_Name)
# Store the vector of variable time in a list
time_array = nf.variables['TIME'][:]
# convert time_array into real_datetime() array
Real_DateTime = [] # Empty list for real_datetime array
for var in time_array:
    Real_DateTime.append(num2date(var,units = nf.variables['TIME'].units))# append each converted time_array in Real_DateTime

# Number of Observations Per day
NO_OPD = 1
# Loop for calculating number of observations per day
for k in range(len(Real_DateTime)-1):
    if(Real_DateTime[k].day==Real_DateTime[k+1].day):
        NO_OPD = NO_OPD+1
    else:
        break;
# Total Number of files to write
if (len(Real_DateTime)% NO_OPD==0):
    Total_F_Nos =int( Real_DateTime/NO_OPD) # variable for total number of files to write
else:
    Total_F_Nos = int(Real_DateTime/NO_OPD)+1
for i in range(Total_F_Nos):
    j = NO_OPD*(i+1)
    if (j>len(nf.dimensions['TIME'])):
        j = len(nf.dimensions['TIME'])
    df = nc(File_Name'/'+str(Real_DateTime[Total_F_Nos*i].date())+'.nc',w)
    #create dimensions
    L_Dimensions = list(nf.dimensions.keys())# store names of dimensions in a list
    # Time is unlimited dimension, so create TIME dimension separately
    L_Dimensions.remove('TIME') 
    df.createDimension('TIME',None)
    for var in L_Dimensions:
         df.createDimension(var,len(nf.dimensions[var]))
    #create variables
    # store names of variables in a list
    Variable_Names = [var for var in nf.variables.keys()]
    for Name in Variable_Names:
        df.createVariable(Name,nf.variables[Name].dtype.name,nf.variables[Name].dimensions)
    #create attributes
    # create global attributes
    df.description = 'Daily data' # create a extra attribute for description
    # Loop for assigning attributes from nf to df 
    for Name in nf.ncattrs():
        df.Name = getattr(nf,Name)
    # create attributes of variables
    for var in Variable_Names:
        for Name in nf.variables[var].ncattrs():
            (df.variables[var]).Name = getattr(nf.variables[var],Name)
            
    # Assigning the variables
    # Loop for traversing through variables in nc file
    for Name in Variable_Names:
        Len_Dim = len(nf.variables[Name].dimensions)
        df_List = [0]*Len_Dim # zero list of the length dimensions of the variable for df(written file)
        nf_List = [0]*Len_Dim # zero list of the length dimensions of the variable for nf(reading file)
        L = list(nf.variables[Name].dimensions)# store the dimensions names of the variable in a list
        # loop for traversing through the dimensions of variables
        for var in range(Len_Dim):
            if(L[var]=='TIME'): # range of time dimension will be calculated separatly
                df_List[var] = [i for i in range(NO_OPD)]
                nf_List[var] = [v for v in range(NO_OPD*i,j)]
            else:
                df_List[var]= [i for i in range(len(nf.dimensions[L[var]]))]# Calculation of range of dimensions of the variables
                nf_List[var]= [i for i in range(len(nf.dimensions[L[var]]))]
        Flattened_df_List =[var for var in df_List]# remove extra square braces in the Lists 
        Flattened_nf_List = [var for var in nf_List]
        df.variables[Name][Flattened_df_List]=nf.variables[Name][Flattened_nf_List]
    df.close()
nf.close()
