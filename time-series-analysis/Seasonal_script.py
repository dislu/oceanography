import os
import glob
#from Seasonal_WTCorr_e import WTLC_plot
from WTCorr_e import WTLC_plot
from Pdf_reg import PDF
import matplotlib.pyplot as plt
#from Seasonal_WTLC_Corr import SWTLC_Corr
dir='/incois_ncmrwfx/incois/hycom/ARVIND_SINGH/HYCOM_TS/BOX/'
Dir1 = '/incois_ncmrwfx/incois/hycom/ARVIND_SINGH/HYCOM_TS/IMG/'
R_path = ['Season_Dec-Feb/','Season_Jun-Aug/','Season_Mar-May/','Season_Sep-Nov/']
R_file = ['AS','AS2','BOB','IO','IOy']
for r_path in R_path:
  fig, axs = plt.subplots(nrows=2,ncols=3)
  x=0
  y=0
  for r_file in R_file:
      file_x = dir+r_path+'avg/'+'gfs_'+r_file+'_avg.nc'
      file_y = dir+r_path+'avg/'+'mld_'+r_file+'_avg.nc'
     # WTLC_plot(file_x,file_y)
      Sns=PDF(file_x,file_y,x,y,axs)
      y=y+1
      if(y>2):
        y=0
        x=x+1
  Sns.savefig(Dir1+r_path+r_path[:-1]+'_Pdf.png')
