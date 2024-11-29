from calendar import c
from multiprocessing.dummy import DummyProcess
import os
from shutil import which
from socket import SHUT_WR
import sys
from turtle import st

from matplotlib import legend
from matplotlib.widgets import EllipseSelector
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
color_list = ["#0099E5","#34BF49","#FF4C4C"] #Blue #Green # Red ##f2af00 Yellow
# color_list = ["#0085c3","#7ab800","#71c6c1","#dc5034","#009bbb",
#               "#b7295a","#6e2585","#f2af00","#5482ab","#ce1126",
#               "#444444","#eeeeee"]

def load_data(File_name):
    file = open(File_name,"r")
    first_line = next(file)
    file.close()
    first_value = first_line.split()
    if first_value[0] == "#Seconds":
        AllData = loaddata_flt(File_name)
    elif first_value[0] == "%=TRO":
        AllData = loaddata_ref(File_name)
    return AllData

def loaddata_flt(File_name):
    all_data={}
    soweek_last = 0
    w_last = 0
    head_end = False
    epoch_flag = True
    with open(File_name,'rt') as f:
        for line in f:
            value = line.split()
            if line[0] == " ":
                soweek = float(value[0])
                if (soweek + w_last*604800 < soweek_last):
                    w_last = w_last + 1
                soweek = soweek + w_last*604800
                soweek_last = soweek
                soweek = int(soweek)
                #soweek = hour + minute/60.0 + second/3600.0
                if soweek not in all_data.keys():
                    all_data[soweek]={}
                if value[16] == 'Fixed' and value[18]  == "1":
                    all_data[soweek]['AMB'] = 1
                else:
                    all_data[soweek]['AMB'] = 0
                
                if float(value[14]) > 5:
                    all_data[soweek]['AMB'] = 0
                all_data[soweek]['ZWD'] = float(value[20])*1000
                
    return all_data

def loaddata_ref(File_name):
    all_data = {}
    epoch_flag,epoch_flag_time = False,False
    soweek_last = 0
    w_last = 0
    with open(File_name,"r") as f:
        for line in f:
            if line == "+TROP/SOLUTION\n":
                epoch_flag = True
                continue
            if line == "-TROP/SOLUTION\n":
                return all_data 
            if epoch_flag and line[0] != "*":
                value = line.split()
                time_value = value[1].split(":")
                ymd_now = tr.doy2ymd(int(time_value[0])+2000,int(time_value[1]))
                [w,soweek] = tr.ymd2gpst(ymd_now[0],ymd_now[1],ymd_now[2],float(time_value[2])/3600,0,0)
                if (not epoch_flag_time):
                    min_sow = soweek
                    epoch_flag_time = True
                if (soweek < min_sow):
                    soweek = soweek + 604800
                if soweek not in all_data.keys():
                    all_data[soweek]={}
                all_data[soweek]["ZWD"] = (float(value[2]))
                all_data[soweek]["AMB"] = 1
    return all_data

def compare_zwd(Data_raw,Data_ref):
    all_data = {}
    for cur_time in Data_raw.keys():
        if cur_time not in all_data.keys() and cur_time in Data_ref.keys():
            all_data[cur_time] = {}
            all_data[cur_time]["ZWD"] = Data_raw[cur_time]["ZWD"] - Data_ref[cur_time]["ZWD"]
            all_data[cur_time]["AMB"] = Data_raw[cur_time]["AMB"]
    return all_data

def plot_ZWD_delta(Plot_Data={}, Ylim=0.5, XlabelSet = [], Show=True, Legend = True):
    #=== Plot ===#
    figP,axP = plt.subplots(1,1,figsize=(12,6),sharey=True,sharex=True)
    mode_list = []
    index = 0
    for cur_mode in Plot_Data.keys():
        axP.plot(Plot_Data[cur_mode]["TIME"],Plot_Data[cur_mode]["ZWD"],linewidth=2,color = color_list[index%3])
        index = index + 1
        mode_list.append(cur_mode)
    #===Set Label===#
    axP.set_xticklabels(XlabelSet[0])
    axP.set_xticks(XlabelSet[1])
    labels = axP.get_yticklabels() + axP.get_xticklabels()
    axP.set_ylim(-Ylim,Ylim)
    [label.set_fontsize(xtick_size) for label in labels]
    [label.set_fontname('Arial') for label in labels]
    axP.set_xlabel('GPS time (hour)',font_label)
    axP.set_ylabel('ZWD errors (mm)',font_label)

    #===Set text===#
    MRS_str = "RMS:"
    for cur_mode in Plot_Data.keys():
        MRS_str = MRS_str + " {:.1f}mm,".format(np.sqrt(np.mean(np.array(Plot_Data[cur_mode]["ZWD"])**2)))
    ax_range = axP.axis()
    axP.text(ax_range[0],ax_range[3]+Ylim/25,MRS_str[:-1],font_text)
    print("{}".format(MRS_str))

    #===Set legend===#
    axP.legend(mode_list,prop=font_legend,
            framealpha=0,facecolor='none',ncol=4,numpoints=5,markerscale=3, 
            borderaxespad=0,bbox_to_anchor=(1,1.08),loc=1) 
    if Show:
        plt.show()

def plot_ZWD_raw(Plot_Data={}, Ylim=0.5, XlabelSet = [], Show=True, Legend = True):
    #=== Plot ===#
    figP,axP = plt.subplots(1,1,figsize=(12,6),sharey=True,sharex=True)
    mode_list = []
    index = 0
    for cur_mode in Plot_Data.keys():
        axP.plot(Plot_Data[cur_mode]["TIME"],Plot_Data[cur_mode]["ZWD"],linewidth=2,color = color_list[index%3])
        index = index + 1
        mode_list.append(cur_mode)
    #===Set Label===#
    axP.set_xticklabels(XlabelSet[0])
    axP.set_xticks(XlabelSet[1])
    labels = axP.get_yticklabels() + axP.get_xticklabels()
    [label.set_fontsize(xtick_size) for label in labels]
    [label.set_fontname('Arial') for label in labels]
    axP.set_xlabel('GPS time (hour)',font_label)
    axP.set_ylabel('ZWD (mm)',font_label)

    #===Set text===#
    # MRS_str = "RMS:"
    # for cur_mode in Plot_Data.keys():
    #     MRS_str = MRS_str + " {:.1f}mm,".format(np.sqrt(np.mean(np.array(Plot_Data[cur_mode]["ZWD"])**2)))
    # ax_range = axP.axis()
    # axP.text(ax_range[0],ax_range[3]+Ylim/25,MRS_str[:-1],font_text)
    # print("{}".format(MRS_str))

    #===Set legend===#
    axP.legend(mode_list,prop=font_legend,
            framealpha=0,facecolor='none',ncol=4,numpoints=5,markerscale=3, 
            borderaxespad=0,bbox_to_anchor=(1,1.08),loc=1) 
    if Show:
        plt.show()

def Plot_timeseries_zwd(File_info=[],Start=[],End=[],Plot_type=[],Ylim=0.5,Save_dir="",Fixed = False,Show=True,All=False,Time_type = "GPST",Delta_xlabel = 1,Delay_model = 0,Legend = False,Sigma=3,Signum=0):
    all_data = {}
    [start_week,start_sow] = tr.ymd2gpst(Start[0],Start[1],Start[2],Start[3],Start[4],Start[5])
    [end_week,end_sow] = tr.ymd2gpst(End[0],End[1],End[2],End[3],End[4],End[5])
    duration_time = ((end_week-start_week)*604800+(end_sow - start_sow))/3600
    #=== load data ===#
    if Plot_type == "DELTA":
        for i in range(len(File_info)):
            data_raw = load_data(File_info[i][0])
            data_ref = load_data(File_info[i][1])  
            all_data[File_info[i][2]] = compare_zwd(data_raw,data_ref)
    elif Plot_type == "RAW":
        for i in range(len(File_info)):
            all_data[File_info[i][1]] = load_data(File_info[i][0])
    
    #=== convert data ===#
    [XLabel,XTick,cov_time,begT,LastT]=glv.xtick(Time_type,Start[0],Start[1],Start[2],Start[3]+Start[4]/60,duration_time,Delta_xlabel)
    PLOT_ALL, PLOT_RAW = {},{}
    for cur_mode in all_data.keys():
        for cur_time in all_data[cur_mode].keys():
            plot_time = (cur_time - cov_time) / 3600
            if ((plot_time >= Start[3] and plot_time <= (Start[3]+duration_time)) or All):
                if Fixed and all_data[cur_mode][cur_time]["AMB"] != 1:
                    continue
                if cur_mode not in PLOT_ALL.keys():
                    PLOT_ALL[cur_mode],PLOT_RAW[cur_mode] = {},{}
                    PLOT_ALL[cur_mode]["TIME"],PLOT_RAW[cur_mode]["TIME"] = [],[]
                    PLOT_ALL[cur_mode]["ZWD"],PLOT_RAW[cur_mode]["ZWD"] = [],[]
                PLOT_ALL[cur_mode]["TIME"].append(plot_time)
                PLOT_RAW[cur_mode]["TIME"].append(plot_time)
                PLOT_ALL[cur_mode]["ZWD"].append(all_data[cur_mode][cur_time]["ZWD"])
                PLOT_RAW[cur_mode]["ZWD"].append(all_data[cur_mode][cur_time]["ZWD"])
    
    #=== plot ===#
    if Plot_type == "DELTA":
        plot_ZWD_delta(Plot_Data=PLOT_ALL, Ylim=Ylim, XlabelSet = [XLabel,XTick], Show=Show)
    elif Plot_type == "RAW":
        plot_ZWD_raw(Plot_Data=PLOT_ALL, Ylim=Ylim, XlabelSet = [XLabel,XTick], Show=Show)
