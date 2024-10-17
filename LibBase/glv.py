#!/usr/bin/python
# author: zhShen
# date: 20190520
#coding:utf8
from numpy import *
import math
import trans as tr

div_ref = {'GNSS_INS20190613':[-2267821.37349,5009333.67843,3220980.19527],
'GNSS_INS20190614':[-2280124.80746,5007874.71896,3214600.77599],
'GNSS_INS20150722':[-2262959.73266,5018893.3985,3209551.26355],
'GNSS_INS20190716':[-2280111.74061,5007885.88124,3214597.99589],
'GNSS_INS_VISION20200918':[-2280480.89589,5007887.35894,3214299.75843],
# 'GNSS_INS_VISION20200918':[-2267775.94401,5009357.28343,3220982.00779],
'GNSS_INS_VISION20201029':[-2286200.13501,5003529.13684,3217153.42898],
'beijing':[-2155275.70303,4374333.06884,4097406.78347],
'GNSS_INS20201216':[-2267761.0457,5009370.8942,3220970.5820]
}

plus_ref = {'GNSS_INS20190613':[-2267825.4414,5009338.2921,3220976.3247],
'GNSS_INS20190614':[-2280126.2433,5007876.9185,3214601.3681],
'GNSS_INS20150722':[-2262959.8563,5018893.5896,3209551.4511],
'GNSS_INS20190716':[ -2280111.5451,5007885.8405,3214598.6301],
'GNSS_INS_VISION20200918':[-2280475.9564,5007885.4941,3214296.9763],
# 'GNSS_INS_VISION20200918':[-2267776.6684,5009357.0310,3220981.7156],
'GNSS_INS_VISION20201029':[-2286267.8496,5003460.8873,3217166.0495],
'GNSS_INS20190716':[-2280111.74061,5007885.88124,3214597.99589],
'beijing':[-2155274.8376,4374329.1363,4097402.8155],
'GNSS_INS20201216':[-2267761.1086,5009370.8950,3220970.6208]
}

a = 6378137;   # the Earth's semi-major axis
f  = 1/298.257;# flattening
wie = 7.2921151467e-5; 
b = (1- f)* a;  # semi-minor axis
e = sqrt(2* f- f**2);  
e2 =  e**2; # 1st eccentricity
ep = sqrt( a**2- b**2)/ b; 
ep2 =  ep**2; # 2nd eccentricity
wie = wie;  # the Earth's angular rate
g0 = 9.7803267714;  # gravitational force
mg = 1.0e-3* g0; # milli g
ug = 1.0e-6* g0; # micro g
mGal = 1.0e-3*0.01; # milli Gal = 1cm/s**2 ~= 1.0E-6*g0
ugpg2 =  ug/ g0**2;# ug/g**2
ppm = 1.0e-6;   # parts per million
deg = pi/180;   # arcdeg
min =  deg/60;   # arcmin
sec =  min/60;   # arcsec
hur = 3600; # time hour (1hur=3600second)
dps = pi/180/1; # arcdeg / second
dph =  deg/ hur;  # arcdeg / hour
dpss =  deg/sqrt(1); # arcdeg / sqrt(second)
dpsh =  deg/sqrt( hur);  # arcdeg / sqrt(hour)
dphpsh =  dph/sqrt( hur); # (arcdeg/hour) / sqrt(hour)
Hz = 1/1;   # Hertz
dphpsHz =  dph/ Hz;   # (arcdeg/hour) / sqrt(Hz)
ugpsHz =  ug/sqrt( Hz);  # ug / sqrt(Hz)
ugpsh =  ug/sqrt( hur); # ug / sqrt(hour)
mpsh = 1/sqrt( hur); # m / sqrt(hour)
mpspsh = 1/1/sqrt( hur); # (m/s) / sqrt(hour), 1*mpspsh~=1700*ugpsHz
ppmpsh =  ppm/sqrt( hur); # ppm / sqrt(hour)

#=== FONT SET ===#
font_title = {'family' : 'Arial', 'weight' : 300, 'size' : 20}
font_label = {'family' : 'Arial', 'weight' : 300, 'size' : 20}
font_tick = {'family' : 'Arial', 'weight' : 300, 'size' : 35}
font_legend = {'family' : 'Arial', 'weight' : 300, 'size' : 20}
# font_legend = {'family' : 'Times New Roman', 'weight' : 600, 'size' : 15}
font_text = {'family' : 'Arial','weight' : 300,'size'   : 20}
xtick_size = 20
color_list = ["#0099E5","#34BF49","#FF4C4C"]

def xtick_min(time,year,mon,day,starttime,LastT,deltaT):
    if "+" in time:
        end_time = len(time)
        delta_Time = int(time[4:end_time]) + starttime
        begT = int(time[4:end_time]) + starttime
    else:
        delta_Time = starttime
        begT=starttime
    #for time in data[mode[0]].keys():
    secow_start = tr.ymd2gpst(year,mon,day,0,00,00)
    doy = tr.ymd2doy(year,mon,day,0,00,00)
    cov_Time = secow_start[1] - 0 * 3600
    if "+" in time:
        value = time.split("+")
        cov_Time = secow_start[1] - int(value[1]) * 3600
    end_Time = begT + LastT
    delta_X = math.ceil((LastT)/deltaT)
    XLabel = []
    XTick = []
    starttime = begT - deltaT

    # for i in range(delta_X):
    #     starttime = starttime + deltaT
    #     cur_Str_X = '%02d' % (starttime % 24) + ":{:0>2}".format(int((starttime-int(starttime))*60))
    #     XLabel.append(cur_Str_X)
    #     XTick.append((starttime))       
    
    while starttime < end_Time:
        starttime = starttime + deltaT
        if (starttime >= end_Time):
            cur_Str_X = '%02d' % (end_Time % 24) + ":{:0>2}".format(round((end_Time-int(end_Time))*60))
            # cur_Str_X = '%d' % (end_Time % 24)
            XLabel.append(cur_Str_X)
            XTick.append((end_Time))
            break
        cur_Str_X = '%02d' % (starttime % 24) + ":{:0>2}".format(round((starttime-int(starttime))*60))
        # cur_Str_X = '%d' % (starttime % 24)
        XLabel.append(cur_Str_X)
        XTick.append((starttime))
    
    return (XLabel,XTick,cov_Time,begT,LastT)

def xtick(time,year,mon,day,starttime,LastT,deltaT):
    if "+" in time:
        end_time = len(time)
        delta_Time = int(time[4:end_time]) + starttime
        begT = int(time[4:end_time]) + starttime
    else:
        delta_Time = starttime
        begT=starttime
    #for time in data[mode[0]].keys():
    secow_start = tr.ymd2gpst(year,mon,day,0,00,00)
    doy = tr.ymd2doy(year,mon,day,0,00,00)
    cov_Time = secow_start[1] - 0 * 3600
    if "+" in time:
        cov_Time = secow_start[1] - int(time[3:end_time]) * 3600
    end_Time = begT + LastT
    delta_X = math.ceil((LastT)/deltaT)
    XLabel = []
    XTick = []
    starttime = begT - deltaT

    # for i in range(delta_X):
    #     starttime = starttime + deltaT
    #     cur_Str_X = '%02d' % (starttime % 24) + ":{:0>2}".format(int((starttime-int(starttime))*60))
    #     XLabel.append(cur_Str_X)
    #     XTick.append((starttime))       
    
    while starttime < end_Time:
        starttime = starttime + deltaT
        if (starttime >= end_Time):
            # cur_Str_X = '%02d' % (end_Time % 24) + ":{:0>2}".format(round((end_Time-int(end_Time))*60))
            cur_Str_X = '%d' % (end_Time % 24)
            XLabel.append(cur_Str_X)
            XTick.append((end_Time))
            break
        # cur_Str_X = '%02d' % (starttime % 24) + ":{:0>2}".format(round((starttime-int(starttime))*60))
        cur_Str_X = '%d' % (starttime % 24)
        XLabel.append(cur_Str_X)
        XTick.append((starttime))
    
    return (XLabel,XTick,cov_Time,begT,LastT)