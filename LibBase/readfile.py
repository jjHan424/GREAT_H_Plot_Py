'''
Author: JunjieHan
Date: 2021-09-06 19:24:38
LastEditTime: 2022-09-01 22:28:11
Description: read data file
'''
import numpy as np
import math
import glv
import trans as tr
import os

def open_aug_file(filename,sys="G"):
    week,sow=[[] for i in range(60)],[[] for i in range(60)]
    P1,P2,L1,L2 = [[] for i in range(60)],[[] for i in range(60)],[[] for i in range(60)],[[] for i in range(60)]
    ion1,ion2,trp = [[] for i in range(60)],[[] for i in range(60)],[[] for i in range(60)]
    ref = []
    ref_w,ref_sow = [],[]
    epoch_flag = False
    line_num = 0
    min_sow = 0
    with open(filename,'rt') as f:
        for line in f:
            if line[0] == ">":
                value=line.split()
                year=(float(value[1]))
                month=(float(value[2]))
                day=(float(value[3]))
                hour=(float(value[4]))
                minute=(float(value[5]))
                second=(float(value[6]))
                [w,soweek] = tr.ymd2gpst(year,month,day,hour,minute,second)
                if (not epoch_flag):
                    min_sow = soweek
                if (soweek < min_sow):
                    soweek = soweek + 604800
                epoch_flag = True
                ref_w.append(w)
                ref_sow.append(soweek)
            if epoch_flag:             
                if line[0] == sys:
                    value=line.split()
                    if len(value) <= 5:
                        continue
                    prn = int(value[0][1:3])
                    week[prn-1].append(w)
                    sow[prn-1].append(soweek)
                    P1[prn-1].append(float(value[1]))
                    L1[prn-1].append(float(value[2]))
                    P2[prn-1].append(float(value[3]))
                    L2[prn-1].append(float(value[4]))
                    line_num = len(value)
                    if len(value) > 5:
                        ion1[prn-1].append(float(value[5]))
                        ion2[prn-1].append(float(value[6]))
                        #trp[prn-1].append(float(value[7]))
                else:
                    prn=0
                    continue
    if (line_num > 5):
        aug = np.array([P1,P2,L1,L2,ion1,ion2]).T
    else:
        aug = np.array([P1,P2,L1,L2]).T   
    S_time = np.array([week,sow]).T
    all_time = np.array([ref_w,ref_sow]).T
    return (S_time,aug,all_time)

def open_aug_file_new(filename,time_delay = 0):
    all_data={}
    head_info={}
    soweek_last = 0
    w_last = 0
    head_end = False
    epoch_flag = False
    num_sat = 0
    last_day = 0
    day=0
    file_exist = os.path.exists(filename)
    if (not file_exist):
        return all_data
    with open(filename,'rt') as f:
        for line in f:
            value = line.split()
            if "SYS / # / AUG TYPES" in line:
                head_end = True
                head_index = 1
                for cur_value in value:
                    if (cur_value == "SYS"):
                        break
                    if (len(cur_value) != 1):
                        if line[0] not in head_info.keys():
                            head_info[line[0]]={}
                        if line[0] == "C" and cur_value == "RION2":
                            cur_value = "RION1"
                        if line[0] == "C" and cur_value == "dION2":
                            cur_value = "dION1"
                        if line[0] == "C" and cur_value == "ION2":
                            cur_value = "ION1"
                        head_info[line[0]][cur_value] = head_index
                        head_index = head_index + 1                   
            if ">" in line:
                value=line.split()
                year=(float(value[1]))
                month=(float(value[2]))
                day=(float(value[3]))
                hour=(float(value[4]))
                minute=(float(value[5]))
                second=(float(value[6]))
                # if hour == 15:
                #     print("HJJ")
                [w,soweek] = tr.ymd2gpst(year,month,day,hour,minute,second)
                if (not epoch_flag):
                    min_sow = soweek
                if (soweek < min_sow):
                    soweek = soweek + 604800
                epoch_flag = True
                soweek = soweek + time_delay
                if soweek not in all_data.keys():
                    all_data[soweek]={}
            if ((value[0][0] == "C" or value[0][0] == "E" or value[0][0] == "G") and epoch_flag):
                if (len(line) <= 4):
                    continue
                sat = value[0]
                if (sat not in all_data[soweek].keys()):
                    all_data[soweek][sat] = {}
                if (sat[0] not in all_data[soweek].keys()):
                    all_data[soweek][sat[0]] = {}
                i = 1
                for type in head_info[sat[0]].keys():
                    if 12*i-9 > len(line) - 1 or 12*i+3 > len(line) - 1:
                        break
                    # cur_value = line[12*i-9:12*i+3].strip()
                    cur_value = line[12*i-8:12*i+4].strip()
                    # if float(cur_value) == 0.0:
                    #     continue
                    if type == "RTRP":
                        if (len(cur_value) >= 1):
                            all_data[soweek][sat[0]][type] = float(cur_value)
                    else:
                        if (len(cur_value) >= 1):
                            all_data[soweek][sat][type] = float(cur_value)
                    i = i+1


    return (head_info,all_data)



def open_ipp_file(filename,Nsat = 0,hour_in = 24):
    all_data={}
    soweek_last = 0
    w_last = 0
    head_end = False
    epoch_flag = True
    num_sat = 0
    last_day = 0
    day=0
    
    file_exist = os.path.exists(filename)
    if (not file_exist):
        return all_data
    with open(filename,'rt') as f:
        for line in f:
            value = line.split()
            if value[0] == 'END':
                head_end = True
                continue
            if(head_end and line[0] != 'G' and line[0] != 'R' and line[0] != 'E' and line[0] != 'C' and line[0] != ' '):
                year=(float(value[0]))
                month=(float(value[1]))
                day=(float(value[2]))
                hour=(float(value[3]))
                minute=(float(value[4]))
                second=(float(value[5]))
                num_sat = (float(value[6]))
                [w,soweek] = tr.ymd2gpst(year,month,day,hour,minute,second)
                if (w_last==0):
                    w_last = w
                if (last_day == 0):
                    last_day = day
                #soweek = soweek + (w-w_last)*604800
                soweek = (day - last_day)*24 + hour + minute/60.0 + second/3600.0
                if (hour_in == 24):
                    soweek = (day - last_day)*24 + hour + minute/60.0 + second/3600.0
                else:
                     if (hour_in < 24 and (hour < (24 - hour_in) / 2)):
                        num_sat = -1
                w_last=w
                if (hour_in > 24 and (day - last_day) != 1):
                    num_sat = -1
                if soweek not in all_data.keys() and num_sat!=-1:
                    all_data[soweek]={}
            if(head_end and (line[0] == 'G' or line[0] == 'R' or line[0] == 'E' or line[0] == 'C') and num_sat >= Nsat):
                sat = value[0]
                if sat not in all_data[soweek].keys():
                    all_data[soweek][sat]={}
                all_data[soweek][sat]['LAT']=float(value[1])
                all_data[soweek][sat]['LON']=float(value[2])
                all_data[soweek][sat]['ELE']=float(value[3])
                all_data[soweek][sat]['AZI']=float(value[4])
                all_data[soweek][sat]['MPF']=float(value[5])
                all_data[soweek][sat]['TEC']=float(value[6])
    return all_data

def open_upd_nl_file(filename_list,sys="G"):
    all_data = {} 
    for index in filename_list:
        filename = filename_list[index]
        w_last = 0
        with open(filename,'rt') as f:
            for line in f:
                value = line.split()
                if value[0] == '%':
                    # if value[4] != 'upd_NL' or value[4] != 'upd_WL':
                    #     return 0
                    continue
                if value[0]=='EPOCH-TIME':
                    day = (float(value[1]))
                    sec = (float(value[2]))
                    [w,soweek] = tr.mjd2gpst(day,sec)
                    if (w_last==0):
                        w_last = w
                    soweek = soweek + (w-w_last)*604800
                    if soweek not in all_data.keys():
                        all_data[soweek]={}
                    w_last = w
                    continue
                if value[0] == 'EOF':
                    break
                sat = value[0]
                if 'x' not in sat and sat not in all_data[soweek].keys():
                    all_data[soweek][sat] = (float(value[1]))
                    continue
    return all_data

def open_upd_wl_onedayfile(filename_list):
    all_data = {} 
    for index in filename_list:
        filename = filename_list[index]
        w_last = 0
        with open(filename,'rt') as f:
            for line in f:
                value = line.split()
                if value[0] == '%':
                    continue
                if value[0] == "EOF":
                    break
                sat = value[0]
                if sat not in all_data.keys():
                    all_data[sat] = float(value[1])
                    continue
    return all_data

def open_flt_ppplsq_file(filename):
    all_data={}
    soweek_last = 0
    w_last = 0
    head_end = False
    epoch_flag = True
    with open(filename,'rt') as f:
        for line in f:
            value = line.split()
            if line[0] == '%':
                head_end = True
                continue
            if head_end:
                ymd = value[1]
                hms = value[2]
                year = float(ymd[0:4])
                month = float(ymd[5:7])
                day = float(ymd[8:10])
                hour = float(hms[0:2])
                minute = float(hms[3:5])
                second = float(hms[6:12])
                [w,soweek] = tr.ymd2gpst(year,month,day,hour,minute,second)
                if (w_last==0):
                    w_last = w
                soweek = soweek + (w-w_last)*604800
                #soweek = hour + minute/60.0 + second/3600.0
                if soweek not in all_data.keys():
                    all_data[soweek]={}
                all_data[soweek]['X'] = float(value[5])
                all_data[soweek]['Y'] = float(value[6])
                all_data[soweek]['Z'] = float(value[7])
                all_data[soweek]['CLK'] = float(value[11])
                all_data[soweek]['NSAT'] = float(value[13])
                all_data[soweek]['GDOP'] = float(value[15])
                all_data[soweek]['PDOP'] = float(value[16])
                if value[17] == 'Fixed':
                    all_data[soweek]['AMB'] = 1
                else:
                    all_data[soweek]['AMB'] = 0
                
    return all_data

def get_gridhead(filename):
    head_str = ""
    with open(filename,"rt") as f:
        for line in f:
            if line[0] == ">":
                return head_str,resnumber
            head_str = head_str + line
            if "OBS TYPES" in line:
                value = line.split()
                for cur_value in value:
                    if "Res" in cur_value:
                        resnumber = int(cur_value[-3:])

def open_grid_file(filename,time_delay = 0):
    all_data = {}
    soweek_last = 0
    w_last = 0
    head_end = False
    epoch_flag = False
    with open(filename,"rt") as f:
        for line in f:
            value = line.split()
            if "REFERENCE" in line:
                ref_lat,ref_lon =  float(value[0]),float(value[2])
            if "OBS TYPES" in line:
                for cur_value in value:
                    if "Res" in cur_value:
                        resnumber = int(cur_value[-3:])
            if (value[0] == ">"):
                year,month,day,hour,minute,second=(float(value[1])),(float(value[2])),(float(value[3])),(float(value[4])),(float(value[5])),(float(value[6]))
                [w,soweek] = tr.ymd2gpst(year,month,day,hour,minute,second)
                if (not epoch_flag):
                    min_sow = soweek
                if (soweek < min_sow):
                    soweek = soweek + 604800
                epoch_flag = True
                soweek = soweek + time_delay
                if soweek not in all_data.keys():
                    all_data[soweek]={}
            if (value[0][0] == "C" or value[0][0] == "E" or value[0][0] == "G" or value[0] == "TRP") and epoch_flag:
                if value[0] not in all_data[soweek].keys():
                    all_data[soweek][value[0]] = []
                all_data[soweek][value[0]].append(float(value[1]))
                all_data[soweek][value[0]].append(float(value[2]))
                all_data[soweek][value[0]].append(float(value[3]))
                all_data[soweek][value[0]].append(float(value[4]))
                all_data[soweek][value[0]].append(float(value[5]))
                all_data[soweek][value[0]].append(float(value[6]))
                if value[0] == "TRP":
                    for i in range(resnumber):
                        all_data[soweek][value[0]].append(float(value[6+i+1]))
    return all_data,ref_lat,ref_lon


def open_flt_pvtflt_file(filename):
    all_data={}
    soweek_last = 0
    w_last = 0
    head_end = False
    epoch_flag = True
    with open(filename,'rt') as f:
        for line in f:
            value = line.split()
            if line[0] == " ":
                soweek = float(value[0])
                if (soweek + w_last*604800 < soweek_last):
                    w_last = w_last + 1
                soweek = soweek + w_last*604800
                soweek_last = soweek
                #soweek = hour + minute/60.0 + second/3600.0
                if soweek not in all_data.keys():
                    all_data[soweek]={}
                all_data[soweek]['X'] = float(value[1])
                all_data[soweek]['Y'] = float(value[2])
                all_data[soweek]['Z'] = float(value[3])
                all_data[soweek]['NSAT'] = float(value[13])
                all_data[soweek]['PDOP'] = float(value[14])
                all_data[soweek]['Q'] = float(value[18])
                if value[16] == 'Fixed' and all_data[soweek]['Q']  == 1:
                    all_data[soweek]['AMB'] = 1
                else:
                    all_data[soweek]['AMB'] = 0
                if all_data[soweek]['PDOP'] > 5:
                    all_data[soweek]['AMB'] = 0
                
    return all_data

def open_flt_pos_rtpppfile(filename):
    all_data={}
    soweek_last = 0
    w_last = 0
    head_end = False
    epoch_flag = True
    with open(filename,'rt') as f:
        for line in f:
            value = line.split()
            if line[0] != "%":
                soweek = float(value[1])
                # soweek = float(value[3])*3600+float(value[4])*60+float(value[5])
                if (soweek < soweek_last):
                    w_last = w_last + 1
                soweek_last = soweek
                soweek = soweek + w_last*604800
                #soweek = hour + minute/60.0 + second/3600.0
                if soweek not in all_data.keys():
                    all_data[soweek]={}
                all_data[soweek]['X'] = float(value[2])
                all_data[soweek]['Y'] = float(value[3])
                all_data[soweek]['Z'] = float(value[4])

                # all_data[soweek]['X'] = float(value[17])
                # all_data[soweek]['Y'] = float(value[18])
                # all_data[soweek]['Z'] = float(value[19])

                all_data[soweek]['Q'] = float(value[5])
                all_data[soweek]['NSAT'] = float(value[5])
                all_data[soweek]['PDOP'] = float(value[5])
                # if value[5] == '1':
                #     all_data[soweek]['AMB'] = 1
                # else:
                #     all_data[soweek]['AMB'] = 0
                # all_data[soweek]['AMB'] = 1
                if value[15] == 'Fixed':
                    all_data[soweek]['AMB'] = 1
                else:
                    all_data[soweek]['AMB'] = 0
                
    return all_data

def open_bias_file_grid(filename):
    all_data={}
    head_info={}
    soweek_last = 0
    w_last = 0
    head_end = False
    epoch_flag = False
    num_sat = 0
    last_day = 0
    day=0
    file_exist = os.path.exists(filename)
    if (not file_exist):
        return all_data
    with open(filename,'rt') as f:
        for line in f:
            value = line.split()                
            if ">" in line:
                value=line.split()
                year=(float(value[1]))
                month=(float(value[2]))
                day=(float(value[3]))
                hour=(float(value[4]))
                minute=(float(value[5]))
                second=(float(value[6]))
                [w,soweek] = tr.ymd2gpst(year,month,day,hour,minute,second)
                if (not epoch_flag):
                    min_sow = soweek
                if (soweek < min_sow):
                    soweek = soweek + 604800
                epoch_flag = True
                if soweek not in all_data.keys():
                    all_data[soweek]={}
                    all_data[soweek]["G"] = {}
                    all_data[soweek]["E"] = {}
                    all_data[soweek]["C"] = {}
                continue
            if (epoch_flag):
                if (len(line) <= 4):
                    continue
                site = value[0][0:4]
                i = 1
                for type in  all_data[soweek].keys():
                    if 18*i-1 > len(line) - 1 or 18*i+6 > len(line) - 1:
                        break
                    # cur_value = line[12*i-9:12*i+3].strip()
                    cur_value = line[18*i-1:18*i+6].strip()
                    if (len(cur_value) > 1):
                        all_data[soweek][type][site] = float(cur_value)
                    i = i+1
    return (all_data)

def open_pos_ref_IE(filename):
    all_data={}
    soweek_last = 0
    w_last = 0
    head_end = False
    epoch_flag = True
    with open(filename,'rt') as f:
        for line in f:
            value = line.split()
            if line[0] != "%":
                soweek = float(value[1])
                if (soweek < soweek_last):
                    w_last = w_last + 1
                soweek = soweek + w_last*604800
                soweek_last = soweek
                #soweek = hour + minute/60.0 + second/3600.0
                if soweek not in all_data.keys():
                    all_data[soweek]={}
                all_data[soweek]['X'] = float(value[2])
                all_data[soweek]['Y'] = float(value[3])
                all_data[soweek]['Z'] = float(value[4])
                all_data[soweek]['Q'] = float(value[5])
                all_data[soweek]['NSAT'] = float(value[5])
                all_data[soweek]['PDOP'] = float(value[5])
                if value[27] == 'Fixed':
                    all_data[soweek]['AMB'] = 1
                else:
                    all_data[soweek]['AMB'] = 0
                
    return all_data


def open_crd_gridmap(filename):
    all_data={}
    soweek_last = 0
    w_last = 0
    head_end = False
    epoch_flag = True
    with open(filename,'rt') as f:
        for line in f:
            value = line.split()
            
            head_end = True
            if len(value) >= 5:
                if value[4] == "False":
                    head_end = False
            if head_end:
                site = value[0]
                if site not in all_data.keys():
                    all_data[site]=[]
                all_data[site].append(float(value[1]))
                all_data[site].append(float(value[2]))
                all_data[site].append(float(value[3]))
                
    return all_data


def H_open_sigma_grid(filename,sys="G"):
    all_data_G,all_data_E,all_data_C={},{},{}
    soweek_last = 0
    w_last = 0
    head_end = False
    epoch_flag = True
    with open(filename,'rt') as f:
        for line in f:
            value = line.split()
            if (len(value) <= 2):
                continue
            ymd = value[1]
            hms = value[2]
            year = float(ymd[0:4])
            month = float(ymd[5:7])
            day = float(ymd[8:10])
            hour = float(hms[0:2])
            minute = float(hms[3:5])
            second = float(hms[6:8])
            [w,soweek] = tr.ymd2gpst(year,month,day,hour,minute,second)
            if (w_last==0):
                    w_last = w
            soweek = soweek + (w-w_last)*604800
            sat = value[4]
            if (sat[0] == "G"):
                if soweek not in all_data_G.keys():
                    all_data_G[soweek]={}
                if len(value) <=5:
                    continue
                all_data_G[soweek][sat] = abs(float(value[5]))
            if (sat[0] == "E"):
                if soweek not in all_data_E.keys():
                    all_data_E[soweek]={}
                if len(value) <=5:
                    continue
                all_data_E[soweek][sat] = abs(float(value[5]))
            if (sat[0] == "C"):
                if soweek not in all_data_C.keys():
                    all_data_C[soweek]={}
                if len(value) <=5:
                    continue
                all_data_C[soweek][sat] = abs(float(value[5]))
    return (all_data_G,all_data_E,all_data_C)

def H_open_residual_grid(filename):
    all_data_res={}
    all_data_dis={}
    all_data_num={}
    soweek_last = 0
    w_last = 0
    head_end = False
    epoch_flag = True
    with open(filename,'rt') as f:
        for line in f:
            value = line.split()
            if (len(value) <= 2):
                continue
            ymd = value[1]
            hms = value[2]
            year = float(ymd[0:4])
            month = float(ymd[5:7])
            day = float(ymd[8:10])
            hour = float(hms[0:2])
            minute = float(hms[3:5])
            second = float(hms[6:8])
            [w,soweek] = tr.ymd2gpst(year,month,day,hour,minute,second)
            if (w_last==0):
                    w_last = w
            soweek = soweek + (w-w_last)*604800
            sat = value[4]
            site_site = value[3]
            dis = value[5]
            if soweek not in all_data_res.keys():
                all_data_res[soweek]={}
            all_data_dis[site_site] = dis
            if site_site not in all_data_num.keys():
                all_data_num[site_site] = {}
                all_data_num[site_site]["G"] = 1
                all_data_num[site_site]["E"] = 1
                all_data_num[site_site]["C"] = 1
            else:
                all_data_num[site_site][sat[0]] = all_data_num[site_site][sat[0]] + 1
            all_data_res[soweek][sat + ":" + site_site] = abs(float(value[6]))
    return (all_data_res,all_data_dis,all_data_num)

def open_ltt_file(filename,Fixed=True,SPP=True):
    if not SPP:
        if Fixed:
            all_data={}
            soweek_last = 0
            w_last = 0
            head_end = False
            epoch_flag = True
            with open(filename,'rt') as f:
                for line in f:
                    value = line.split()
                    if value[0] != "Week":
                        soweek = float(value[1])
                        if (soweek < soweek_last):
                            w_last = w_last + 1
                        soweek = soweek + w_last*604800
                        soweek_last = soweek
                        #soweek = hour + minute/60.0 + second/3600.0
                        if soweek not in all_data.keys():
                            all_data[soweek]={}
                        all_data[soweek]['X'] = float(value[5])
                        all_data[soweek]['Y'] = float(value[6])
                        all_data[soweek]['Z'] = float(value[7])
                        all_data[soweek]['NSAT'] = float(value[8])
                        all_data[soweek]['PDOP'] = float(value[9])
                        if value[10] == 'Fixed':
                            all_data[soweek]['AMB'] = 1
                        else:
                            all_data[soweek]['AMB'] = 0
        else:
            all_data={}
            soweek_last = 0
            w_last = 0
            head_end = False
            epoch_flag = True
            with open(filename,'rt') as f:
                for line in f:
                    value = line.split()
                    if value[0] != "Week":
                        soweek = float(value[1])
                        if (soweek < soweek_last):
                            w_last = w_last + 1
                        soweek = soweek + w_last*604800
                        soweek_last = soweek
                        #soweek = hour + minute/60.0 + second/3600.0
                        if soweek not in all_data.keys():
                            all_data[soweek]={}
                        all_data[soweek]['X'] = float(value[2])
                        all_data[soweek]['Y'] = float(value[3])
                        all_data[soweek]['Z'] = float(value[4])
                        all_data[soweek]['NSAT'] = float(value[8])
                        all_data[soweek]['PDOP'] = float(value[9])
                        all_data[soweek]['AMB'] = 1
    else:
        all_data={}
        soweek_last = 0
        w_last = 0
        head_end = False
        epoch_flag = True
        with open(filename,'rt') as f:
            for line in f:
                value = line.split()
                if value[0] != "Week":
                    soweek = float(value[1])
                    if (soweek < soweek_last):
                        w_last = w_last + 1
                    soweek = soweek + w_last*604800
                    soweek_last = soweek
                    #soweek = hour + minute/60.0 + second/3600.0
                    if soweek not in all_data.keys():
                        all_data[soweek]={}
                    all_data[soweek]['X'] = float(value[2])
                    all_data[soweek]['Y'] = float(value[3])
                    all_data[soweek]['Z'] = float(value[4])
                    all_data[soweek]['NSAT'] = float(value[5])
                    all_data[soweek]['PDOP'] = float(value[6])
                    all_data[soweek]['AMB'] = 1           
    return all_data


def open_flt_ppp_rtpppfile(filename):
    all_data={}
    soweek_last = 0
    w_last = 0
    head_end = False
    epoch_flag = True
    with open(filename,'rt') as f:
        for line in f:
            value = line.split()
            if line[0] != "%":
                soweek = float(value[7])
                if (soweek < soweek_last):
                    w_last = w_last + 1
                soweek = soweek + w_last*604800
                soweek_last = soweek
                #soweek = hour + minute/60.0 + second/3600.0
                if soweek not in all_data.keys():
                    all_data[soweek]={}
                all_data[soweek]['X'] = float(value[17])
                all_data[soweek]['Y'] = float(value[18])
                all_data[soweek]['Z'] = float(value[19])
                all_data[soweek]['Q'] = float(value[20])
                all_data[soweek]['NSAT'] = float(value[20])
                all_data[soweek]['PDOP'] = float(value[20])
                all_data[soweek]['AMB'] = 1
                
    return all_data

def open_aug_file_rtppp(filename):
    all_data={}
    head_info={}
    soweek_last = 0
    w_last = 0
    head_end = False
    epoch_flag = False
    num_sat = 0
    last_day = 0
    day=0
    file_exist = os.path.exists(filename)
    if (not file_exist):
        return all_data
    with open(filename,'rt') as f:
        for line in f:
            value = line.split()
            if len(value) <= 0:
                continue
            if value[0] == "%" or value[0] == "##" or value[0] == "amb":
                epoch_flag = False
                continue               
            if value[0]=="*":
                value=line.split()
                year=(float(value[1]))
                month=(float(value[2]))
                day=(float(value[3]))
                hour=(float(value[4]))
                minute=(float(value[5]))
                second=(float(value[6]))
                satnum = float(value[7])
                [w,soweek] = tr.ymd2gpst(year,month,day,hour,minute,second)
                if (not epoch_flag):
                    min_sow = soweek
                if (soweek < min_sow):
                    soweek = soweek + 604800
                epoch_flag = True
                if soweek not in all_data.keys():
                    all_data[soweek]={}
            if ((value[0][0] == "C" or value[0][0] == "E" or value[0][0] == "G") and epoch_flag):
                sat = value[0]
                if (sat not in all_data[soweek].keys()):
                    all_data[soweek][sat] = {}
                all_data[soweek][sat]["L1"] = float(value[1])
                all_data[soweek][sat]["P1"] = float(value[2])
                all_data[soweek][sat]["L2"] = float(value[3])
                all_data[soweek][sat]["P2"] = float(value[4])
                all_data[soweek][sat]["TRP1"] = satnum
                all_data[soweek][sat]["NSAT"] = satnum
                all_data[soweek][sat]["ELE"] = satnum

    head_info["G"]={}
    head_info["G"]["L1"]=1
    head_info["G"]["P1"]=2
    head_info["G"]["L2"]=3
    head_info["G"]["P2"]=4
    head_info["E"]={}
    head_info["E"]["L1"]=1
    head_info["E"]["P1"]=2
    head_info["E"]["L2"]=3
    head_info["E"]["P2"]=4
    head_info["C"]={}
    head_info["C"]["L1"]=1
    head_info["C"]["P1"]=2
    head_info["C"]["L2"]=3
    head_info["C"]["P2"]=4
    return (head_info,all_data)


def open_ppp_float_rtpppfile(filename):
    all_data={}
    soweek_last = 0
    w_last = 0
    head_end = False
    epoch_flag = True
    with open(filename,'rt') as f:
        for line in f:
            value = line.split()
            if line[0] != "%":
                soweek = float(value[7])
                if (soweek < soweek_last):
                    w_last = w_last + 1
                soweek = soweek + w_last*604800
                soweek_last = soweek
                #soweek = hour + minute/60.0 + second/3600.0
                if soweek not in all_data.keys():
                    all_data[soweek]={}
                all_data[soweek]['E'] = float(value[8])
                all_data[soweek]['N'] = float(value[9])
                all_data[soweek]['U'] = float(value[10])
                all_data[soweek]['NSAT'] = float(value[10])
                all_data[soweek]['AMB'] = 1
                
                # if value[15] == 'Fixed':
                #     all_data[soweek]['AMB'] = 1
                # else:
                #     all_data[soweek]['AMB'] = 0
                
    return all_data


def open_pos_ref_GREAT(filename):
    all_data={}
    soweek_last = 0
    w_last = 0
    head_end = False
    epoch_flag = True
    with open(filename,'rt') as f:
        for line in f:
            value = line.split()
            if line[0] != "#":
                soweek = float(value[0])
                if (soweek < soweek_last):
                    w_last = w_last + 1
                soweek = soweek + w_last*604800
                soweek_last = soweek
                #soweek = hour + minute/60.0 + second/3600.0
                if soweek not in all_data.keys():
                    all_data[soweek]={}
                all_data[soweek]['X'] = float(value[1])
                all_data[soweek]['Y'] = float(value[2])
                all_data[soweek]['Z'] = float(value[3])
                all_data[soweek]['Q'] = float(value[5])
                all_data[soweek]['NSAT'] = float(value[5])
                all_data[soweek]['PDOP'] = float(value[5])
                if value[19] == 'Fixed':
                    all_data[soweek]['AMB'] = 1
                else:
                    all_data[soweek]['AMB'] = 0
                
    return all_data


def open_flt_ppprtk_rtpppfile(filename):
    all_data={}
    soweek_last = 0
    w_last = 0
    head_end = False
    epoch_flag = True
    with open(filename,'rt') as f:
        for line in f:
            value = line.split()
            if line[0] != "%":
                soweek = float(value[7])
                if (soweek < soweek_last):
                    w_last = w_last + 1
                soweek = soweek + w_last*604800
                soweek_last = soweek
                #soweek = hour + minute/60.0 + second/3600.0
                if soweek not in all_data.keys():
                    all_data[soweek]={}
                all_data[soweek]['X'] = float(value[29])
                all_data[soweek]['Y'] = float(value[30])
                all_data[soweek]['Z'] = float(value[31])
                all_data[soweek]['Q'] = float(value[20])
                all_data[soweek]['NSAT'] = float(value[20])
                all_data[soweek]['PDOP'] = float(value[20])
                all_data[soweek]['AMB'] = 1
                
    return all_data

def open_arinf_rtpppfile(filename,sat = "G15"):
    all_data={}
    soweek_last = 0
    w_last = 0
    head_end = False
    epoch_flag = True
    wr=False
    data1 = []
    time1 = []
    with open(filename,'rt') as f:
        for line in f:
            value = line.split()
            time = value[0].split(':')
            if len(time) > 2:
                year=2022
                mon=6
                day=22
                hour = float(time[0])
                min = float(time[1])
                sec = float(time[2])
                [w,soweek] = tr.ymd2gpst(year,mon,day,hour,min,sec)
                if (w_last == 0):
                    w_last = w
                soweek = soweek + (w - w_last)*7*24*3600
            if value[0] == "WL_INF":
                wr = True
                continue
            elif not wr:
                wr=False
                continue
            if wr and value[0][0] != sat[0]:
                wr=False
            if wr and value[0]==sat:
                data1.append(float(value[1]))
                time1.append(soweek)
                wr = False
  
    return (time1,data1)

def open_ppprtk_rtpppfile(filename):
    all_data={}
    soweek_last = 0
    w_last = 0
    head_end = False
    epoch_flag = True
    with open(filename,'rt') as f:
        for line in f:
            value = line.split()
            if line[0] != "%":
                soweek = float(value[7])
                if (soweek < soweek_last):
                    w_last = w_last + 1
                soweek = soweek + w_last*604800
                soweek_last = soweek
                #soweek = hour + minute/60.0 + second/3600.0
                if soweek not in all_data.keys():
                    all_data[soweek]={}
                all_data[soweek]['X'] = float(value[29])
                all_data[soweek]['Y'] = float(value[30])
                all_data[soweek]['Z'] = float(value[31])
                all_data[soweek]['Q'] = float(value[20])
                # all_data[soweek]['NSAT'] = float(value[24])
                all_data[soweek]['NSAT'] = float(value[12])
                # all_data[soweek]['NSAT'] = float(value[18])
                all_data[soweek]['PDOP'] = float(value[23])
                if (all_data[soweek]['NSAT'] <= 5):
                    all_data[soweek]['AMB'] = 0
                else:
                    all_data[soweek]['AMB'] = 1
                # all_data[soweek]['AMB'] = 1
                
    return all_data


def open_upd_rtpppfile(filename_list,sys="G"):
    all_data = {}
    all_data["upd_NL"],all_data["upd_WL"] = {},{}
    for index in filename_list:
        filename = index
        w_last = 0
        with open(filename,'rt') as f:
            for line in f:
                value = line.split()
                if value[0]=='*':
                    if value[7] == "0":
                        continue
                    year=float(value[1])
                    mon=float(value[2])
                    day=float(value[3])
                    hour = float(value[4])
                    min = float(value[5])
                    sec = float(value[6])
                    [w,soweek] = tr.ymd2gpst(year,mon,day,hour,min,sec)
                    if (w_last==0):
                        w_last = w
                    soweek = soweek + (w-w_last)*604800
                    if soweek not in all_data["upd_NL"].keys():
                        all_data["upd_NL"][soweek],all_data["upd_WL"][soweek]={},{}
                    w_last = w
                    continue
                
                sat = value[0]
                if 'x' not in sat and sat not in all_data["upd_NL"][soweek].keys():
                    all_data["upd_NL"][soweek][sat] = [float(value[2]),float(value[2])]
                    all_data["upd_WL"][soweek][sat] = [float(value[1]),float(value[2])]
                    continue
    return all_data


def open_augc_file_rtppp(filename,sitename):
    all_data={}
    head_info={}
    soweek_last = 0
    w_last = 0
    head_end = False
    epoch_flag = False
    num_sat = 0
    last_day = 0
    day=0
    file_exist = os.path.exists(filename)
    if (not file_exist):
        return all_data
    with open(filename,'rt') as f:
        for line in f:
            value = line.split()               
            if value[0]=="*":
                value=line.split()
                year=(float(value[1]))
                month=(float(value[2]))
                day=(float(value[3]))
                hour=(float(value[4]))
                minute=(float(value[5]))
                second=(float(value[6]))
                satnum = float(value[7])
                [w,soweek] = tr.ymd2gpst(year,month,day,hour,minute,second)
                if (not epoch_flag):
                    min_sow = soweek
                if (soweek < min_sow):
                    soweek = soweek + 604800
                epoch_flag = True
                if soweek not in all_data.keys():
                    all_data[soweek]={}
                continue
            all_data[soweek][sitename[int(value[0])-1]] = int(value[1])
            continue

    return (all_data)

def open_ismr(filename):
    all_data={}
    soweek_last = 0
    w_last = 0
    head_end = False
    epoch_flag = True
    file_exist = os.path.exists(filename)
    if (not file_exist):
        return all_data
    with open(filename,'rt') as f:
        for line in f:
            value = line.split()
            if len(value) != 10:
                continue
            if line[0] != "%":
                soweek = float(value[1])
                if (soweek < soweek_last):
                    w_last = w_last + 1
                soweek = soweek + w_last*604800
                soweek_last = soweek
                #soweek = hour + minute/60.0 + second/3600.0
                if soweek not in all_data.keys():
                    all_data[soweek]={}
                sat=value[2]
                all_data[soweek][sat] = float(value[9])
    return all_data


def open_epo_file_rtppp(filename):
    all_data={}
    head_info={}
    soweek_last = 0
    w_last = 0
    head_end = False
    epoch_flag = False
    num_sat = 0
    last_day = 0
    day=0
    file_exist = os.path.exists(filename)
    if (not file_exist):
        return all_data
    with open(filename,'rt') as f:
        for line in f:
            value = line.split()
            if value[0] == "%" or value[0] == "##" or value[0] == "amb":
                epoch_flag = False
                continue               
            if value[0]=="*":
                value=line.split()
                year=(float(value[1]))
                month=(float(value[2]))
                day=(float(value[3]))
                hour=(float(value[4]))
                minute=(float(value[5]))
                second=(float(value[6]))
                satnum = float(value[9])
                [w,soweek] = tr.ymd2gpst(year,month,day,hour,minute,second)
                if (not epoch_flag):
                    min_sow = soweek
                if (soweek < min_sow):
                    soweek = soweek + 604800
                epoch_flag = True
                if soweek not in all_data.keys():
                    all_data[soweek]={}
            if ((value[0][0] == "C" or value[0][0] == "E" or value[0][0] == "G") and epoch_flag):
                sat = value[0]
                if (sat not in all_data[soweek].keys()):
                    all_data[soweek][sat] = {}
                all_data[soweek][sat]["L1"] = float(value[1])
                all_data[soweek][sat]["NSAT"] = satnum

    
    return all_data

def open_gpgga_file(gpgga,year=2022,mon=7,day=26):
    t,X,Y,Z,nsat,hdop,state=[],[],[],[],[],[],[]
    count=0
    all_data={}
    with open(gpgga,'rt') as f:
        for line in f:
            value=line.split(',')
            if(value[0] != '$GPGGA'):
                if (value[0] != '$GNGGA'):
                    continue
            hour=float(value[1][0:2])
            min=float(value[1][2:4])
            sec=float(value[1][4:]) + 18
            [w,sec_all] = tr.ymd2gpst(year,mon,day,hour,min,sec)
            # if (soweek < min_sow):
            #     soweek = soweek + 604800
            # sec_all = hour*3600+min*60+sec
            if(value[2]==''):
                continue
            b_deg=float(value[2][0:2])
            b_min=float(value[2][2:])
            b=(b_deg+b_min/60)
            if(value[3]==''):
                continue
            l_deg=float(value[4][0:3])
            l_min=float(value[4][3:])
            l=(l_deg+l_min/60)
            h=float(value[9])+float(value[11])
            # sec_all = sec_all - 18
            if sec_all not in all_data.keys():
                all_data[sec_all]={}
                XYZ = tr.blh2xyz(b*glv.deg,l*glv.deg,h)
                all_data[sec_all]["X"]=XYZ[0]
                all_data[sec_all]["Y"]=XYZ[1]
                all_data[sec_all]["Z"]=XYZ[2]
                all_data[sec_all]['AMB'] = 1
            if(float(value[6])!=4):
                count=count+1
                continue
        
    return all_data

def open_pos_ref_HDBD(filename):
    all_data={}
    soweek_last = 0
    w_last = 0
    head_end = False
    epoch_flag = True
    with open(filename,'rt') as f:
        for line in f:
            value = line.split()
            if line[0] != "%":
                soweek = float(value[1])
                if (soweek < soweek_last):
                    w_last = w_last + 1
                soweek = soweek + w_last*604800
                soweek_last = soweek
                #soweek = hour + minute/60.0 + second/3600.0
                if soweek not in all_data.keys():
                    all_data[soweek]={}
                XYZ = tr.blh2xyz(float(value[3])*glv.deg,float(value[4])*glv.deg,float(value[5]))
                all_data[soweek]['X'] = XYZ[0]
                all_data[soweek]['Y'] = XYZ[1]
                all_data[soweek]['Z'] = XYZ[2]           
                all_data[soweek]['AMB'] = 1
                
    return all_data


def open_diff_file_new(filename):
    all_data={}
    head_info={}
    soweek_last = 0
    w_last = 0
    head_end = False
    epoch_flag = False
    num_sat = 0
    last_day = 0
    day=0
    file_exist = os.path.exists(filename)
    if (not file_exist):
        return all_data
    with open(filename,'rt') as f:
        for line in f:
            value = line.split()
            if "SYS / # / AUG TYPES" in line:
                head_end = True
                head_index = 1
                for cur_value in value:
                    if (cur_value == "SYS"):
                        break
                    if (len(cur_value) != 1):
                        if line[0] not in head_info.keys():
                            head_info[line[0]]={}
                        head_info[line[0]][cur_value] = head_index
                        head_index = head_index + 1                   
            if ">" in line:
                value=line.split()
                year=(float(value[1]))
                month=(float(value[2]))
                day=(float(value[3]))
                hour=(float(value[4]))
                minute=(float(value[5]))
                second=(float(value[6]))
                [w,soweek] = tr.ymd2gpst(year,month,day,hour,minute,second)
                if (not epoch_flag):
                    min_sow = soweek
                if (soweek < min_sow):
                    soweek = soweek + 604800
                epoch_flag = True
                if soweek not in all_data.keys():
                    all_data[soweek]={}
            if ((value[0][0] == "C" or value[0][0] == "E" or value[0][0] == "G") and epoch_flag):
                if (len(line) <= 4):
                    continue
                sat = value[0]
                if (sat not in all_data[soweek].keys()):
                    all_data[soweek][sat] = {}
                i = 1
                for type in head_info[sat[0]].keys():
                    if 12*i-9 > len(line) - 1 or 12*i+3 > len(line) - 1:
                        break
                    # cur_value = line[12*i-9:12*i+3].strip()
                    cur_value = line[12*i-8:12*i+4].strip()
                    if (len(cur_value) > 1):
                        all_data[soweek][sat][type] = float(cur_value)
                    i = i+1


    return (head_info,all_data)

def H_open_rms(filename,index=1,all_num = 1):
    all_data={}
    file_exist = os.path.exists(filename)
    recover_list = []
    if (not file_exist):
        return all_data
    with open(filename,'rt') as f:
        for line in f:
            value = line.split()
            if value[0] == "DOY":
                Total = int((len(value) - 1)/5)
                Total = all_num
                if index > Total:
                    return all_data
                if len(value) > (1+5*all_num):
                    reconver_num = int((len(value)-1-all_num*5) / all_num / 3)
                    for i in range(int(reconver_num)):
                        cur_recover_string = value[0+Total*5+i*3+1]
                        cur_recover_value = cur_recover_string.split("-")
                        recover_list.append(cur_recover_value[1])
                continue
            if "*" in value[0] and index == 2:
                continue
            if "*" in value[0]:
                doy = int(value[0][1:])
            else:
                doy = int(value[0])
            # if doy == 2 or doy == 8 or doy == 14 or doy == 20:
            if 1:
                # continue
            # if doy != 8:
            #     continue
            # if doy != 14:
            #     continue
            # if doy != 20:
            #     continue
                if doy not in all_data.keys():
                    all_data[doy]={}
                Fix = value[Total+index]
                all_data[doy]["FixSig"] = float(Fix)
                Fix = value[index]
                all_data[doy]["FixRaw"] = float(Fix)
                all_data[doy]["E"] = float(value[Total*2+index])
                all_data[doy]["N"] = float(value[Total*3+index])
                all_data[doy]["U"] = float(value[Total*4+index])
                all_data[doy]["3D"] = math.sqrt(all_data[doy]["E"]*all_data[doy]["E"]+all_data[doy]["N"]*all_data[doy]["N"]+all_data[doy]["U"]*all_data[doy]["U"])
                all_data[doy]["2D"] = math.sqrt(all_data[doy]["E"]*all_data[doy]["E"]+all_data[doy]["N"]*all_data[doy]["N"])
                if len(value) > (1+5*all_num):
                    # reconver_num = int((len(value)-1-all_num*5) / all_num / 3)
                    for i in range(int(reconver_num)):
                        # print(Total*5+2*index-1+i*Total*2)
                        # print(float(value[0+Total*5+i*3+index]))
                        # print(float(value[0+Total*5+i*3+index+reconver_num*Total]))
                        # print(float(value[0+Total*5+i*3+index+2*reconver_num*Total]))
                        cur_acc = recover_list[i]
                        all_data[doy]["{:0>3}-3".format(cur_acc)] = float(value[0+Total*5+i*3+index])
                        all_data[doy]["{:0>3}-V".format(cur_acc)] = float(value[0+Total*5+i*3+index+reconver_num*Total])
                        all_data[doy]["{:0>3}-H".format(cur_acc)] = float(value[0+Total*5+i*3+index+2*reconver_num*Total])
    
    return all_data


def H_open_log_ppprtk_client_wgt(filename,P_C = 1000):
    all_data={}
    all_data_dis={}
    all_data_num={}
    soweek_last = 0
    w_last = 0
    head_end = False
    epoch_flag = True
    index_normal = 0
    with open(filename,'rt') as f:
        for line in f:
            value = line.split()
            if len(value) < 15:
                continue
            if (value[0] != "Sat"):
                if (value[0] == "HongKong" or value[0]=="WuHan"):
                    index_normal = 1
                else:
                    continue
            if value[7] == "ROTIFac:" :
                index_normal = 1
            ymd = value[7+index_normal]
            hms = value[8+index_normal]
            year = float(ymd[0:4])
            month = float(ymd[5:7])
            day = float(ymd[8:10])
            hour = float(hms[0:2])
            minute = float(hms[3:5])
            second = float(hms[6:8])
            [w,soweek] = tr.ymd2gpst(year,month,day,hour,minute,second)
            if (w_last==0):
                    w_last = w
            soweek = soweek + (w-w_last)*604800
            sat = value[9+index_normal]
            site_site = value[3+index_normal]
            dis = value[5+index_normal]
            if soweek not in all_data.keys():
                all_data[soweek]={}
            if sat not in all_data[soweek].keys():
                all_data[soweek][sat]={}
                for index in range(6):
                    if value[7] == "ROTIFac:" :
                        all_data[soweek][sat][value[index+1]] = float(value[index+10+index_normal])
                    else:
                        all_data[soweek][sat][value[index+1+index_normal]] = float(value[index+10+index_normal])
                all_data[soweek][sat]["Grid"] = P_C/all_data[soweek][sat]["BaseFac"]*math.sqrt(P_C/all_data[soweek][sat]["BaseWgt"])
    return all_data

def H_open_mean_ppprtk_client_wgt(filename,index):
    all_data={}
    all_data_dis={}
    all_data_num={}
    soweek_last = 0
    w_last = 0
    head_end = False
    epoch_flag = True
    with open(filename,'rt') as f:
        for line in f:
            value = line.split()
            if value[2] not in all_data.keys():
                all_data[value[2]] = {}
            if int(value[0]) not in all_data[value[2]].keys():
                all_data[value[2]][int(value[0])] = {}
            all_data[value[2]][int(value[0])][value[1]] = float(value[index+2])

    return all_data

def open_flt_pvtflt_file_percent(filename,Year=1999,Mon=4,Day=24,Hour=2,Last=2):
    all_data={}
    soweek_last = 0
    w_last = 0
    head_end = False
    epoch_flag = True
    [week,secs] = tr.ymd2gpst(Year,Mon,Day,Hour,0,00)
    with open(filename,'rt') as f:
        for line in f:
            value = line.split()
            if line[0] == " ":
                soweek = float(value[0])
                if (soweek < soweek_last):
                    w_last = w_last + 1
                soweek = soweek + w_last*604800
                soweek_last = soweek
                #soweek = hour + minute/60.0 + second/3600.0
                if soweek >= secs and soweek < secs + Last*3600:
                    soweek_save = soweek - secs
                elif soweek <= secs:
                    continue
                if soweek >= secs + Last*3600:
                    return all_data
                if soweek_save not in all_data.keys():
                    all_data[soweek_save]={}
                all_data[soweek_save]['X'] = float(value[1])
                all_data[soweek_save]['Y'] = float(value[2])
                all_data[soweek_save]['Z'] = float(value[3])
                all_data[soweek_save]['NSAT'] = float(value[13])
                all_data[soweek_save]['PDOP'] = float(value[14])
                if value[16] == 'Fixed':
                    all_data[soweek_save]['AMB'] = 1
                else:
                    all_data[soweek_save]['AMB'] = 0
                
    return all_data

def open_upd_great(filename,all_data = {}):
    w_last = 0
    with open(filename,'rt') as f:
        for line in f:
            value = line.split()
            if value[0] == "%":
                all_data[value[4]] = {}
                mode = value[4]
                continue
            if value[0] == "EPOCH-TIME":
                [w,soweek] = tr.mjd2gpst(float(value[1]),float(value[2]))
                if (w_last==0):
                    w_last = w
                soweek = soweek + (w-w_last)*604800
                all_data[mode][soweek] = {}
                continue
            all_data[mode][soweek][value[0]] = [float(value[1]),float(value[3])]


def H_open_aug_file_for_heat(filename,year,mon,day,hour,min,sec,s_length):
    all_data={}
    new_all_data = []
    head_info={}
    soweek_last = 0
    w_last = 0
    head_end = False
    epoch_flag = False
    num_sat = 0
    last_day = 0
    # day=0
    file_exist = os.path.exists(filename)
    [w_need,soweek_need] = tr.ymd2gpst(year,mon,day,hour,min,sec)
    if (not file_exist):
        return all_data
    with open(filename,'rt') as f:
        for line in f:
            value = line.split()
            if "SYS / # / AUG TYPES" in line:
                head_end = True
                head_index = 1
                for cur_value in value:
                    if (cur_value == "SYS"):
                        break
                    if (len(cur_value) != 1):
                        if line[0] not in head_info.keys():
                            head_info[line[0]]={}
                        head_info[line[0]][cur_value] = head_index
                        head_index = head_index + 1                   
            if ">" in line:
                value=line.split()
                year=(float(value[1]))
                month=(float(value[2]))
                day=(float(value[3]))
                hour=(float(value[4]))
                minute=(float(value[5]))
                second=(float(value[6]))
                [w,soweek] = tr.ymd2gpst(year,month,day,hour,minute,second)
                if w<w_need:
                    continue
                if w>w_need:
                    return new_all_data
                if soweek<soweek_need:
                    continue
                if soweek > soweek_need + s_length:
                    return new_all_data
                
                if (not epoch_flag):
                    min_sow = soweek
                if (soweek < min_sow):
                    soweek = soweek + 604800
                epoch_flag = True
                if soweek not in all_data.keys():
                    all_data[soweek]={}
            
            # if ((value[0][0] == "C" or value[0][0] == "E" or value[0][0] == "G") and epoch_flag):
            if ((value[0][0] == "G") and epoch_flag):
                if (len(line) <= 4):
                    continue
                sat = value[0]
                if (sat not in all_data[soweek].keys()):
                    all_data[soweek][sat] = {}
                i = 1
                for type in head_info[sat[0]].keys():
                    if 12*i-9 > len(line) - 1 or 12*i+3 > len(line) - 1:
                        break
                    # cur_value = line[12*i-9:12*i+3].strip()
                    cur_value = line[12*i-8:12*i+4].strip()
                    
                    if (len(cur_value) > 1):
                        all_data[soweek][sat][type] = float(cur_value)
                        if i == 2:
                            new_all_data.append(float(cur_value))
                    i = i+1


    return all_data

def H_open_grid_file_for_heat(filename,year,mon,day,hour,min,sec,s_length):
    all_data={}
    new_all_data = []
    head_info={}
    soweek_last = 0
    w_last = 0
    head_end = False
    epoch_flag = False
    num_sat = 0
    last_day = 0
    # day=0
    file_exist = os.path.exists(filename)
    [w_need,soweek_need] = tr.ymd2gpst(year,mon,day,hour,min,sec)
    if (not file_exist):
        return all_data
    with open(filename,'rt') as f:
        for line in f:
            value = line.split()
            if "SYS / # / AUG TYPES" in line:
                head_end = True
                head_index = 1
                for cur_value in value:
                    if (cur_value == "SYS"):
                        break
                    if (len(cur_value) != 1):
                        if line[0] not in head_info.keys():
                            head_info[line[0]]={}
                        head_info[line[0]][cur_value] = head_index
                        head_index = head_index + 1
            if "OBS TYPES" in line:
                grid_node = int(value[7][10:13])
                data_all = [[] for i in range(grid_node)]
                all_data_new = []                  
            if ">" in line:
                value=line.split()
                year=(float(value[1]))
                month=(float(value[2]))
                day=(float(value[3]))
                hour=(float(value[4]))
                minute=(float(value[5]))
                second=(float(value[6]))
                [w,soweek] = tr.ymd2gpst(year,month,day,hour,minute,second)
                if w<w_need:
                    continue
                if w>w_need:
                    return new_all_data
                if soweek<soweek_need:
                    continue
                if soweek > soweek_need + s_length:
                    break
                
                if (not epoch_flag):
                    min_sow = soweek
                if (soweek < min_sow):
                    soweek = soweek + 604800
                epoch_flag = True
                if soweek not in all_data.keys():
                    all_data[soweek]={}
            
            if ((value[0][0] == "C" or value[0][0] == "E" or value[0][0] == "G") and epoch_flag):
            # if ((value[0][0] == "T") and epoch_flag):
                for i in range(grid_node):
                    cur_node_diff = float(value[grid_node+7+i])  # Diff
                    # cur_node_diff = float(value[grid_node+grid_node+5+i])  # Dis
                    if cur_node_diff == 9.9999:
                        continue
                    data_all[i].append(cur_node_diff)
    for i in range(grid_node):
        data_all[i].remove(np.max(data_all[i]))
        data_all[i].remove(np.max(data_all[i]))
        data_all[i].remove(np.min(data_all[i]))
        all_data_new.append(np.mean(data_all[i]))

    return all_data_new