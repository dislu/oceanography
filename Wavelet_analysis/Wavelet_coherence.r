library(biwavelet)
library(ncdf4)
library(chron)
library(zoo)
R_path<-"/home/dislu/Incois_nc/"
ncname1<-"gfs_BOB_avg"
ncname2<-"mld_BOB_avg"
ncfname1<- paste(R_path, ncname1, ".nc", sep="")
ncfname2<- paste(R_path, ncname2, ".nc", sep="")
df1<-nc_open(ncfname1)
df2<-nc_open(ncfname2)
d1_time<-ncvar_get(df1,"TIME")
tunits1 <- ncatt_get(df1,"TIME","units")
df1_gfs<-ncvar_get(df1,"DSWRF_AVG")
df2_mld<-ncvar_get(df2,"MLD_AVG")
dates<-seq.dates("01/01/2012",by="days",length. = 1826)
T1<-cbind(dates,df1_gfs)
T2<-cbind(dates,df2_mld)
T1[,2]<-na.approx(T1[,2],rule=2)
T2[,2]<-na.approx(T2[,2],rule=2)
T1[,2]<-scale(T1[,2])
T2[,2]<-scale(T2[,2])
# Continuous wavelet transform
wt.T1=wt(T2)
# Plot power
# Make room to the right for the color bar
par(oma=c(0, 0, 0, 1), mar=c(5, 4, 4, 5) + 0.1)
plot(wt.T1, plot.cb=TRUE, plot.phase=FALSE)
# Cross-wavelet
xwt.T1T2=xwt(T1, T2)
# Plot cross wavelet power and phase difference (arrows)
plot(xwt.T1T2, plot.cb=TRUE)
# Wavelet coherence; nrands should be large (>= 1000)
dt=1
wtc.T1T2<-wtc (T1, T2, pad = TRUE, dj = 1/12, s0 = 2 * dt, J1 = NULL, 
     max.scale = NULL, mother = c("morlet", "paul", "dog"), param = -1, 
     lag1 = NULL, sig.level = 0.95, sig.test = 0, nrands = 300, quiet = FALSE)
# Plot wavelet coherence and phase difference (arrows)
# Make room to the right for the color bar
par(mfrow=c(2,1),oma = c(2, 1, 1, 9.25), mar = c(2, 1, 1, 8.25) + 0.1)
#par(oma=c(0, 0, 2, 0), mar=c(5, 4, 4, 5) + 0.1)
plot(wtc.T1T2, plot.cb=TRUE,main="Power",plot.phase = TRUE)
# Plotting a graph

plot(wtc.T1T2,plot.phase = TRUE,lty.coi = 1, col.coi = "grey", lwd.coi = 2, 
     lwd.sig = 2, arrow.lwd = 0.01, arrow.len = 0.05, ylab = "period", xlab = "time", 
     plot.cb = TRUE, main = "Wavelet Coherence: MLD vs DSWF")

# Adding grid lines
n = length(T1[, 1])
abline(v = seq(wtc.T1T2$t[1],wtc.T1T2$t[n],365),h=c(4,16,64,256),col = "black", lty = 1, lwd = 1)

# Defining x labels
axis(side = 3, at = seq(wtc.T1T2$t[1],wtc.T1T2$t[n],365), labels = c(seq(2012, 2017, 1)))

