library(ncdf4)
library(chron)
library(zoo)
library(WaveletComp)
library(splus2R)
library(xts)
library(TTR)
library(quantmod)
library(cluster)

R_path<-"C:\Users\INCOIS\OneDrive\Documents\arvindt\Incois_nc"
ncname1<-"gfs_AS_avg"
ncname2<-"mld_AS_avg"
ncfname1<- paste(R_path, ncname1, ".nc", sep="")
ncfname2<- paste(R_path, ncname2, ".nc", sep="")
df1<-nc_open(ncfname1)
df2<-nc_open(ncfname2)
d1_time<-ncvar_get(df1,"TIME")
tunits1 <- ncatt_get(df1,"TIME","units")
df1_gfsv<-ncvar_get(df1,"VGRD_10MABOVEGROUND_AVG")
df1_gfsu<-ncvar_get(df1,"UGRD_10MABOVEGROUND_AVG")
Wind_speed_Sq<-(df1_gfsu)^2+(df1_gfsv)^2
df2_mld<-ncvar_get(df2,"MLD_AVG")
dates<-seq.dates("01/01/2012",by="days",length. = 1826)
T1<-cbind(dates,Wind_speed_Sq)
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
ts_Wind<-ts(Wind_speed_Sq)
ts_MLD<-ts(df2_mld)
plot(ts_Wind,type="l",col="red",xaxt="n",main="Wind_Speed_Sq and MLD",
     xlab="Time in weeks",ylab="")
lines(ts_MLD,col="green")
axis(side=1,at = seq(0,1826,365),labels = c(seq(2012, 2017, 1)))
legend("topright",legen=c("Wind_speed_sq","MLD"),col=c("red","green"),lty=1,cex = 0.5)
my.data<-data.frame(x=X,y=Y)
my.wc <- analyze.coherency(my.data, my.pair = c(1,2),loess.span = 0,dt = 1,
                           dj = 1/100,
                           window.type.t = 1, window.type.s = 1,
                           window.size.t = 5, window.size.s = 1,
                           make.pval = TRUE, n.sim = 10)

Lag_M<-matrix(0,545,261)
for (i in 1:545)
{
  for ( j in 1:261)
  {
    Lag_M[i,j]=(my.wc$sAngle[i,j])*(my.wc$Period[i])/(2*pi)
  }
}
clus1=matrix(0,261,1)
clus2=matrix(0,261,1)

flag=0
count=0
count1=0
count2=0
for (i in 1:545)
{
  if(my.wc$Coherence.avg.pval[i]>0.95)
   {
     flag=1
   
  } else {
    count=count+flag
    flag=0
  }
  print("flag=")
  print(count) 
  if(my.wc$Coherence.avg.pval[i]>0.95 && count==1)
  {
    clus1<-clus1+Lag_M[i,]
    print(i)
    count1=count1+1
  }
  
  if(my.wc$Coherence.avg.pval[i]>0.95 && count==2)
  {
    clus2<-clus2+Lag_M[i,]
    print(i)
    count2=count2+1
  }
}
Mean_clus1<-clus1/count1
Mean_clus2<-clus2/count2
PEAK <- findPeaks(my.wc$Coherence.avg,thresh=0)
Lar_clus1<-pam(Lag_M[PEAK[length(PEAK)],],1)
Lar_clus2<-pam(Lag_M[PEAK[length(PEAK)-1],],1)

par(fig=c(0,0.7,0.5,1))
par(oma=c(1, 2, 1, 0), mar=c(1, 1, 1, 1) + 0.1)    
wc.image(my.wc, n.levels = 250,
         siglvl.contour = 0.1, siglvl.arrow = 0.06, ## default values
         legend.params = list(width=1.2, shrink = 0.9, mar =1, 
                              n.ticks = 6, 
                              label.digits = 1, label.format = "f", 
                              lab = "Cross wavelet power levels", lab.line = 0.15),
         spec.time.axis = list(at = seq(my.wc$axis.1[1],my.wc$axis.1[n],52),
                               labels = c(seq(2012, 2017, 1)),las = 1,
                               hadj = NA, padj = NA),
         timelab = paste("wind_Sq lead MLD by 1:",
           toString(round(Lar_clus1$medoids[1,1],digits = 1)),
           "2:",toString(round(Lar_clus1$medoids[1,1],digits = 1)),sep=""),
           lwd = 2,lwd.axis = 1)
#abline(h=c(my.wc$Period[length(PEAK)],my.wc$Period[length(PEAK)-1]),col=c("blue","green"))
par(fig=c(0,0.7,0,0.5),new=T)
par(oma=c(1, 2, 1, 0), mar=c(1, 1, 1, 1) + 0.1)
wc.image(my.wc, which.image = "wc", color.key = "interval", n.levels = 250,
         siglvl.contour = 0.1, siglvl.arrow = 0.05,
         legend.params = list(width=1.2, shrink = 0.9, mar =1, 
                              n.ticks = 6, 
                              label.digits = 1, label.format = "f", 
                              lab = "Wavelet coherence levels", lab.line = 0.15),
         spec.time.axis = list(at = seq(my.wc$axis.1[1],my.wc$axis.1[n],52),
                               labels = c(seq(2012, 2017, 1)),las = 1,
                               hadj = NA, padj = NA),
         timelab = "")
par(fig=c(0.75,1,0.5,1),new=T)
par(oma=c(2, 2, 2, 0), mar=c(2, 2, 1, 1) + 0.1)
wc.avg(my.wc, siglvl = 0.05, sigcol = "blue", sigpch = 20,show.legend = F,
       periodlab = "")
legend("bottomright",legend = 0.05,cex=0.4,pt.cex = 4,col=1)
#abline(v=seq(0.05,0.95,0.05),h=2^seq(1,9,1),lty=2)
grid(nx = NULL, ny = NULL, col = "lightgray", lty = "dotted",
     lwd = par("lwd"), equilogs = TRUE)
par(fig=c(0.75,1,0,0.5),new=T)
par(oma=c(2, 2, 2, 0), mar=c(1, 2, 2, 1) + 0.1)
wc.avg(my.wc,which.avg = "wc",siglvl = 0.05, sigcol = "blue", sigpch = 20,show.legend = F,
       spec.avg.axis = list(at = seq(0.1,1,0.1), labels = c(seq(0.1,1,0.1)), 
                            las = 1, hadj = NA, padj = NA),
       periodlab = "")
legend("bottomright",legend = 0.05,cex=0.4,pt.cex = 4,col=1)
#abline(v=seq(0.05,0.95,0.05),h=2^seq(1,9,1),lty=2)
grid(nx = NULL, ny = NULL, col = "lightgray", lty = "dotted",
     lwd = par("lwd"), equilogs = TRUE)
#univariate power spectrum
wt.image(my.wc, my.series=2,
         spec.time.axis = list(at = seq(my.wc$axis.1[1],my.wc$axis.1[261],52),
                               labels = c(seq(2012, 2017, 1)),las = 1,
                               hadj = NA, padj = NA),
         timelab = "", main = "Short-wave Wavelet power spectrum")
#global phasedifference
wc.phasediff.image(my.wc, which.contour = "wc", use.sAngle = TRUE,
                   n.levels = 250, siglvl = 0.1,
                   legend.params = list(lab = "phase difference levels",
                                        lab.line = 3),
                   timelab = "")

