from calendar import c
from multiprocessing.dummy import DummyProcess
import os
from socket import SHUT_WR
import sys
from turtle import st
sys.path.insert(0,os.path.dirname(__file__)+'/../LibBase')
from matplotlib.markers import MarkerStyle
import numpy as np
import matplotlib as mpl
mpl.use("TkAgg")
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import scienceplots
plt.style.use(['science','grid','no-latex'])
# plt.style.use('science')
from numpy.core.fromnumeric import shape, size
import dataprocess as dp
import matplotlib.colors as colors
# from matplotlib.pyplot import MultipleLocator
import seaborn as sns
import math
import trans as tr
import glv
import os
from mpl_toolkits.axes_grid1.inset_locator import mark_inset
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

#=== FONT SET ===#
font_title = {'family' : 'Arial', 'weight' : 300, 'size' : 20}
font_label = {'family' : 'Arial', 'weight' : 300, 'size' : 20}
font_tick = {'family' : 'Arial', 'weight' : 300, 'size' : 35}
font_legend = {'family' : 'Arial', 'weight' : 300, 'size' : 20}
# font_legend = {'family' : 'Times New Roman', 'weight' : 600, 'size' : 15}
font_text = {'family' : 'Arial','weight' : 300,'size'   : 20}
xtick_size = 20
color_list = ["#0099E5","#34BF49","#FF4C4C"]
# color_list = ["#0085c3","#7ab800","#71c6c1","#dc5034","#009bbb",
#               "#b7295a","#6e2585","#f2af00","#5482ab","#ce1126",
#               "#444444","#eeeeee"]

def load_data(filename,time_delay = 0):
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
                # if (sat[0] not in all_data[soweek].keys()):
                #     all_data[soweek][sat[0]] = {}
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

def compare_aug(data_raw = {},data_model = {}):
    all_data = {}
    ref_data = {}
    for time in data_model.keys():
        if time not in data_raw.keys():
            continue
        if time not in all_data.keys():
            all_data[time] = {}
            ref_data[time] = {}
        Ele_index,Ele_cur,Ele_sort,ref_sat = {},{},{},{}
        for sat in data_model[time].keys():
            if len(sat) <= 1:
                continue
            if sat not in data_raw[time].keys():
                continue
            if sat[0] not in Ele_index.keys():
                Ele_index[sat[0]],Ele_cur[sat[0]],Ele_sort[sat[0]] = [],[],[]
            Ele_index[sat[0]].append(sat)
            if "ELE" in data_raw[time][sat].keys():
                Ele_cur[sat[0]].append(data_raw[time][sat]["ELE"])
                Ele_sort[sat[0]].append(data_raw[time][sat]["ELE"])
            else:
                Ele_cur[sat[0]].append(0)
                Ele_sort[sat[0]].append(0)
        
        for sys_cur in Ele_cur.keys():
            Ele_sort[sys_cur].sort(reverse = True)
            index_max_ele = np.array(Ele_cur[sys_cur]) == Ele_sort[sys_cur][0]
            ref_sat[sys_cur] = np.array(Ele_index[sys_cur])[index_max_ele]
            if sys_cur in ref_sat.keys():
                for type in data_model[time][sat].keys():
                    sys_type = ref_sat[sys_cur][0][0] + "_" + type
                    if type not in data_raw[time][ref_sat[sys_cur][0]].keys():
                        continue    
                    ref_data[time][sys_cur] = 0                
                    ref_data[time][sys_type] = data_model[time][ref_sat[sys_cur][0]][type] - data_raw[time][ref_sat[sys_cur][0]][type]

        for sat in data_model[time].keys():
            if sat not in data_raw[time].keys():
                continue
            if sat not in all_data[time].keys() and sat[0] in ref_data[time].keys():
                all_data[time][sat] = {}
            for type in data_model[time][sat].keys():
                sys_type = sat[0] + "_" + type
                if type not in data_raw[time][sat].keys():
                    continue               
                if sys_type not in ref_data[time]:   
                    ref_data[time][sat[0]] = 0                
                    ref_data[time][sys_type] = data_model[time][ref_sat[sat[0]][0]][type] - data_raw[time][ref_sat[sat[0]][0]][type]
                    ref_data[time][sys_type] = data_model[time][sat][type] - data_raw[time][sat][type]
                else:
                    if "ELE" in data_raw[time][sat].keys():
                        all_data[time][sat]["ELE"] = data_raw[time][sat]["ELE"]
                    if type == "TRP1":
                        all_data[time][sat][type] = (data_model[time][sat][type] - data_raw[time][sat][type])
                    else:
                        # if data_I[time][sat][type] == 0.0 or data_S[time][sat][type] == 0.0:
                        #     continue
                        all_data[time][sat][type] = (data_model[time][sat][type] - data_raw[time][sat][type]) - ref_data[time][sys_type]
        for sat in data_model[time].keys():
            if sat not in all_data[time].keys():
                continue
            for type in data_model[time][sat].keys():
                if type[0] != "d":
                    continue
                all_data[time][sat][type] = data_model[time][sat][type]
    return all_data

def plot_ION_G_E_C(Plot_Data={}, Ylim=0.5, XlabelSet = [], Show=True):
    #=== Plot ===#
    figP,axP = plt.subplots(3,1,figsize=(12,15),sharey=True,sharex=True)
    sys_plotindex = {"G":0,"E":1,"C":2}
    for cur_sat in Plot_Data.keys():
        axP[sys_plotindex[cur_sat[0]]].scatter(Plot_Data[cur_sat]["TIME"],Plot_Data[cur_sat]["ION1"],s=3)
    
    #===Set Label===#
    axP[2].set_xlabel('GPS time (hour)',font_label)
    axP[1].set_ylabel('Difference of Ionosphere Delay correction/m',font_label)
    # aaaaaa = axP[1].yaxis.get_label_coords()
    axP[1].yaxis.set_label_coords(-0.1,0.5)
    axP[0].set_title('GPS',font_title)
    axP[1].set_title('GAL',font_title)
    axP[2].set_title('BDS',font_title)
    plt.show()

def plot_timeseries_aug_compare(File_info=[],Start=[],End=[],Plot_type=[],Ylim=0.5,Save_dir="",Show=True,All=False,Time_type = "GPST",Delta_xlabel = 1,Delay_model = 0,Sigma=3,Signum=0):
    
    [start_week,start_sow] = tr.ymd2gpst(Start[0],Start[1],Start[2],Start[3],Start[4],Start[5])
    [end_week,end_sow] = tr.ymd2gpst(End[0],End[1],End[2],End[3],End[4],End[5])
    duration_time = ((end_week-start_week)*604800+(end_sow - start_sow))/3600
    #=== Load data ===#
    [head_raw,data_raw] = load_data(File_info[0],Delay_model)
    [head_model,data_model] = load_data(File_info[1],Delay_model)

    #=== Compare AUG ===#
    data_compare = compare_aug(data_raw,data_model)

    #=== Data Convert ===#
    [XLabel,XTick,cov_time,begT,LastT]=glv.xtick(Time_type,Start[0],Start[1],Start[2],Start[3]+Start[4]/60,duration_time,Delta_xlabel)
    PLOT_ALL, PLOT_RAW = {},{}
    for cur_time in data_compare.keys():
        plot_time = (cur_time - cov_time) / 3600
        if ((plot_time >= Start[3] and plot_time <= (Start[3]+duration_time)) or All):
            for cur_sat in data_compare[cur_time].keys():
                if cur_sat not in PLOT_ALL.keys():
                    PLOT_ALL[cur_sat], PLOT_RAW[cur_sat] = {},{}
                    PLOT_ALL[cur_sat]["TIME"], PLOT_RAW[cur_sat]["TIME"] = [],[]
                PLOT_ALL[cur_sat]["TIME"].append(plot_time)
                PLOT_RAW[cur_sat]["TIME"].append(plot_time)
                for cur_type in data_compare[cur_time][cur_sat].keys():
                    if cur_type not in PLOT_ALL[cur_sat].keys():
                        PLOT_ALL[cur_sat][cur_type], PLOT_RAW[cur_sat][cur_type] = [],[]
                    PLOT_ALL[cur_sat][cur_type].append(data_compare[cur_time][cur_sat][cur_type])
                    PLOT_RAW[cur_sat][cur_type].append(data_compare[cur_time][cur_sat][cur_type])

    #=== Plot ===#
    if Plot_type == "ION":
        plot_ION_G_E_C(Plot_Data=PLOT_ALL, Ylim=Ylim, XlabelSet = [XLabel,XTick], Show=Show)
            

