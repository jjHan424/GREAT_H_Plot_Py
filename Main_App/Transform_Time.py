from math import pi
import os
import sys
sys.path.insert(0,os.path.dirname(__file__)+'/../LibBase')
sys.path.insert(0,os.path.dirname(__file__)+'/../LibPlot')
import trans as tr
import numpy as np
import math


# ymd
year,mon,day,hours,mins,secs = 2024,10,18,0,0,0
print("Day of Year: ",tr.ymd2doy(year,mon,day,hours,mins,secs))
# [week,sow]=tr.ymd2gpst(year,mon,day,hours,mins,secs)
# print("GPST(Week Sow): ",week)
# print("GPST(Second of Week): ",sow)
# print("GPST(Day of Week): ",sow/3600/24)
print("MJD: ", format(tr.ymd2mjd(year,mon,day)))
# Doy2Ymd
# [y,m,d] = tr.doy2ymd(2021,344)
# print("{}-{}-{}".format(y,m,d))

#MJD
# mjd = 60298
# [week,sow] = tr.mjd2gpst(mjd)
# print("GPST(Week Sow): ",week)
# print("GPST(Day of Week): ",sow/3600/24)
# [Year,Mon,Day] = tr.mjd2ymd(mjd)
# Mjd = tr.ymd2mjd(Year,Mon,Day)
# [week,sow]=tr.ymd2gpst(Year,Mon,Day,hours,mins,secs)
# print("GPST(Week Sow): ",week)
# print("GPST(Day of Week): ",sow/3600/24)

#xyz
# [B,L,H] = tr.xyz2blh(4.02788e+06,306998,4.9195e+06)
# print(B*180/pi)
# print(L*180/pi)

ENSG = np.array([4201576.3238,189861.1118,4779065.2530])
MLVL = np.array([4201577.2080,189859.8580,4779064.5580])
delta = (ENSG - MLVL)
print(math.sqrt(delta[0]*delta[0]+delta[1]*delta[1]+delta[2]*delta[2]))
