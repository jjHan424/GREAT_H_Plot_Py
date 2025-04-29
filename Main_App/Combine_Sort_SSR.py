import os
from re import S
import sys
from turtle import color
sys.path.insert(0,os.path.dirname(__file__)+'/../LibBase')
sys.path.insert(0,os.path.dirname(__file__)+'/../LibPlot')
import numpy as np
import readfile as rf
import matplotlib as mpl
mpl.use("TkAgg")
import matplotlib.pyplot as plt
import dataprocess as dp
import draw as dr
import glv
import math
import csv
import trans as tr
class ORBIT:
    Name = "ORBIT"
    R,T,N = 0,0,0
    vR,vT,vN = 0,0,0
    IOD = 0
    # year,mon,day,hour,mins,secs = 0,0,0,0,0,0
    PRN = "G01"
    def toString(self):
        string_orb = "{}{:>12}{:>11.4f}{:>11.4f}{:>11.4f}{:>14.4f}{:>11.4f}{:>11.4f}".format(self.PRN,\
                                                                                             self.IOD,self.R,self.T,self.N,\
                                                                                             self.vR,self.vT,self.vN)
        return string_orb

class CLOCK:
    Name = "CLOCK"
    IOD = 0
    C0,C1,C2 = 0,0,0
    PRN = "G01"
    def toString(self):
        string_clk = "{}{:>12}{:>11.4f}{:>11.4f}{:>11.4f}".format(self.PRN,self.IOD,self.C0,self.C1,self.C2)
        return string_clk

class CODE_BIAS:
    Name = "CODE_BIAS"
    PRN = "G01"
    NUM = 0
    DATA = {}
    string_raw = ""
    def __init__(self):
        self.DATA = {}
    def toString(self):
        string_code = "{}{:>5}".format(self.PRN,self.NUM)
        for cur_key in self.DATA:
            string_code = string_code+"{:>5}{:>11.4f}".format(cur_key,self.DATA[cur_key])
        return string_code

class PHASE_BIAS:
    Name = "PHASE_BIAS"
    PRN = "G01"
    string_raw = ""
    def toString(self):
        return self.string_raw


def write_file(file = "",data_list = [],year = 0,mon = 0,day = 0,hour = 0,mins = 0,sec = 0):
    with open(file,'a') as f:
        for i in range(len(data_list)):
            if i == 0:
                if data_list[0].Name == "PHASE_BIAS":
                    f.write("> {}{:>5} {:0>2} {:0>2} {:0>2} {:0>2} {:0>2}.0 2 {} SSRA00{}\n".format(data_list[0].Name,year,mon,day,hour,mins,int(sec),len(data_list) - 1,AC))
                else:
                    f.write("> {}{:>5} {:0>2} {:0>2} {:0>2} {:0>2} {:0>2}.0 2 {} SSRA00{}\n".format(data_list[0].Name,year,mon,day,hour,mins,int(sec),len(data_list),AC))
            f.write(data_list[i].toString()+"\n")
        f.close()
        
#=== SETINGS ===#
inputFiledir = r"E:\PhD_1\4.RTZTD\Data\SSR"
outputFiledir = r"E:\PhD_1\4.RTZTD\Data\SSR"
AC = "CNE0"
start_time,end_time = [2025,100],[2025,103]
inter_val = 5
#===Start Process ===#
cur_time = start_time
outputFile =  os.path.join(outputFiledir,"SSRA00{}_S_{:4}{:0>3}0000_{:0>2}D_MC.ssr".format(AC,start_time[0],start_time[1], end_time[1] - start_time[1] + 1))
while cur_time[1] <= end_time[1]:
    cur_fileName = "SSRA00{}_S_{:4}{:0>3}0000_01D_MC.ssr".format(AC,cur_time[0],cur_time[1])
    cur_file = os.path.join(inputFiledir,cur_fileName)
    cur_ymd = tr.doy2ymd(cur_time[0],cur_time[1])
    cur_orb = ORBIT()
    cur_orb.PRN = "G11"
    temp = cur_orb.toString()
    cur_hms = [0,0,0]
    save_data,save_time = {},{}
    save_data["ORBIT"],save_data["CLOCK"],save_data["CODE_BIAS"],save_data["PHASE_BIAS"] = [],[],[],[]
    save_time["ORBIT"],save_time["CLOCK"],save_time["CODE_BIAS"],save_time["PHASE_BIAS"] = [],[],[],[]
    if os.path.exists(cur_file):
        with open(cur_file,'rt') as f_in:
            cur_type = "NONE"
            last_week,last_sow = 0,0
            rt_write = False
            flag_start_week,flag_start_sow = tr.doy2gpst(cur_time[0],cur_time[1],cur_hms[0],cur_hms[1],cur_hms[2] - 5)
            for line in f_in:
                value = line.split()
                if value[0] == ">":
                    if cur_type != "NONE" and cur_type != "VTEC":
                        if (last_week - data_week) + (last_sow - data_sow) != 0 and (last_week - flag_start_week) + (last_sow - flag_start_sow) != 0 and rt_write:
                            cur_hms[2] = cur_hms[2] + inter_val
                            if cur_hms[2] == 60:
                                cur_hms[2] = 0
                                cur_hms[1] = cur_hms[1] + 1
                            if cur_hms[1] == 60:
                                cur_hms[1] = 0
                                cur_hms[0] = cur_hms[0] + 1
                        cur_week,cur_sow = tr.doy2gpst(cur_time[0],cur_time[1],cur_hms[0],cur_hms[1],cur_hms[2])
                        delta_time = (data_week - cur_week) * 3600 + (data_sow - cur_sow)
                        if delta_time == 0:
                            write_file(outputFile,data_list,y,mon,d,h,m,s)
                            rt_write = True
                        if delta_time > 0:
                            save_data[cur_type].append(data_list)
                            save_time[cur_type].append([y,mon,d,h,m,s])
                    cur_type = value[1]
                    y,mon,d,h,m,s = int(value[2]),int(value[3]),int(value[4]),int(value[5]),int(value[6]),float(value[7])
                    if last_week != 0:
                        last_week,last_sow = data_week,data_sow
                    data_week,data_sow = tr.ymd2gpst(y,mon,d,h,m,s)
                    if last_week == 0:
                        last_week,last_sow = data_week,data_sow
                    update_indicator = int(value[8])
                    num_sat = int(value[9])
                    source = value[10]
                    data_list = []
                    continue
                if cur_type == "ORBIT":
                    cur_data = ORBIT()
                    cur_data.PRN,cur_data.IOD = value[0],int(value[1])
                    cur_data.R,cur_data.T,cur_data.N = float(value[2]),float(value[3]),float(value[4])
                    cur_data.vR,cur_data.vT,cur_data.vN = float(value[5]),float(value[6]),float(value[7])
                    data_list.append(cur_data)
                if cur_type == "CLOCK":
                    cur_data = CLOCK()
                    cur_data.PRN,cur_data.IOD = value[0],int(value[1])
                    cur_data.C0,cur_data.C1,cur_data.C2 = float(value[2]),float(value[3]),float(value[4])
                    data_list.append(cur_data)
                if cur_type == "CODE_BIAS":
                    cur_data = CODE_BIAS()
                    cur_data.PRN,cur_data.NUM = value[0],int(value[1])
                    for i in range(cur_data.NUM):
                        cur_data.DATA[value[2*i+2]] = float(value[2*i+3])
                    data_list.append(cur_data)
                if cur_type == "PHASE_BIAS":
                    cur_data = PHASE_BIAS()
                    cur_data.PRN,cur_data.string_raw = value[0],line[:-1]
                    data_list.append(cur_data)
    for i in range(len(save_time["ORBIT"])):
        y,mon,d,h,m,s = save_time["ORBIT"][i][0],save_time["ORBIT"][i][1],save_time["ORBIT"][i][2],\
        save_time["ORBIT"][i][3],save_time["ORBIT"][i][4],save_time["ORBIT"][i][5]
        write_file(outputFile,save_data["ORBIT"][i],y,mon,d,h,m,s)
        if save_time["ORBIT"][i] in save_time["CLOCK"]:
            write_file(outputFile,save_data["CLOCK"][i],y,mon,d,h,m,s)
        if save_time["ORBIT"][i] in save_time["CODE_BIAS"]:
            write_file(outputFile,save_data["CODE_BIAS"][i],y,mon,d,h,m,s)
        if save_time["ORBIT"][i] in save_time["PHASE_BIAS"]:
            write_file(outputFile,save_data["PHASE_BIAS"][i],y,mon,d,h,m,s)
    cur_time[1] = cur_time[1]+1