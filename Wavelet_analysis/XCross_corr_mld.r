library(ncdf4)
library(chron)
library(zoo)
library(WaveletComp)
library(splus2R)
library(xts)
library(TTR)
library(quantmod)
library(cluster)

R_path<-"/Users/arvind tomar/OneDrive/Documents/Incois_nc/incois/"
ncname1<-"gfs_L-10_avg"
ncname2<-"mld_L-10_avg"
ncfname1<- paste(R_path, ncname1, ".nc", sep="")
ncfname2<- paste(R_path, ncname2, ".nc", sep="")
df1<-nc_open(ncfname1)
df2<-nc_open(ncfname2)
#d1_time<-ncvar_get(df1,"TAX")
#tunits1 <- ncatt_get(df1,"TAX","units")
df1_gfs_DSWRF<-ncvar_get(df1,"DSWRF_SURFACE_AVG")
df1_gfsv<-ncvar_get(df1,"VGRD_10MABOVEGROUND_AVG")
df1_gfsu<-ncvar_get(df1,"UGRD_10MABOVEGROUND_AVG")
Wind_speed_Sq<-(df1_gfsu)^2+(df1_gfsv)^2
df2_mld<-ncvar_get(df2,"MLD_AVG")
dates<-seq.dates("01/01/2012",by="days",length. = 1826)
T1<-cbind(dates,df1_gfs_DSWRF)
T2<-cbind(dates,df2_mld)
T1[,2]<-na.approx(T1[,2],rule=2)
T2[,2]<-na.approx(T2[,2],rule=2)
T1[,2]<-scale(T1[,2])
T2[,2]<-scale(T2[,2])
XX=T1[,2]
YY=T2[,2]
X=c()
Y=c()
weekly_seq=seq(1,length(XX),by=7)
for ( i in weekly_seq )
{
  X=append(X,mean(XX[i:(i+1)]))
  Y=append(Y,mean(YY[i:(i+1)]))
}
X[length(X)]=mean(XX[weekly_seq[length(weekly_seq)]:length(XX)])
Y[length(Y)]=mean(YY[weekly_seq[length(weekly_seq)]:length(YY)])
n = length(X)
#plot two time series
ts_DSWRF<-X
ts_MLD<-Y
plot(ts_MLD,type="l",col="red",xaxt="n",main="Wind_Speed_Sq and MLD",
     xlab="Time in weeks",ylab="")
lines(ts_DSWRF,col="green")
axis(side=1,at = seq(0,1826,365),labels = c(seq(2012, 2017, 1)))
legend("topright",legen=c("Wind_speed_sq","MLD"),col=c("red","green"),lty=1,cex = 0.5)
#cross correlation 

ccf_mld_DSWF<-ccf(ts_DSWRF,ts_MLD,lag.max = 40,ylab="CCF",main="DSWRF vs MLD")
max_index<-which(ccf_mld_DSWF$acf==max(ccf_mld_DSWF$acf))
min_index<-which(ccf_mld_DSWF$acf==min(ccf_mld_DSWF$acf))
Max<-format(round(ccf_mld_DSWF$acf[max_index], 2), nsmall = 2)
Min<-format(round(ccf_mld_DSWF$acf[min_index], 2), nsmall = 2)
lab_Max<-paste("R=", Max, sep="")
lab_Min<-paste("R=",Min, sep="")
points(ccf_mld_DSWF$lag[max_index],ccf_mld_DSWF$acf[max_index],col="red")
points(ccf_mld_DSWF$lag[min_index],ccf_mld_DSWF$acf[min_index],col="red")
text(ccf_mld_DSWF$lag[max_index],ccf_mld_DSWF$acf[max_index],labels =lab_Max,pos=2,font = 2)
text(ccf_mld_DSWF$lag[min_index],ccf_mld_DSWF$acf[min_index],labels = lab_Min,pos=4,font = 2)
abline(v=0,col="red",lty=2)

my.data<-data.frame(x=X,y=Y)
