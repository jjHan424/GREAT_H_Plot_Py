from calendar import c
from multiprocessing.dummy import DummyProcess
import os
from shutil import which
from socket import SHUT_WR
import sys
from turtle import st

from matplotlib import legend
from matplotlib.widgets import EllipseSelector
from scipy.__config__ import show
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
TRUE_Position = {
           "ALME":[36.85,-2.46,127.50],"ANK2":[39.84,32.78,1296.06],"ARJ6":[66.32,18.12,489.67],"BBYS":[48.75,19.15,487.43],"BRMF":[45.73,4.94,256.86],"COMO":[45.80,9.10,292.30],"ELBA":[42.75,10.21,271.76],"ESCO":[42.69,0.98,2508.44],"IZAN":[28.31,-16.50,2417.49],"JON6":[57.75,14.06,260.46],"KEV2":[69.76,27.01,136.33],"LEK6":[60.72,14.88,477.69],"LODZ":[51.78,19.46,259.42],"LPAL":[28.76,-17.89,2199.22],"MAS1":[27.76,-15.63,197.16],"MLVL":[48.84,2.59,160.46],"NABG":[78.94,11.86,42.77],"NICO":[35.14,33.40,190.11],"NYA1":[78.93,11.87,84.15],"NYAL":[78.93,11.87,78.43],"OST6":[63.44,14.86,489.83],"OVE6":[66.32,22.77,222.86],"QAQ1":[60.72,-46.05,109.64],"RAEG":[36.99,-25.13,297.91],"RANT":[54.81,8.29,47.15],"SAS2":[54.51,13.64,39.21],"SCOR":[70.49,-21.95,129.73],"SONS":[39.68,-3.96,808.95],"SPT0":[57.71,12.89,219.92],"TRO1":[69.66,18.94,138.07],"UME6":[63.58,19.51,55.12],"VARS":[70.34,31.03,174.88],"VLN1":[51.94,-10.24,76.83],"WUTH":[77.00,15.54,52.06],"HKSC":[22.32,114.14119537381285,20.23]
           }

def load_data_roti(File_name, all_data = {}, data_type = "ROTI" , start_week = 0, Time = []):
    soweek_last = 0
    w_last = start_week
    if len(Time) > 0:
        [w_want,sow_want] = tr.ymd2gpst(Time[0],Time[1],Time[2],Time[3],Time[4],Time[5])
    if os.path.exists(File_name):
        with open(File_name,'rt') as f:
            for line in f:
                value = line.split()
                # if len(value) < 15:
                #     continue
                year,doy,sod = int(value[0]),int(value[1]),float(value[2])
                sat = value[3]
                roti = float(value[10])
                [year,mon,day] = tr.doy2ymd(year,doy)
                [w,soweek] = tr.ymd2gpst(year,mon,day,0,0,sod)
                if len(Time) > 0:
                    if soweek > sow_want:
                        break
                    if w > w_want:
                        break
                    if w!=w_want:
                        continue
                    if sow_want != soweek:
                        continue
                if (w_last==0):
                    w_last = w
                soweek = soweek + (w-w_last)*604800
                if soweek not in all_data[data_type].keys():
                    all_data[data_type][soweek] = {}
                all_data[data_type][soweek][sat] = {}
                all_data[data_type][soweek][sat]["ROTI"] = roti
                if len(value) > 11:
                    all_data[data_type][soweek][sat]["Ele"] = float(value[11])
                    all_data[data_type][soweek][sat]["Azi"] = float(value[12])
                    all_data[data_type][soweek][sat]["Lat"] = float(value[13])
                    all_data[data_type][soweek][sat]["Lon"] = float(value[14])

def load_data_Dst(File_name,all_data = {},Start = []):
    soweek_last = 0
    w_last = 0
    [start_week,start_sow] = tr.ymd2gpst(Start[0],Start[1],Start[2],Start[3],Start[4],Start[5])
    with open(File_name,'rt') as f:
        for line in f:
            value_blank = line.split()
            if "|" not in line:
                value_ymd = value_blank[0].split("-")
                value_hms = value_blank[1].split(":")
                [w,soweek] = tr.ymd2gpst(float(value_ymd[0]),float(value_ymd[1]),float(value_ymd[2]),float(value_hms[0]),float(value_hms[1]),float(value_hms[2]))
                if w < start_week:
                    continue
                if (w_last==0):
                    w_last = w
                soweek = soweek + (w-w_last)*604800
                # cur_time = ((cur_gpst_week-Start_gpst[0])*7*24*3600 + (cur_gpst_sow - Start_gpst[1])) / 3600
                all_data[soweek] = float(value_blank[3])
    return all_data

def plot_roti_G_E_C(Plot_Data={}, Ylim=1.0, XlabelSet = [], Delta_date = 1, Show=True, Start = [], End = [], Legend = True, Save_dir = ""):
    figP,axP = plt.subplots(3,1,figsize=(12,10),sharey=True,sharex=True)
    sys_plotindex = {"G":0,"E":1,"C":2}
    #=== Plot ===#
    for cur_sat in Plot_Data.keys():
        if "TIME" in cur_sat:
            continue
        axP[sys_plotindex[cur_sat[0]]].scatter(Plot_Data[cur_sat+"-TIME"],Plot_Data[cur_sat],s=3)
    
    #===Set Label===#
    axP[0].set_xticks(XlabelSet[1])
    axP[0].set_xticklabels(XlabelSet[0])
    labels = axP[0].get_yticklabels()
    for i in range(3):
        labels = labels + axP[i].get_yticklabels() + axP[i].get_xticklabels()
        axP[i].set_ylim(0,Ylim)
    [label.set_fontsize(xtick_size) for label in labels]
    [label.set_fontname('Arial') for label in labels]
    axP[2].set_xlabel('GPS time (hour)',font_label,labelpad = 30)
    axP[1].set_ylabel('ROTI (TECU/min)',font_label)
    axP[0].set_title('GPS',font_title)
    axP[1].set_title('GAL',font_title)
    axP[2].set_title('BDS',font_title)
    duration_day = (XlabelSet[1][-1] - XlabelSet[1][0]) / 24
    ax_range = axP[2].axis()
    cur_date = Start
    end_doy = tr.ymd2doy(End[0],End[1],End[2],0,0,0)
    cur_doy = tr.ymd2doy(Start[0],Start[1],Start[2],0,0,0)
    start_doy = cur_doy
    while cur_doy < end_doy:
        axP[2].text(24*(cur_doy - start_doy),ax_range[2]-Ylim/3.7,"{}-{}-{}".format(cur_date[0],cur_date[1],cur_date[2]),font_text)
        cur_doy = tr.ymd2doy(cur_date[0],cur_date[1],cur_date[2],0,0,0) + Delta_date
        [cur_date[0],cur_date[1],cur_date[2]] = tr.doy2ymd(cur_date[0],cur_doy)
    if Show:
        plt.show()
    else:
        plt.savefig(Save_dir,dpi = 600)
        plt.close()

def plot_roti_GEC(Plot_Data={}, Ylim=1.0, XlabelSet = [], Delta_date = 1, Show=True, Start = [], End = [], Legend = True):
    figP,axP = plt.subplots(1,1,figsize=(12,6),sharey=True,sharex=True)
    box = axP.get_position()
    axP.set_position([box.x0, box.y0 + box.height*0.13, box.width, box.height*0.9])
    #=== Plot ===#
    for cur_sat in Plot_Data.keys():
        if "TIME" in cur_sat:
            continue
        axP.scatter(Plot_Data[cur_sat+"-TIME"],Plot_Data[cur_sat],s=3)
    
    #===Set Label===#
    axP.set_xticklabels(XlabelSet[0])
    axP.set_xticks(XlabelSet[1])
    labels = axP.get_yticklabels() + axP.get_xticklabels()
    axP.set_ylim(0,Ylim)
    [label.set_fontsize(xtick_size) for label in labels]
    [label.set_fontname('Arial') for label in labels]
    axP.set_xlabel('GPS time (hour)',font_label,labelpad = 30)
    axP.set_ylabel('ROTI (TECU/min)',font_label)
    duration_day = (XlabelSet[1][-1] - XlabelSet[1][0]) / 24
    ax_range = axP.axis()
    cur_date = Start
    end_doy = tr.ymd2doy(End[0],End[1],End[2],0,0,0)
    cur_doy = tr.ymd2doy(Start[0],Start[1],Start[2],0,0,0)
    start_doy = cur_doy
    while cur_doy < end_doy:
        axP.text(24*(cur_doy - start_doy),ax_range[2]-Ylim/7,"{}-{}-{}".format(cur_date[0],cur_date[1],cur_date[2]),font_text)
        cur_doy = tr.ymd2doy(cur_date[0],cur_date[1],cur_date[2],0,0,0) + Delta_date
        [cur_date[0],cur_date[1],cur_date[2]] = tr.doy2ymd(cur_date[0],cur_doy)
    if Show:
        plt.show() 

def plot_roti_GEC_Dst(Plot_Data={}, Ylim=1.0, XlabelSet = [], Delta_date = 1, Show=True, Start = [], End = [], Legend = True, Save_dir = ""):
    figP,axP = plt.subplots(2,1,figsize=(12,9),sharey=False,sharex=True)
    # box = axP.get_position()
    # axP.set_position([box.x0, box.y0 + box.height*0.13, box.width, box.height*0.9])
    #=== Plot ===#
    for cur_type in Plot_Data.keys():
        if "ROTI" in cur_type:
            site_name = cur_type
            for cur_sat in Plot_Data[cur_type].keys():
                if "TIME" in cur_sat:
                    continue
                axP[0].scatter(Plot_Data[cur_type][cur_sat+"-TIME"],Plot_Data[cur_type][cur_sat],s=3)
    axP[1].plot(Plot_Data["Dst"+"-TIME"],Plot_Data["Dst"])
    
    #===Set Label===#
    axP[1].set_xticklabels(XlabelSet[0])
    axP[1].set_xticks(XlabelSet[1])
    labels = axP[0].get_yticklabels() + axP[0].get_xticklabels() + axP[1].get_yticklabels() + axP[1].get_xticklabels()
    if Ylim != 0:
        axP[0].set_ylim(0,Ylim)
    [label.set_fontsize(xtick_size) for label in labels]
    [label.set_fontname('Arial') for label in labels]
    axP[1].set_xlabel('GPS time (hour)',font_label)
    axP[0].set_ylabel('ROTI (TECU/min)',font_label)
    axP[1].set_ylabel('Dst (nT)',font_label)
    # axP[0].set_title("{}: {:.2f}N, {:.2f}E".format(site_name[-4:],TRUE_Position[site_name[-4:]][0],TRUE_Position[site_name[-4:]][1]),font = font_title)
    axP[0].set_title("{}".format(site_name[-4:]),font = font_title)
    duration_day = (XlabelSet[1][-1] - XlabelSet[1][0]) / 24
    ax_range = axP[1].axis()
    cur_date = Start
    end_doy = tr.ymd2doy(End[0],End[1],End[2],0,0,0)
    cur_doy = tr.ymd2doy(Start[0],Start[1],Start[2],0,0,0)
    start_doy = cur_doy
    while cur_doy < end_doy:
        axP[1].text(24*(cur_doy - start_doy),ax_range[2],"{}-{}-{}".format(cur_date[0],cur_date[1],cur_date[2]),font_text)
        cur_doy = tr.ymd2doy(cur_date[0],cur_date[1],cur_date[2],0,0,0) + Delta_date
        [cur_date[0],cur_date[1],cur_date[2]] = tr.doy2ymd(cur_date[0],cur_doy)
    if Show:
        plt.show()
    else:
        plt.savefig(Save_dir,dpi = 600)
        plt.close()       

def plot_roti_multi_site_GEC(Plot_Data={}, Ylim=1.0, XlabelSet = [], Delta_date = 1, Show=True, Start = [], End = [], Legend = True):
    plot_num = len(Plot_Data)
    figP,axP = plt.subplots(plot_num,1,figsize=(12,3*plot_num),sharey=False,sharex=True)
    # box = axP[].get_position()
    # axP.set_position([box.x0, box.y0 + box.height*0.13, box.width, box.height*0.9])
    #=== Plot ===#
    index_plot = 0
    for cur_mode in Plot_Data.keys():
        for cur_sat in Plot_Data[cur_mode].keys():
            if "TIME" in cur_sat:
                continue
            axP[index_plot].scatter(Plot_Data[cur_mode][cur_sat+"-TIME"],Plot_Data[cur_mode][cur_sat],s=3)
        axP[index_plot].set_title(cur_mode[4:],font = font_title)
        index_plot = index_plot + 1
    
    #===Set Label===#
    axP[plot_num-1].set_xticklabels(XlabelSet[0])
    axP[plot_num-1].set_xticks(XlabelSet[1])
    labels = axP[0].get_yticklabels() + axP[0].get_xticklabels()
    for i in range(plot_num):
        labels = labels + axP[i].get_yticklabels() + axP[i].get_xticklabels()
        if Ylim != 0:
            axP[i].set_ylim(0,Ylim)
    [label.set_fontsize(xtick_size) for label in labels]
    [label.set_fontname('Arial') for label in labels]
    axP[plot_num-1].set_xlabel('GPS time (hour)',font_label,labelpad = 30)
    axP[int(index_plot/2)].set_ylabel('ROTI (TECU/min)',font_label)
    duration_day = (XlabelSet[1][-1] - XlabelSet[1][0]) / 24
    ax_range = axP[plot_num - 1].axis()
    cur_date = Start
    end_doy = tr.ymd2doy(End[0],End[1],End[2],0,0,0)
    cur_doy = tr.ymd2doy(Start[0],Start[1],Start[2],0,0,0)
    start_doy = cur_doy
    while cur_doy < end_doy:
        axP[index_plot-1].text(24*(cur_doy - start_doy),ax_range[2]-Ylim/3.5,"{}-{}-{}".format(cur_date[0],cur_date[1],cur_date[2]),font_text)
        cur_doy = tr.ymd2doy(cur_date[0],cur_date[1],cur_date[2],0,0,0) + Delta_date
        [cur_date[0],cur_date[1],cur_date[2]] = tr.doy2ymd(cur_date[0],cur_doy)
    if Show:
        plt.show()   

def Plot_timeseries_ROTI(File_info=[],Start=[],End=[],Plot_type=[],Ylim = 1.0,Delta_xlabel = 4,Delta_date = 3,Save_dir="",Show=True,All=False,Time_type = "GPST"):
    [start_week,start_sow] = tr.ymd2gpst(Start[0],Start[1],Start[2],Start[3],Start[4],Start[5])
    [end_week,end_sow] = tr.ymd2gpst(End[0],End[1],End[2],End[3],End[4],End[5])
    duration_time = (((end_week-start_week)*604800+(end_sow - start_sow))/3600)
    all_data = {}

    #=== load data ===#
    for cur_data_type in File_info.keys():
        if cur_data_type not in all_data.keys():
            all_data[cur_data_type] = {}
        if "ROTI" in cur_data_type:
            for cur_file in File_info[cur_data_type]:
                load_data_roti(cur_file,all_data,cur_data_type,start_week)
        elif "Dst" in cur_data_type:
            for cur_file in File_info[cur_data_type]:
                load_data_Dst(cur_file,all_data["Dst"],Start)
    
    #=== convert data ===#
    [XLabel,XTick,cov_time,begT,LastT]=glv.xtick(Time_type,Start[0],Start[1],Start[2],Start[3]+Start[4]/60,duration_time,Delta_xlabel)
    PLOT_ALL = {}
    for cur_mode in all_data.keys():
        if "ROTI" in cur_mode:
            if cur_mode not in PLOT_ALL.keys():
                PLOT_ALL[cur_mode] = {}
            for cur_time in all_data[cur_mode].keys():
                plot_time = (cur_time - cov_time) / 3600
                if ((plot_time >= Start[3] and plot_time <= (Start[3]+duration_time)) or All):
                    for cur_sat in all_data[cur_mode][cur_time].keys():
                        if cur_sat not in PLOT_ALL[cur_mode].keys():
                            PLOT_ALL[cur_mode][cur_sat] = []
                            PLOT_ALL[cur_mode][cur_sat+"-TIME"] = []
                        PLOT_ALL[cur_mode][cur_sat].append(all_data[cur_mode][cur_time][cur_sat]["ROTI"])
                        PLOT_ALL[cur_mode][cur_sat+"-TIME"].append(plot_time)
        if "Dst" in cur_mode:
            if cur_mode not in PLOT_ALL.keys():
                PLOT_ALL[cur_mode] = []
                PLOT_ALL[cur_mode+"-TIME"] = []
            for cur_time in all_data[cur_mode].keys():
                plot_time = (cur_time - cov_time) / 3600
                if ((plot_time >= Start[3] and plot_time <= (Start[3]+duration_time)) or All):
                    PLOT_ALL[cur_mode].append(all_data[cur_mode][cur_time])
                    PLOT_ALL[cur_mode+"-TIME"].append(plot_time)
        # if cur_mode == "ROTI_Multi_Site"
    
    #=== Plot ===#
    if len(Plot_type) == 1:
        if "G_E_C" in Plot_type[0]:
            plot_roti_G_E_C(Plot_Data=PLOT_ALL["ROTI"], Ylim=Ylim, XlabelSet = [XLabel,XTick], Delta_date = Delta_date, Start = Start, End = End, Show=Show, Save_dir = Save_dir)
        elif "GEC" in Plot_type[0]:
            plot_roti_GEC(Plot_Data=PLOT_ALL["ROTI"], Ylim=Ylim, XlabelSet = [XLabel,XTick], Delta_date = Delta_date, Start = Start, End = End, Show=Show)
        elif "Multi" in Plot_type[0]:
            plot_roti_multi_site_GEC(Plot_Data=PLOT_ALL, Ylim=Ylim, XlabelSet = [XLabel,XTick], Delta_date = Delta_date, Start = Start, End = End, Show=Show)
    else:
        plot_roti_GEC_Dst(Plot_Data=PLOT_ALL, Ylim=Ylim, XlabelSet = [XLabel,XTick], Delta_date = Delta_date, Start = Start, End = End, Show=Show, Save_dir = Save_dir)