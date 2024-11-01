import os
import sys
sys.path.insert(0,os.path.dirname(__file__)+'/../LibBase')
sys.path.insert(0,os.path.dirname(__file__)+'/../LibPlot')
import trans as tr


# ymd
year,mon,day,hours,mins,secs = 2023,12,22,0,0,0
print("Day of Year: ",tr.ymd2doy(year,mon,day,hours,mins,secs))
[week,sow]=tr.ymd2gpst(year,mon,day,hours,mins,secs)
print("GPST(Week Sow): ",week)
print("GPST(Day of Week): ",sow/3600/24)