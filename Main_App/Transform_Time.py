from math import pi
import os
import sys
sys.path.insert(0,os.path.dirname(__file__)+'/../LibBase')
sys.path.insert(0,os.path.dirname(__file__)+'/../LibPlot')
import trans as tr


# ymd
year,mon,day,hours,mins,secs = 2018,12,22,0,0,0
print("Day of Year: ",tr.ymd2doy(year,mon,day,hours,mins,secs))
[week,sow]=tr.ymd2gpst(year,mon,day,hours,mins,secs)
print("GPST(Week Sow): ",week)
print("GPST(Day of Week): ",sow/3600/24)

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
[B,L,H] = tr.xyz2blh(-2414267.6526,5386768.7552,2407459.7917)
print(B*180/pi)
print(L*180/pi)
