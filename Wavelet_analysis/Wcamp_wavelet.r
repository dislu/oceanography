library(ncdf4)
library(chron)
library(zoo)
library(WaveletComp)
library(dplR)
R_path<-"C:\Users\INCOIS\OneDrive\Documents\arvindt\Incois_nc"
ncname1<-"gfs_IOy_avg"
ncname2<-"mld_IOy_avg"
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
#df1_Preci_R<-ncvar_get(df1,"PRATE_SURFACE_AVG")
#df1_DSWFR<-ncvar_get(df1,"DLWRF_SURFACE_AVG")
dates<-seq.dates("01/01/2012",by="days",length. = 1826)
T1<-cbind(dates,Wind_speed_Sq)
T2<-cbind(dates,df2_mld)
T1[,2]<-na.approx(T1[,2],rule=2)
T2[,2]<-na.approx(T2[,2],rule=2)
T1[,2]<-scale(T1[,2])
T2[,2]<-scale(T2[,2])

#filter band pass
DSWRF_pass<-pass.filt(T1[,2],W=c(180,208),type="pass")
MLD_pass<-pass.filt(T2[,2],W=c(180,208),type = "pass")
ts_DSWRF_pass<-ts(DSWRF_pass)
ts_MLD_pass<-ts(MLD_pass)
plot(ts_DSWRF_pass,type="l",col="red",xaxt="n",main="wind_speed_square and MLD 180-208 days filtered band",
     xlab="Time in days",ylab="")
lines(ts_MLD_pass,col="green")
axis(side=1,at = seq(0,1826,365),labels = c(seq(2012, 2017, 1)))
legend("topright",legen=c("wind_speed_square","MLD"),col=c("red","green"),lty=1,cex = 0.5)
ccf_mld_DSWF<-ccf(ts_DSWRF_pass,ts_MLD_pass,lag.max = 40,ylab="CCF",main="Wind_speed_S vs MLD")
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
n = length(T1[, 1])
my.data<-data.frame(x=T1,y=T2)
#Wavelet coherence
my.wc <- analyze.coherency(my.data, my.pair = c(2,4),loess.span = 0,dt = 1,
                           dj = 1/100,
                           window.type.t = 1, window.type.s = 1,
                           window.size.t = 5, window.size.s = 1,
                           make.pval = TRUE, n.sim = 10)
#figure size and location
par(fig=c(0,0.7,0.5,1))
par(oma=c(1, 2, 1, 0), mar=c(1, 1, 1, 1) + 0.1)
#wavelet power average at 95% significance level
wc.image(my.wc, n.levels = 250,
         siglvl.contour = 0.1, siglvl.arrow = 0.06, ## default values
         legend.params = list(width=1.2, shrink = 0.9, mar =1, 
                              n.ticks = 6, 
                              label.digits = 1, label.format = "f", 
                              lab = "Cross wavelet power levels", lab.line = 0.15),
         spec.time.axis = list(at = seq(my.wc$axis.1[1],my.wc$axis.1[n],365),
                               labels = c(seq(2012, 2017, 1)),las = 1,
                                          hadj = NA, padj = NA),
         timelab = "",lwd = 2,lwd.axis = 1)
#figure size and location
par(fig=c(0,0.7,0,0.5),new=T)
par(oma=c(1, 2, 1, 0), mar=c(1, 1, 1, 1) + 0.1)
wc.image(my.wc, which.image = "wc", color.key = "interval", n.levels = 250,
         siglvl.contour = 0.1, siglvl.arrow = 0.05,
         legend.params = list(width=1.2, shrink = 0.9, mar =1, 
                              n.ticks = 6, 
                              label.digits = 1, label.format = "f", 
                              lab = "Wavelet coherence levels", lab.line = 0.15),
         spec.time.axis = list(at = seq(my.wc$axis.1[1],my.wc$axis.1[n],365),
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
