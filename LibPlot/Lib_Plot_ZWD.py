from calendar import c
from genericpath import exists
from multiprocessing.dummy import DummyProcess
import os
from shutil import which
from socket import SHUT_WR
import sys
from tempfile import tempdir
from tkinter.filedialog import SaveAs
from turtle import mode, st

from matplotlib import legend
import matplotlib
import matplotlib.patches
from matplotlib.widgets import EllipseSelector
from matplotlib.patches import Rectangle
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

def load_data(File_name,AllData = {}, Inter_zpd = False):
    if not os.path.exists(File_name):
        # print(File_name)
        return
    file = open(File_name,"r")
    first_line = next(file)
    file.close()
    first_value = first_line.split()
    if first_value[0] == "#Seconds":
        loaddata_flt(File_name, AllData)
    elif first_value[0] == "%=TRO":
        loaddata_ref(File_name, AllData, Inter_zpd)
    # return AllData

def loaddata_flt(File_name,all_data={}): 
    w_last = 0
    head_end = False
    epoch_flag = True
    gradient = False
    soweek_last = 0
    if len(all_data) != 0:
        all_time = list(all_data.keys())
        np_time = np.array(all_time)
        soweek_last = np_time.max()
        num_slip_week = math.floor(soweek_last/604498)
    with open(File_name,'rt') as f:
        for line in f:
            value = line.split()
            if line[0:2] == "#S":
                if "TGN" in line:
                    gradient = True
            if line[0] == " ":
                soweek = float(value[0])
                if soweek < soweek_last:
                    soweek = soweek + num_slip_week * 604800
                # if (soweek + w_last*604800 < soweek_last):
                #     w_last = w_last + 1
                # soweek = soweek + w_last*604800
                # soweek_last = soweek
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
                if gradient:
                    if len(value) > 22:
                        all_data[soweek]['ZWD'] = float(value[20])*1000
                        all_data[soweek]['TGN'] = float(value[21])
                        all_data[soweek]['TGE'] = float(value[22])
                    else:
                        all_data[soweek]['ZWD'] = float(value[19])*1000
                        all_data[soweek]['TGN'] = float(value[20])
                        all_data[soweek]['TGE'] = float(value[21])
                else:
                    if len(value) > 20:
                        all_data[soweek]['ZWD'] = float(value[20])*1000
                        all_data[soweek]['TGN'] = float(value[20])
                        all_data[soweek]['TGE'] = float(value[20])
                    else:
                        all_data[soweek]['ZWD'] = float(value[19])*1000
                        all_data[soweek]['TGN'] = float(value[19])
                        all_data[soweek]['TGE'] = float(value[19])
                
    # return all_data

def loaddata_ref(File_name,all_data = {}, Inter_zpd = False):
    epoch_flag,epoch_flag_time = False,False
    soweek_last = 0
    w_last = 0
    if len(all_data) != 0:
        all_time = list(all_data.keys())
        np_time = np.array(all_time)
        soweek_last = np_time.max()
        num_slip_week = math.floor(soweek_last/604498)
        # num_slip_week = 1
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
                if soweek < soweek_last:
                    soweek = soweek + num_slip_week * 604800
                if (not epoch_flag_time):
                    min_sow = soweek
                    epoch_flag_time = True
                # if (soweek < min_sow):
                #     soweek = soweek + 604800
                if soweek not in all_data.keys():
                    all_data[soweek]={}
                all_data[soweek]["ZWD"] = (float(value[2]))
                all_data[soweek]["TGN"] = (float(value[4]))
                all_data[soweek]["TGE"] = (float(value[6]))
                all_data[soweek]["AMB"] = 1
                #=== Interp ===#
                if Inter_zpd:
                    if len(all_data) > 1:
                        key_list = list(all_data.keys())
                        last_time = key_list[-1]
                        pre_time = key_list[-2]
                        cur_time = pre_time
                        x_new_list = []
                        while cur_time < last_time:
                            x_new_list.append(cur_time)
                            cur_time = cur_time + 30
                        x_new = np.array(x_new_list)
                        x_known = np.array([pre_time,last_time])
                        for cur_type in all_data[soweek].keys():
                            y_known = np.array([all_data[pre_time][cur_type],all_data[last_time][cur_type]])
                            y_new = np.interp(x_new,x_known,y_known)
                            index = 0
                            for cur_time in x_new_list:
                                if cur_time not in all_data.keys():
                                    all_data[cur_time]={}
                                all_data[cur_time][cur_type] = y_new[index]
                                index = index + 1
    # return all_data

def compare_zwd(Data_raw,Data_ref):
    all_data = {}
    for cur_time in Data_raw.keys():
        if cur_time not in all_data.keys() and cur_time in Data_ref.keys():
            all_data[cur_time] = {}
            all_data[cur_time]["ZWD"] = Data_raw[cur_time]["ZWD"] - Data_ref[cur_time]["ZWD"]
            all_data[cur_time]["TGN"] = Data_raw[cur_time]["TGN"] - Data_ref[cur_time]["TGN"]
            all_data[cur_time]["TGE"] = Data_raw[cur_time]["TGE"] - Data_ref[cur_time]["TGE"]
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
    axP.set_xticks(XlabelSet[1])
    axP.set_xticklabels(XlabelSet[0])
    labels = axP.get_yticklabels() + axP.get_xticklabels()
    if Ylim != 0:
        axP.set_ylim(-Ylim,Ylim)
    [label.set_fontsize(xtick_size) for label in labels]
    [label.set_fontname('Arial') for label in labels]
    axP.set_xlabel('GPS time (hour)',font_label)
    axP.set_ylabel('ZWD errors (mm)',font_label)

    #===Set text===#
    MRS_str = "RMS:"
    for cur_mode in Plot_Data.keys():
        time_np = np.array(Plot_Data[cur_mode]["TIME"])
        mintime,max_time = time_np.min(),time_np.max()
        day_num = math.ceil(max_time / 24)
        index_all = []
        while day_num > 0:
            index_all.append((time_np >= 2 + 24*(day_num - 1)) & (time_np <= 24 + 24*(day_num - 1)))
            day_num = day_num - 1
        i = 0
        index_rms = index_all[0]
        while i < len(index_all):
            index_rms = index_rms | index_all[i]
            i = i + 1
        MRS_str = MRS_str + " {:.1f}mm,".format(np.sqrt(np.mean(np.array(Plot_Data[cur_mode]["ZWD"])[index_rms]**2)))
    ax_range = axP.axis()
    axP.text(ax_range[0],ax_range[3]+Ylim/25,MRS_str[:-1],font_text)
    print("{}".format(MRS_str))

    #===Set legend===#
    axP.legend(mode_list,prop=font_legend,
            framealpha=0,facecolor='none',ncol=4,numpoints=5,markerscale=3, 
            borderaxespad=0,bbox_to_anchor=(1,1.08),loc=1)
     
    if Show:
        plt.show()

def plot_MultiDay_ZWD_delta(Plot_Data={}, Ylim=0.5, XlabelSet = [], Show=True, Legend = True, Start_hour = 0, End_hour = 24, Start = [], End = [], Save_dir = ""):
    #=== Plot ===#
    figP,axP = plt.subplots(1,1,figsize=(12,6),sharey=True,sharex=True)
    mode_list = []
    index = 0
    for cur_mode in Plot_Data.keys():
        time_np = np.array(Plot_Data[cur_mode]["TIME"])
        mintime,max_time = time_np.min(),time_np.max()
        day_num = math.ceil(max_time / 24)
        while day_num > 0:
            index_plot = (time_np >= Start_hour + 24*(day_num - 1)) & (time_np <= End_hour + 24*(day_num - 1))
            day_num = day_num - 1
            # axP.plot(time_np[index_plot],np.array(Plot_Data[cur_mode]["ZWD"])[index_plot],linewidth=2,color = color_list[index%3])
            axP.scatter(time_np[index_plot],np.array(Plot_Data[cur_mode]["ZWD"])[index_plot],color = color_list[index%3],s=15)
        index = index + 1
        mode_list.append(cur_mode)
    #===Set Label===#
    axP.set_xticks(XlabelSet[1])
    axP.set_xticklabels(XlabelSet[0])
    labels = axP.get_yticklabels() + axP.get_xticklabels()
    if Ylim != 0:
        axP.set_ylim(-Ylim,Ylim)
    [label.set_fontsize(xtick_size) for label in labels]
    [label.set_fontname('Arial') for label in labels]
    # axP.set_xlabel('GPS time (hour)',font_label)
    axP.set_xlabel('Time (YYYY-MM-DD)',font_label)
    axP.set_ylabel('ZWD errors (mm)',font_label)
    # Date
    XlabelDate = []
    for cur_hour in XlabelSet[1]:
        doy = tr.ymd2doy(Start[0],Start[1],Start[2],Start[3] + cur_hour,Start[4],Start[5])
        [year,mon,day] = tr.doy2ymd(Start[0],doy)
        XlabelDate.append("{}-{:0>2}-{:0>2}".format(year,mon,day))
    axP.set_xticklabels(XlabelDate)
    #===Set text===#
    MRS_str = "RMS:"
    RMS_value = []
    for cur_mode in Plot_Data.keys():
        time_np = np.array(Plot_Data[cur_mode]["TIME"])
        mintime,max_time = time_np.min(),time_np.max()
        day_num = math.ceil(max_time / 24)
        index_all = []
        while day_num > 0:
            index_all.append((time_np >= Start_hour + 24*(day_num - 1)) & (time_np <= End_hour + 24*(day_num - 1)))
            day_num = day_num - 1
        i = 0
        index_rms = index_all[0]
        while i < len(index_all):
            index_rms = index_rms | index_all[i]
            i = i + 1
        MRS_str = MRS_str + " {:.1f}mm,".format(np.sqrt(np.mean(np.array(Plot_Data[cur_mode]["ZWD"])[index_rms]**2)))
        RMS_value.append(np.sqrt(np.mean(np.array(Plot_Data[cur_mode]["ZWD"])[index_rms]**2)))
    MRS_str = MRS_str + " {:.2f}%,".format((RMS_value[0] - RMS_value[1])/RMS_value[0]*100)
    ax_range = axP.axis()
    axP.text(ax_range[0],ax_range[3]+Ylim/25,MRS_str[:-1],font_text)
    print("{}".format(MRS_str))

    #===Set legend===#
    axP.legend(mode_list,prop=font_legend,
            framealpha=0,facecolor='none',ncol=4,numpoints=5,markerscale=3, 
            borderaxespad=0,bbox_to_anchor=(1,1.08),loc=1)
    leg = axP.get_legend()
    index = 0
    # for cur_mode in Plot_Data.keys():
    for legobj in leg.legendHandles:
        legobj.set_linewidth(2)
        legobj.set_color(color_list[index%3])
        index = index + 1
     
    if Show:
        plt.show()
    else:
        file_name = ""
        for cur_mode in mode_list:
            file_name = file_name + "-{}".format(cur_mode)
        plt.savefig(os.path.join(Save_dir,"ZWD-DELTA{}.jpg".format(file_name)),dpi=600)

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
    axP.set_xticks(XlabelSet[1])
    axP.set_xticklabels(XlabelSet[0])
    labels = axP.get_yticklabels() + axP.get_xticklabels()
    [label.set_fontsize(xtick_size) for label in labels]
    [label.set_fontname('Arial') for label in labels]
    axP.set_xlabel('GPS time (hour)',font_label)
    # axP.set_xlabel('Time (YYYY-MM-DD)',font_label)
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

def plot_MultiDay_ZWD_raw(Plot_Data={}, Ylim=0.5, XlabelSet = [], Show=True, Legend = True, Start_hour = 0, Start = [], End = [], End_hour = 24, Save_dir = ""):
    #=== Plot ===#
    figP,axP = plt.subplots(1,1,figsize=(12,6),sharey=True,sharex=True)
    mode_list = []
    index = 0
    for cur_mode in Plot_Data.keys():
        time_np = np.array(Plot_Data[cur_mode]["TIME"])
        mintime,max_time = time_np.min(),time_np.max()
        day_num = math.ceil(max_time / 24)
        while day_num > 0:
            index_plot = (time_np >= Start_hour + 24*(day_num - 1)) & (time_np <= End_hour + 24*(day_num - 1))
            day_num = day_num - 1
            axP.plot(time_np[index_plot],np.array(Plot_Data[cur_mode]["ZWD"])[index_plot],linewidth=2,color = color_list[index%3])
        index = index + 1
        mode_list.append(cur_mode)
    #===Set Label===#
    axP.set_xticks(XlabelSet[1])
    axP.set_xticklabels(XlabelSet[0])
    labels = axP.get_yticklabels() + axP.get_xticklabels()
    [label.set_fontsize(xtick_size) for label in labels]
    [label.set_fontname('Arial') for label in labels]
    # axP.set_xlabel('GPS time (hour)',font_label)
    axP.set_xlabel('Time (YYYY-MM-DD)',font_label)
    axP.set_ylabel('ZWD (mm)',font_label)
    XlabelDate = []
    for cur_hour in XlabelSet[1]:
        doy = tr.ymd2doy(Start[0],Start[1],Start[2],Start[3] + cur_hour,Start[4],Start[5])
        [year,mon,day] = tr.doy2ymd(Start[0],doy)
        XlabelDate.append("{}-{:0>2}-{:0>2}".format(year,mon,day))
    axP.set_xticklabels(XlabelDate)
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
    leg = axP.get_legend()
    index = 0
    # for cur_mode in Plot_Data.keys():
    for legobj in leg.legendHandles:
        legobj.set_linewidth(2)
        legobj.set_color(color_list[index%3])
        index = index + 1
    if Show:
        plt.show()
    else:
        file_name = ""
        for cur_mode in mode_list:
            file_name = file_name + "-{}".format(cur_mode)
        plt.savefig(os.path.join(Save_dir,"ZWD-RAW{}.jpg".format(file_name)),dpi=600)

def plot_GRD_raw(Plot_Data={}, Ylim=0.5, XlabelSet = [], Show=True, Legend = True):
    #=== Plot ===#
    figP,axP = plt.subplots(2,1,figsize=(12,9),sharey=True,sharex=True)
    mode_list = []
    index = 0
    for cur_mode in Plot_Data.keys():
        axP[0].plot(Plot_Data[cur_mode]["TIME"],Plot_Data[cur_mode]["TGN"],linewidth=2,color = color_list[index%3])
        axP[1].plot(Plot_Data[cur_mode]["TIME"],Plot_Data[cur_mode]["TGE"],linewidth=2,color = color_list[index%3])
        index = index + 1
        mode_list.append(cur_mode)
    #===Set Label===#
    axP[1].set_xticks(XlabelSet[1])
    axP[1].set_xticklabels(XlabelSet[0])
    labels = axP[0].get_yticklabels() + axP[0].get_xticklabels() + axP[1].get_yticklabels() + axP[1].get_xticklabels()
    [label.set_fontsize(xtick_size) for label in labels]
    [label.set_fontname('Arial') for label in labels]
    axP[1].set_xlabel('GPS time (hour)',font_label)
    axP[0].set_ylabel('North gradient (mm)',font_label)
    axP[1].set_ylabel('East gradient (mm)',font_label)

    #===Set text===#
    # MRS_str = "RMS:"
    # for cur_mode in Plot_Data.keys():
    #     MRS_str = MRS_str + " {:.1f}mm,".format(np.sqrt(np.mean(np.array(Plot_Data[cur_mode]["ZWD"])**2)))
    # ax_range = axP.axis()
    # axP.text(ax_range[0],ax_range[3]+Ylim/25,MRS_str[:-1],font_text)
    # print("{}".format(MRS_str))

    #===Set legend===#
    axP[0].legend(mode_list,prop=font_legend,
            framealpha=0,facecolor='none',ncol=4,numpoints=5,markerscale=3, 
            borderaxespad=0,bbox_to_anchor=(1,1.15),loc=1) 
    if Show:
        plt.show()

def plot_MultiDay_GRD_raw(Plot_Data={}, Ylim=0.5, XlabelSet = [], Show=True, Legend = True, Start_hour = 0, Start = [], End = [], End_hour = 24, Save_dir = ""):
    #=== Plot ===#
    figP,axP = plt.subplots(2,1,figsize=(12,9),sharey=True,sharex=True)
    mode_list = []
    index = 0
    for cur_mode in Plot_Data.keys():
        time_np = np.array(Plot_Data[cur_mode]["TIME"])
        mintime,max_time = time_np.min(),time_np.max()
        day_num = math.ceil(max_time / 24)
        while day_num > 0:
            index_plot = (time_np >= Start_hour + 24*(day_num - 1)) & (time_np <= End_hour + 24*(day_num - 1))
            day_num = day_num - 1
            axP[0].plot(time_np[index_plot],np.array(Plot_Data[cur_mode]["TGN"])[index_plot],linewidth=2,color = color_list[index%3])
            axP[1].plot(time_np[index_plot],np.array(Plot_Data[cur_mode]["TGE"])[index_plot],linewidth=2,color = color_list[index%3])
        index = index + 1
        mode_list.append(cur_mode)
    #===Set Label===#
    if Ylim != 0:
        axP[0].set_ylim(-Ylim,Ylim)
    axP[1].set_xticks(XlabelSet[1])
    axP[1].set_xticklabels(XlabelSet[0])
    labels = axP[0].get_yticklabels() + axP[0].get_xticklabels() + axP[1].get_yticklabels() + axP[1].get_xticklabels()
    [label.set_fontsize(xtick_size) for label in labels]
    [label.set_fontname('Arial') for label in labels]
    # axP[1].set_xlabel('GPS time (hour)',font_label)
    axP[1].set_xlabel('Time (YYYY-MM-DD)',font_label)
    axP[0].set_ylabel('North gradient (mm)',font_label)
    axP[1].set_ylabel('East gradient (mm)',font_label)
    # Date
    XlabelDate = []
    for cur_hour in XlabelSet[1]:
        doy = tr.ymd2doy(Start[0],Start[1],Start[2],Start[3] + cur_hour,Start[4],Start[5])
        [year,mon,day] = tr.doy2ymd(Start[0],doy)
        XlabelDate.append("{}-{:0>2}-{:0>2}".format(year,mon,day))
    axP[1].set_xticklabels(XlabelDate)
    #===Set legend===#
    axP[0].legend(mode_list,prop=font_legend,
            framealpha=0,facecolor='none',ncol=4,numpoints=5,markerscale=3, 
            borderaxespad=0,bbox_to_anchor=(1,1.15),loc=1) 
    leg = axP[0].get_legend()
    index = 0
    # for cur_mode in Plot_Data.keys():
    for legobj in leg.legendHandles:
        legobj.set_linewidth(2)
        legobj.set_color(color_list[index%3])
        index = index + 1
    if Show:
        plt.show()
    else:
        file_name = ""
        for cur_mode in mode_list:
            file_name = file_name + "-{}".format(cur_mode)
        plt.savefig(os.path.join(Save_dir,"GRD-RAW{}.jpg".format(file_name)),dpi=600)

def plot_GRD_delta(Plot_Data={}, Ylim=0.5, XlabelSet = [], Show=True, Legend = True):
    #=== Plot ===#
    figP,axP = plt.subplots(2,1,figsize=(12,9),sharey=True,sharex=True)
    mode_list = []
    index = 0
    for cur_mode in Plot_Data.keys():
        axP[0].plot(Plot_Data[cur_mode]["TIME"],Plot_Data[cur_mode]["TGN"],linewidth=2,color = color_list[index%3])
        axP[1].plot(Plot_Data[cur_mode]["TIME"],Plot_Data[cur_mode]["TGE"],linewidth=2,color = color_list[index%3])
        index = index + 1
        mode_list.append(cur_mode)
    #===Set Label===#
    if Ylim != 0:
        axP.set_ylim(-Ylim,Ylim)
    axP[1].set_xticks(XlabelSet[1])
    axP[1].set_xticklabels(XlabelSet[0])
    labels = axP[0].get_yticklabels() + axP[0].get_xticklabels() + axP[1].get_yticklabels() + axP[1].get_xticklabels()
    [label.set_fontsize(xtick_size) for label in labels]
    [label.set_fontname('Arial') for label in labels]
    axP[1].set_xlabel('GPS time (hour)',font_label)
    axP[0].set_ylabel('North gradient (mm)',font_label)
    axP[1].set_ylabel('East gradient (mm)',font_label)
    

    # ===Set text===#
    MRS_TGN_str,MRS_TGE_str = "RMS:","RMS:"
    for cur_mode in Plot_Data.keys():
        MRS_TGN_str = MRS_TGN_str + " {:.1f}mm,".format(np.sqrt(np.mean(np.array(Plot_Data[cur_mode]["TGN"])**2)))
        MRS_TGE_str = MRS_TGE_str + " {:.1f}mm,".format(np.sqrt(np.mean(np.array(Plot_Data[cur_mode]["TGE"])**2)))
    ax_range = axP[0].axis()
    axP[0].text(ax_range[0],ax_range[3]+Ylim/25,MRS_TGN_str[:-1],font_text)
    ax_range = axP[1].axis()
    axP[1].text(ax_range[0],ax_range[3]+Ylim/25,MRS_TGE_str[:-1],font_text)
    print("{}: {}".format("TGN",MRS_TGN_str))
    print("{}: {}".format("TGE",MRS_TGE_str))

    #===Set legend===#
    axP[0].legend(mode_list,prop=font_legend,
            framealpha=0,facecolor='none',ncol=4,numpoints=5,markerscale=3, 
            borderaxespad=0,bbox_to_anchor=(1,1.15),loc=1) 
    if Show:
        plt.show()

def plot_MultiDay_GRD_delta(Plot_Data={}, Ylim=0.5, XlabelSet = [], Show=True, Legend = True, Start_hour = 0, Start = [], End = [], End_hour = 24, Save_dir = ""):
    #=== Plot ===#
    figP,axP = plt.subplots(2,1,figsize=(12,9),sharey=True,sharex=True)
    mode_list = []
    index = 0
    for cur_mode in Plot_Data.keys():
        time_np = np.array(Plot_Data[cur_mode]["TIME"])
        mintime,max_time = time_np.min(),time_np.max()
        day_num = math.ceil(max_time / 24)
        while day_num > 0:
            index_plot = (time_np >= Start_hour + 24*(day_num - 1)) & (time_np <= End_hour + 24*(day_num - 1))
            day_num = day_num - 1
            # axP[0].plot(time_np[index_plot],np.array(Plot_Data[cur_mode]["TGN"])[index_plot],linewidth=2,color = color_list[index%3])
            # axP[1].plot(time_np[index_plot],np.array(Plot_Data[cur_mode]["TGE"])[index_plot],linewidth=2,color = color_list[index%3])
            axP[0].scatter(time_np[index_plot],np.array(Plot_Data[cur_mode]["TGN"])[index_plot],color = color_list[index%3],s=15)
            axP[1].scatter(time_np[index_plot],np.array(Plot_Data[cur_mode]["TGE"])[index_plot],color = color_list[index%3],s=15)
            
        index = index + 1
        mode_list.append(cur_mode)
    #===Set Label===#
    if Ylim != 0:
        axP[0].set_ylim(-Ylim,Ylim)
    axP[1].set_xticks(XlabelSet[1])
    axP[1].set_xticklabels(XlabelSet[0])
    labels = axP[0].get_yticklabels() + axP[0].get_xticklabels() + axP[1].get_yticklabels() + axP[1].get_xticklabels()
    [label.set_fontsize(xtick_size) for label in labels]
    [label.set_fontname('Arial') for label in labels]
    # axP[1].set_xlabel('GPS time (hour)',font_label)
    axP[1].set_xlabel('Time (YYYY-MM-DD)',font_label)
    axP[0].set_ylabel('North gradient (mm)',font_label)
    axP[1].set_ylabel('East gradient (mm)',font_label)
    # Date
    XlabelDate = []
    for cur_hour in XlabelSet[1]:
        doy = tr.ymd2doy(Start[0],Start[1],Start[2],Start[3] + cur_hour,Start[4],Start[5])
        [year,mon,day] = tr.doy2ymd(Start[0],doy)
        XlabelDate.append("{}-{:0>2}-{:0>2}".format(year,mon,day))
    axP[0].set_xticklabels(XlabelDate)

    # ===Set text===#
    MRS_TGN_str,MRS_TGE_str = "RMS:","RMS:"
    for cur_mode in Plot_Data.keys():
        time_np = np.array(Plot_Data[cur_mode]["TIME"])
        mintime,max_time = time_np.min(),time_np.max()
        day_num = math.ceil(max_time / 24)
        index_all = []
        while day_num > 0:
            index_all.append((time_np >= Start_hour + 24*(day_num - 1)) & (time_np <= End_hour + 24*(day_num - 1)))
            day_num = day_num - 1
        i = 0
        index_rms = index_all[0]
        while i < len(index_all):
            index_rms = index_rms | index_all[i]
            i = i + 1
        MRS_TGN_str = MRS_TGN_str + " {:.2f}mm,".format(np.sqrt(np.mean(np.array(Plot_Data[cur_mode]["TGN"])[index_rms]**2)))
        MRS_TGE_str = MRS_TGE_str + " {:.2f}mm,".format(np.sqrt(np.mean(np.array(Plot_Data[cur_mode]["TGE"])[index_rms]**2)))
    ax_range = axP[0].axis()
    axP[0].text(ax_range[0],ax_range[3]+Ylim/25,MRS_TGN_str[:-1],font_text)
    ax_range = axP[1].axis()
    axP[1].text(ax_range[0],ax_range[3]+Ylim/25,MRS_TGE_str[:-1],font_text)
    print("{}: {}".format("TGN",MRS_TGN_str))
    print("{}: {}".format("TGE",MRS_TGE_str))
    #===Set legend===#
    axP[0].legend(mode_list,prop=font_legend,
            framealpha=0,facecolor='none',ncol=4,numpoints=5,markerscale=3, 
            borderaxespad=0,bbox_to_anchor=(1,1.15),loc=1)
    leg = axP[0].get_legend()
    index = 0
    # for cur_mode in Plot_Data.keys():
    for legobj in leg.legendHandles:
        legobj.set_linewidth(2)
        legobj.set_color(color_list[index%3])
        index = index + 1 
    if Show:
        plt.show()
    else:
        file_name = ""
        for cur_mode in mode_list:
            file_name = file_name + "-{}".format(cur_mode)
        plt.savefig(os.path.join(Save_dir,"GRD-DELTA{}.jpg".format(file_name)),dpi=600)
        

def statistics(All_Data, Delta_data, Start_time, Duration_time, Reconvergence, Recon_list, Show = True, Save_dir = ""):
    #=== Reconvergence ===#
    # Set
    max_recon_time = 1800
    cont_continue = 10
    # Initialization
    con_ZWD,con_TGN,con_TGE = {},{},{}
    for cur_mode in All_Data.keys():
        if cur_mode not in con_ZWD.keys():
            con_ZWD[cur_mode],con_TGN[cur_mode],con_TGE[cur_mode] = {},{},{}
            for cur_accuracy in Recon_list:
                con_ZWD[cur_mode][cur_accuracy] = []
                con_TGN[cur_mode][cur_accuracy] = []
                con_TGE[cur_mode][cur_accuracy] = []
    # Start reconvergence
    if Reconvergence != 0:
        for cur_mode in All_Data.keys():
            time_np = np.array(All_Data[cur_mode]["TIME"])
            zwd,tgn,tge = np.abs(np.array(All_Data[cur_mode]["ZWD"])),np.abs(np.array(All_Data[cur_mode]["TGN"])),np.abs(np.array(All_Data[cur_mode]["TGE"]))
            cur_time = Start_time[3] * 3600
            # i = 0
            for i in range(int(Duration_time*3600 / Reconvergence)):
                for cur_accuracy in Recon_list:
                    cur_time = Start_time[3] * 3600 + i * Reconvergence
                    con_zwd_num,con_tgn_num,con_tge_num = 0,0,0
                    while cur_time < Start_time[3] * 3600 + (i+1) * Reconvergence:
                        find_time = time_np[time_np == cur_time/3600]
                        find_time_index = time_np == cur_time/3600
                        if find_time.size < 1:
                            cur_time = cur_time + Delta_data
                            continue
                        # ZWD
                        if zwd[find_time_index] < cur_accuracy:
                            if con_zwd_num < cont_continue:
                                con_zwd_num = con_zwd_num + 1
                        elif con_zwd_num < cont_continue:
                            con_zwd_num = 0
                        if con_zwd_num == cont_continue:
                            con_ZWD[cur_mode][cur_accuracy].append(cur_time - (Start_time[3] * 3600 + i * Reconvergence) - Delta_data * (cont_continue-1))
                            con_zwd_num = 9999999
                        # TGN
                        if tgn[find_time_index] < cur_accuracy:
                            if con_tgn_num < cont_continue:
                                con_tgn_num = con_tgn_num + 1
                        elif con_tgn_num < cont_continue:
                            con_tgn_num = 0
                        if con_tgn_num == cont_continue:
                            con_TGN[cur_mode][cur_accuracy].append(cur_time - (Start_time[3] * 3600 + i * Reconvergence) - Delta_data * (cont_continue-1))
                            con_tgn_num = 9999999
                        # TGE
                        if tge[find_time_index] < cur_accuracy:
                            if con_tge_num < cont_continue:
                                con_tge_num = con_tge_num + 1
                        elif con_tge_num < cont_continue:
                            con_tge_num = 0
                        if con_tge_num == cont_continue:
                            con_TGE[cur_mode][cur_accuracy].append(cur_time - (Start_time[3] * 3600 + i * Reconvergence) - Delta_data * (cont_continue-1))
                            con_tge_num = 9999999
                        
                        if cur_time - (Start_time[3] * 3600 + i * Reconvergence) > max_recon_time:
                            if con_zwd_num != 9999999:
                                con_ZWD[cur_mode][cur_accuracy].append(max_recon_time)
                            if con_tgn_num != 9999999:
                                con_TGN[cur_mode][cur_accuracy].append(max_recon_time)
                            if con_tge_num != 9999999:
                                con_TGE[cur_mode][cur_accuracy].append(max_recon_time)
                            break
                        cur_time = cur_time + Delta_data
    # Print Revonvergence
    for cur_accuracy in Recon_list:
        print("{:>2}mm-RECONVERGENCE".format(cur_accuracy))
        print("{:<15}".format("Mode") + "{:>7}".format("ZWD(s)") + \
                                         "{:>14}".format("TGN(s)") + \
                                         "{:>14}".format("TGE(s)"))
        for cur_mode in con_ZWD.keys():
            Str_temp = "{:<15}".format(cur_mode) + "{:>7}".format(int(np.mean(con_ZWD[cur_mode][cur_accuracy]))) + \
                                                "{:>14}".format(int(np.mean(con_TGN[cur_mode][cur_accuracy]))) + \
                                                "{:>14}".format(int(np.mean(con_TGE[cur_mode][cur_accuracy])))
            print(Str_temp)
            # print(con_ZWD[cur_mode][cur_accuracy])
        # for cur_mode in Static_print.keys():


def Plot_timeseries_zwd(File_info=[],Start=[],End=[],Plot_type=[],Ylim=0.5,Save_dir="",Fixed = False,Show=True,All=False,Time_type = "GPST",Delta_xlabel = 1,Delay_model = 0,Legend = False,Sigma=3,Signum=0):
    all_data,data_raw,data_ref = {},{},{}
    [start_week,start_sow] = tr.ymd2gpst(Start[0],Start[1],Start[2],Start[3],Start[4],Start[5])
    [end_week,end_sow] = tr.ymd2gpst(End[0],End[1],End[2],End[3],End[4],End[5])
    duration_time = ((end_week-start_week)*604800+(end_sow - start_sow))/3600
    #=== load data ===#
    if "DELTA" in Plot_type:
        for i in range(len(File_info)):
            file_list1 = File_info[i][0].split(",")
            for cur_file in file_list1:
                load_data(cur_file, data_raw)
            file_list2 = File_info[i][1].split(",")
            for cur_file in file_list2:
                load_data(cur_file, data_ref)
            all_data[File_info[i][2]] = compare_zwd(data_raw,data_ref)
            data_ref,data_raw={},{}
    elif "RAW" in Plot_type:
        for i in range(len(File_info)):
            file_list1 = File_info[i][0].split(",")
            if File_info[i][1] not in all_data.keys():
                all_data[File_info[i][1]] = {}
            for cur_file in file_list1:
                 load_data(cur_file,all_data[File_info[i][1]])
    
    #=== convert data ===#
    [XLabel,XTick,cov_time,begT,LastT]=glv.xtick(Time_type,Start[0],Start[1],Start[2],Start[3]+Start[4]/60,duration_time,Delta_xlabel)
    type_list = ["ZWD","TGN","TGE"]
    PLOT_ALL, PLOT_RAW = {},{}
    for cur_mode in all_data.keys():
        for cur_time in all_data[cur_mode].keys():
            plot_time = (cur_time - cov_time) / 3600
            # if (cur_time - start_sow) % 300 != 0:
            #     continue
            if ((plot_time >= Start[3] and plot_time <= (Start[3]+duration_time)) or All):
                if Fixed and all_data[cur_mode][cur_time]["AMB"] != 1:
                    continue
                if cur_mode not in PLOT_ALL.keys():
                    PLOT_ALL[cur_mode],PLOT_RAW[cur_mode] = {},{}
                    PLOT_ALL[cur_mode]["TIME"],PLOT_RAW[cur_mode]["TIME"] = [],[]
                    for cur_type in type_list:
                        PLOT_ALL[cur_mode][cur_type],PLOT_RAW[cur_mode][cur_type] = [],[]
                PLOT_ALL[cur_mode]["TIME"].append(plot_time)
                PLOT_RAW[cur_mode]["TIME"].append(plot_time)
                for cur_type in type_list:
                    PLOT_ALL[cur_mode][cur_type].append(all_data[cur_mode][cur_time][cur_type])
                    PLOT_RAW[cur_mode][cur_type].append(all_data[cur_mode][cur_time][cur_type])
    
    #=== plot ===#
    if Plot_type == "ZWD_DELTA":
        plot_ZWD_delta(Plot_Data=PLOT_ALL, Ylim=Ylim, XlabelSet = [XLabel,XTick], Show=Show)
    elif Plot_type == "ZWD_RAW":
        plot_ZWD_raw(Plot_Data=PLOT_ALL, Ylim=Ylim, XlabelSet = [XLabel,XTick], Show=Show)
    elif Plot_type == "GRD_RAW":
        plot_GRD_raw(Plot_Data=PLOT_ALL, Ylim=Ylim, XlabelSet = [XLabel,XTick], Show=Show)
    elif Plot_type == "GRD_DELTA":
        plot_GRD_delta(Plot_Data=PLOT_ALL, Ylim=Ylim, XlabelSet = [XLabel,XTick], Show=Show)

def plot_percent_ZWD_delta(all_data = {},Ylim = 0.0, Show=True, Reconvergence = 3600, Percent = 0.9, Delta_data = 30 , Save_dir = ""):
    data_sort = {}
    
    #=== Initialization ===#
    for cur_mode in all_data.keys():
        plot_time = []
        if cur_mode not in data_sort.keys():
            data_sort[cur_mode] = {}
        cur_time = 0
        while cur_time < Reconvergence:
            data_sort[cur_mode][cur_time] = []
            plot_time.append(cur_time)
            cur_time = cur_time + Delta_data
    #=== Sort Data ===#
    for cur_mode in all_data.keys():
        for cur_time in all_data[cur_mode].keys():
            if cur_time%3600 == 0:
                cur_time_find = 0
                while cur_time_find < Reconvergence:
                    if (cur_time_find + cur_time) in all_data[cur_mode].keys():
                        data_sort[cur_mode][cur_time_find].append(abs(all_data[cur_mode][cur_time_find + cur_time]["ZWD"]))
                    cur_time_find = cur_time_find + Delta_data
    Plot_data = {"TIME":{},"DATA":{}}
    for cur_mode in data_sort.keys():
        if cur_mode not in Plot_data["TIME"].keys():
            Plot_data["TIME"][cur_mode],Plot_data["DATA"][cur_mode] = [],[]
        for cur_time in data_sort[cur_mode].keys():
            temp_np = np.array(data_sort[cur_mode][cur_time])
            Plot_data["TIME"][cur_mode].append(cur_time/60)
            temp_np.sort()
            if Percent != 0:
                index = math.floor(temp_np.size * Percent)
                Plot_data["DATA"][cur_mode].append(temp_np[index]/10)
            else:
                Plot_data["DATA"][cur_mode].append(np.mean(temp_np)/10)
    #=== Plot ===#
    figP,axP = plt.subplots(1,1,figsize=(8,7),sharey=True,sharex=True)
    mode_list = []
    index = 0
    for cur_mode in Plot_data["TIME"].keys():
        axP.plot(Plot_data["TIME"][cur_mode],Plot_data["DATA"][cur_mode],linewidth=2,color = color_list[index%3])
        index = index + 1
        mode_list.append(cur_mode)
    
    # Zoom
    axins1 = axP.inset_axes(((1/3,1/2,0.5,0.4)))
    index = 0
    for cur_mode in Plot_data["TIME"].keys():
        index_plot = (np.array(Plot_data["TIME"][cur_mode]) > 0) & (np.array(Plot_data["TIME"][cur_mode]) <= 5)
        axins1.plot(np.array(Plot_data["TIME"][cur_mode])[index_plot],np.array(Plot_data["DATA"][cur_mode])[index_plot],linewidth=2,color = color_list[index%3])
        index = index + 1
    mark_inset(axP,axins1,loc1=4,loc2=2,fc = "none",ec="k",lw=1,ls = '--')
    # axins2 = axP.inset_axes(((1/1.8,1/5,0.4,0.3)))
    # index = 0
    # for cur_mode in Plot_data["TIME"].keys():
    #     index_plot = (np.array(Plot_data["TIME"][cur_mode]) >= 30) & (np.array(Plot_data["TIME"][cur_mode]) <= 60)
    #     axins2.plot(np.array(Plot_data["TIME"][cur_mode])[index_plot],np.array(Plot_data["DATA"][cur_mode])[index_plot],linewidth=2,color = color_list[index%3])
    #     index = index + 1
    # mark_inset(axP,axins2,loc1=4,loc2=2,fc = "none",ec="k",lw=1,ls = '--')
    #===Set Label===#
    axP.set_xticks([0,10,20,30,40,50,60])
    axP.set_xticklabels([0,10,20,30,40,50,60])
    labels = axP.get_yticklabels() + axP.get_xticklabels() + axins1.get_yticklabels() + axins1.get_xticklabels()# + axins2.get_yticklabels() + axins2.get_xticklabels()
    if Ylim != 0:
        axP.set_ylim(0,Ylim)
    [label.set_fontsize(xtick_size) for label in labels]
    [label.set_fontname('Arial') for label in labels]
    axP.set_xlabel('Time (mins)',font_label)
    axP.set_ylabel('ZWD errors (cm)',font_label)
    #===Set legend===#
    axP.legend(mode_list,prop=font_legend,
            framealpha=0,facecolor='none',ncol=4,numpoints=5,markerscale=3, 
            borderaxespad=0,bbox_to_anchor=(1,1.08),loc=1)
    if Show:
        plt.show()
    else:
        file_name = ""
        for cur_mode in mode_list:
            file_name = file_name + "-{}".format(cur_mode)
        plt.savefig(os.path.join(Save_dir,"ZWD-PERCENT{}.jpg".format(file_name)),dpi=600)

def plot_box_ZWD_delta(all_data = {},Ylim = 0.0, Show=True, Reconvergence = 3600, Percent = 0.9, Delta_data = 30 , Save_dir = ""):
    data_sort = {}
    mode_list = {}
    #=== Initialization ===#
    for cur_mode in all_data.keys():
        plot_time = []
        if cur_mode not in data_sort.keys():
            data_sort[cur_mode] = {}
        cur_time = 0
        while cur_time < Reconvergence:
            data_sort[cur_mode][cur_time] = []
            plot_time.append(cur_time)
            cur_time = cur_time + Delta_data
    #=== Sort Data ===#
    for cur_mode in all_data.keys():
        for cur_time in all_data[cur_mode].keys():
            if cur_time%3600 == 0:
                cur_time_find = 0
                while cur_time_find < Reconvergence:
                    if (cur_time_find + cur_time) in all_data[cur_mode].keys():
                        data_sort[cur_mode][cur_time_find].append(abs(all_data[cur_mode][cur_time_find + cur_time]["ZWD"]))
                    cur_time_find = cur_time_find + Delta_data
    Plot_data = {"TIME":{},"DATA":{}}
    delta_sec = 300
    for cur_mode in data_sort.keys():
        if cur_mode not in Plot_data["TIME"].keys():
            Plot_data["TIME"][cur_mode],Plot_data["DATA"][cur_mode] = [],[]
        for cur_time in data_sort[cur_mode].keys():
            # if cur_time == 0:
            #     continue
            if cur_time%delta_sec == 0:
                cur_time_find = cur_time
                Plot_data["DATA"][cur_mode].append([])
                while cur_time_find < cur_time + delta_sec:
                    # if cur_time_find == 0:
                    #     cur_time_find = cur_time_find+30
                    #     continue
                    if cur_time_find in data_sort[cur_mode].keys():
                        for i in range(len(data_sort[cur_mode][cur_time_find])):
                            Plot_data["DATA"][cur_mode][int(cur_time/delta_sec)].append(data_sort[cur_mode][cur_time_find][i])
                        cur_time_find = cur_time_find+30
    #=== Plot ===#
    figP,axP = plt.subplots(1,1,figsize=(14,6),sharey=True,sharex=True)
    index = 0
    multi_plot = []
    for cur_mode in Plot_data["TIME"].keys():
        mode_list[cur_mode] = index
        index = index + 1
        for i in range(len(Plot_data["DATA"][cur_mode])):
            multi_plot.append([])
    for cur_mode in mode_list.keys():
         for i in range(len(Plot_data["DATA"][cur_mode])):
             multi_plot[mode_list[cur_mode] + 2*i] = Plot_data["DATA"][cur_mode][i]
    x_labels = []
    for i in range(1,len(multi_plot)+1):
        if i%2==0:
            x_labels.append(i-0.25)
        else:
            x_labels.append(i+0.25)
    box = axP.boxplot(multi_plot,positions = x_labels,showfliers = False,patch_artist = True, widths = 0.5)
    #=== Set background ===#
    # for i in range(int(len(multi_plot)/4)):
    #     axP.axvspan(ymin = 0,ymax = 1,xmin = 2.5+4*i,xmax = 2.5+4*i+2,alpha = 0.3,color = "gray")
    #=== Set Color ===#
    index = 0
    for boxes,medians in zip(box['boxes'],box['medians']):
        if index%2==0:
            color_idnex = 0
        else:
            color_idnex = 1
        boxes.set_facecolor(color_list[color_idnex])
        medians.set_color("k")
        index = index + 1

    #===Set Label===#
    # axP.set_ylim(0,300)
    x_tick_temp,x_label_temp = 1.5,0
    x_tick_list = []
    x_tick_label = []
    for i in range(int(len(multi_plot)/2)):
        x_tick_list.append(x_tick_temp)
        x_tick_label.append("[{:0>2},{:0>2})".format(x_label_temp,int(x_label_temp+delta_sec/60)))
        x_tick_temp = x_tick_temp + 2
        x_label_temp = x_label_temp+5
    axP.set_xticks(x_tick_list)
    axP.set_xticklabels(x_tick_label)
    axP.grid(axis = 'x')
    labels = axP.get_yticklabels() + axP.get_xticklabels()
    # if Ylim != 0:
    #     axP.set_ylim(0,Ylim)
    [label.set_fontsize(xtick_size) for label in labels]
    [label.set_fontname('Arial') for label in labels]
    axP.set_xlabel('Time range (mins)',font_label)
    axP.set_ylabel('ZWD errors (cm)',font_label)
    # #===Set legend===#  
    handle_list = []
    for index in range(2):
        handle_list.append(Rectangle((0,0),40,14,color = (color_list[index%3])))
        index = index + 1
    leg = axP.legend(handles = handle_list,labels = mode_list,prop=font_legend,
                framealpha=0,facecolor='none',ncol=4,numpoints=5,markerscale=3, 
                borderaxespad=0,bbox_to_anchor=(1,1.08),loc=1)
    #=== Zoom ===#
    # axins1 = axP.inset_axes(((1/4,1/3,0.7,0.4)))
    # index = 0
    # box = axins1.boxplot(multi_plot[10:],positions = x_labels[10:],showfliers = False,patch_artist = True, widths = 0.5)
    # index = 0
    # for boxes,medians in zip(box['boxes'],box['medians']):
    #     if index%2==0:
    #         color_idnex = 0
    #     else:
    #         color_idnex = 1
    #     boxes.set_facecolor(color_list[color_idnex])
    #     medians.set_color("k")
    #     index = index + 1
    # axins1.set_xticks(x_tick_list[5:])
    # axins1.set_xticklabels(x_tick_label[5:])
    # mark_inset(axP,axins1,loc1=3,loc2=1,fc = "none",ec="k",lw=1,ls = '--')
    # labels = axins1.get_yticklabels() + axins1.get_xticklabels()
    # [label.set_fontsize(xtick_size) for label in labels]
    # [label.set_fontname('Arial') for label in labels]
    if Show:
        plt.show()
    else:
        file_name = ""
        for cur_mode in mode_list:
            file_name = file_name + "-{}".format(cur_mode)
        plt.savefig(os.path.join(Save_dir,"ZWD-BOX-ZOOM{}.jpg".format(file_name)),dpi=600)

def plot_qq_ZWD_delta(all_data = {},Ylim = 0.0, Show=True, Reconvergence = 3600, Percent = 0.9, Delta_data = 30 , Save_dir = ""):
    num_plot = len(all_data)
    figP,axP = plt.subplots(1,num_plot,figsize=(14,6),sharey=True,sharex=True)
    index = 0
    for cur_mode in all_data.keys():
        axP[index].scatter(all_data[cur_mode]['ZWD'][0],all_data[cur_mode]['ZWD'][1])
        pccs = np.corrcoef(np.array(all_data[cur_mode]['ZWD'][0]),np.array(all_data[cur_mode]['ZWD'][1]))
        index = index + 1
        print(cur_mode)
        print(pccs)
    if Show:
        plt.show()
    # else:
        # file_name = ""
        # for cur_mode in mode_list:
        #     file_name = file_name + "-{}".format(cur_mode)
        # plt.savefig(os.path.join(Save_dir,"ZWD-BOX-ZOOM{}.jpg".format(file_name)),dpi=600)

def Plot_MultiDay_timeseries_zwd(File_info=[],Start=[],End=[],Plot_type=[],Ylim=0.5,Save_dir="",Fixed = False,Show=True,All=False,Time_type = "GPST",Delta_xlabel = 1,Delay_model = 0,Legend = False,Sigma=3,Signum=0,Start_hour = 0,End_hour = 0,Inter_zpd = False, Reconvergence = 3600, Recon_list = [], Percent = 0.9):
    all_data,data_raw,data_ref = {},{},{}
    [start_week,start_sow] = tr.ymd2gpst(Start[0],Start[1],Start[2],Start[3],Start[4],Start[5])
    [end_week,end_sow] = tr.ymd2gpst(End[0],End[1],End[2],End[3],End[4],End[5])
    if Start_hour == 0 and End_hour == 0:
        Start_hour,End_hour = Start[3],End[3]
    duration_time = ((end_week-start_week)*604800+(end_sow - start_sow))/3600
    #=== load data ===#
    if "DELTA" in Plot_type:
        for i in range(len(File_info)):
            file_list1 = File_info[i][0].split(",")
            for cur_file in file_list1:
                load_data(cur_file, data_raw, Inter_zpd)
            file_list2 = File_info[i][1].split(",")
            for cur_file in file_list2:
                load_data(cur_file, data_ref, Inter_zpd)
            all_data[File_info[i][2]] = compare_zwd(data_raw,data_ref)
            data_ref,data_raw={},{}
    elif "RAW" in Plot_type:
        for i in range(len(File_info)):
            if File_info[i][1] not in all_data.keys():
                all_data[File_info[i][1]] = {}
            file_list1 = File_info[i][0].split(",")
            for cur_file in file_list1:
                 load_data(cur_file,all_data[File_info[i][1]], Inter_zpd)
    
    #=== convert data ===#
    [XLabel,XTick,cov_time,begT,LastT]=glv.xtick(Time_type,Start[0],Start[1],Start[2],Start[3]+Start[4]/60,duration_time,Delta_xlabel)
    type_list = ["ZWD","TGN","TGE"]
    PLOT_ALL, PLOT_RAW = {},{}
    for cur_mode in all_data.keys():
        for cur_time in all_data[cur_mode].keys():
            plot_time = (cur_time - cov_time) / 3600
            # if (cur_time - start_sow) % 300 != 0:
            #     continue
            if ((plot_time >= Start[3] and plot_time <= (Start[3]+duration_time)) or All):
                if Fixed and all_data[cur_mode][cur_time]["AMB"] != 1:
                    continue
                if cur_mode not in PLOT_ALL.keys():
                    PLOT_ALL[cur_mode],PLOT_RAW[cur_mode] = {},{}
                    PLOT_ALL[cur_mode]["TIME"],PLOT_RAW[cur_mode]["TIME"] = [],[]
                    for cur_type in type_list:
                        PLOT_ALL[cur_mode][cur_type],PLOT_RAW[cur_mode][cur_type] = [],[]
                PLOT_ALL[cur_mode]["TIME"].append(plot_time)
                PLOT_RAW[cur_mode]["TIME"].append(plot_time)
                for cur_type in type_list:
                    PLOT_ALL[cur_mode][cur_type].append(all_data[cur_mode][cur_time][cur_type])
                    PLOT_RAW[cur_mode][cur_type].append(all_data[cur_mode][cur_time][cur_type])
    if "DELTA" in Plot_type and Reconvergence != 0:
        statistics(PLOT_ALL, 30, Start, duration_time, Reconvergence, Recon_list, Show, Save_dir)
    #=== plot ===#
    if Plot_type == "ZWD_DELTA":
        plot_MultiDay_ZWD_delta(Plot_Data=PLOT_ALL, Ylim=Ylim, XlabelSet = [XLabel,XTick], Show=Show, Start_hour=Start_hour, End_hour = End_hour, Start = Start, End = End, Save_dir = Save_dir)
    elif Plot_type == "ZWD_RAW":
        plot_MultiDay_ZWD_raw(Plot_Data=PLOT_ALL, Ylim=Ylim, XlabelSet = [XLabel,XTick], Show=Show, Start_hour=Start_hour, End_hour = End_hour, Start = Start, End = End, Save_dir = Save_dir)
    elif Plot_type == "GRD_RAW":
        plot_MultiDay_GRD_raw(Plot_Data=PLOT_ALL, Ylim=Ylim, XlabelSet = [XLabel,XTick], Show=Show, Start_hour=Start_hour, End_hour = End_hour, Start = Start, End = End, Save_dir = Save_dir)
    elif Plot_type == "GRD_DELTA":
        plot_MultiDay_GRD_delta(Plot_Data=PLOT_ALL, Ylim=Ylim, XlabelSet = [XLabel,XTick], Show=Show, Start_hour=Start_hour, End_hour = End_hour, Start = Start, End = End, Save_dir = Save_dir)

def Plot_MultiDay_percent_zwd(File_info=[],Start=[],End=[],Plot_type=[],Ylim=0.5,Save_dir="",Fixed = False,Show=True,All=False,Time_type = "GPST",Delta_xlabel = 1,Delay_model = 0,Legend = False,Sigma=3,Signum=0,Start_hour = 0,End_hour = 0,Inter_zpd = False, Reconvergence = 3600, Recon_list = [], Percent = 0.9):
    all_data,data_raw,data_ref = {},{},{}
    [start_week,start_sow] = tr.ymd2gpst(Start[0],Start[1],Start[2],Start[3],Start[4],Start[5])
    [end_week,end_sow] = tr.ymd2gpst(End[0],End[1],End[2],End[3],End[4],End[5])
    if Start_hour == 0 and End_hour == 0:
        Start_hour,End_hour = Start[3],End[3]
    duration_time = ((end_week-start_week)*604800+(end_sow - start_sow))/3600
    #=== load data ===#
    for i in range(len(File_info)):
        file_list1 = File_info[i][0].split(",")
        for cur_file in file_list1:
            load_data(cur_file, data_raw, Inter_zpd)
        file_list2 = File_info[i][1].split(",")
        for cur_file in file_list2:
            load_data(cur_file, data_ref, Inter_zpd)
        all_data[File_info[i][2]] = compare_zwd(data_raw,data_ref)
        data_ref,data_raw={},{}
    
    #=== convert data ===#
    [XLabel,XTick,cov_time,begT,LastT]=glv.xtick(Time_type,Start[0],Start[1],Start[2],Start[3]+Start[4]/60,duration_time,Delta_xlabel)
    type_list = ["ZWD","TGN","TGE"]
    PLOT_ALL, PLOT_RAW = {},{}
    for cur_mode in all_data.keys():
        for cur_time in all_data[cur_mode].keys():
            plot_time = (cur_time - cov_time) / 3600
            # if (cur_time - start_sow) % 300 != 0:
            #     continue
            if ((plot_time >= Start[3] and plot_time <= (Start[3]+duration_time)) or All):
                if Fixed and all_data[cur_mode][cur_time]["AMB"] != 1:
                    continue
                if cur_mode not in PLOT_ALL.keys():
                    PLOT_ALL[cur_mode],PLOT_RAW[cur_mode] = {},{}
                    PLOT_ALL[cur_mode]["TIME"],PLOT_RAW[cur_mode]["TIME"] = [],[]
                    for cur_type in type_list:
                        PLOT_ALL[cur_mode][cur_type],PLOT_RAW[cur_mode][cur_type] = [],[]
                PLOT_ALL[cur_mode]["TIME"].append(plot_time)
                PLOT_RAW[cur_mode]["TIME"].append(plot_time)
                for cur_type in type_list:
                    PLOT_ALL[cur_mode][cur_type].append(all_data[cur_mode][cur_time][cur_type])
                    PLOT_RAW[cur_mode][cur_type].append(all_data[cur_mode][cur_time][cur_type])
    if Reconvergence != 0:
        statistics(PLOT_ALL, 30, Start, duration_time, Reconvergence, Recon_list, Show, Save_dir)
    #=== plot ===#
    if Plot_type == "ZWD_DELTA_PERCENT":
        plot_percent_ZWD_delta(all_data = all_data,Ylim = Ylim, Show=Show, Reconvergence = Reconvergence, Percent = Percent, Save_dir = Save_dir)
    elif Plot_type == "ZWD_DELTA_BOX":
        plot_box_ZWD_delta(all_data = all_data,Ylim = Ylim, Show=Show, Reconvergence = Reconvergence, Percent = Percent, Save_dir = Save_dir)
    elif Plot_type == "ZWD_DELTA_QQ":
        plot_qq_ZWD_delta(all_data = all_data,Ylim = Ylim, Show=Show, Reconvergence = Reconvergence, Percent = Percent, Save_dir = Save_dir)

def Plot_MultiDay_qq_zwd(File_info=[],Start=[],End=[],Plot_type=[],Ylim=0.5,Save_dir="",Fixed = False,Show=True,All=False,Time_type = "GPST",Delta_xlabel = 1,Delay_model = 0,Legend = False,Sigma=3,Signum=0,Start_hour = 0,End_hour = 0,Inter_zpd = False, Reconvergence = 3600, Recon_list = [], Percent = 0.9):
    all_data,data_raw,data_ref = {},{},{}
    [start_week,start_sow] = tr.ymd2gpst(Start[0],Start[1],Start[2],Start[3],Start[4],Start[5])
    [end_week,end_sow] = tr.ymd2gpst(End[0],End[1],End[2],End[3],End[4],End[5])
    if Start_hour == 0 and End_hour == 0:
        Start_hour,End_hour = Start[3],End[3]
    duration_time = ((end_week-start_week)*604800+(end_sow - start_sow))/3600
    #=== load data ===#
    for i in range(len(File_info)):
        if File_info[i][2] not in all_data.keys():
            all_data[File_info[i][2]] = {}
        file_list1 = File_info[i][0].split(",")
        for cur_file in file_list1:
            load_data(cur_file, data_raw, Inter_zpd)
        file_list2 = File_info[i][1].split(",")
        for cur_file in file_list2:
            load_data(cur_file, data_ref, Inter_zpd)
        all_data[File_info[i][2]][0] = data_raw
        all_data[File_info[i][2]][1] = data_ref
        data_ref,data_raw={},{}
    #=== convert data ===#
    [XLabel,XTick,cov_time,begT,LastT]=glv.xtick(Time_type,Start[0],Start[1],Start[2],Start[3]+Start[4]/60,duration_time,Delta_xlabel)
    type_list = ["ZWD","TGN","TGE"]
    PLOT_ALL, PLOT_RAW = {},{}
    for cur_mode in all_data.keys():
        for cur_time in all_data[cur_mode][0].keys():
            if cur_time not in all_data[cur_mode][1].keys():
                continue
            plot_time = (cur_time - cov_time) / 3600
            cur_hour_in_day = plot_time
            while cur_hour_in_day >24:
                cur_hour_in_day = cur_hour_in_day - 24
            if cur_hour_in_day < Start_hour or cur_hour_in_day > End_hour:
                continue
            if ((plot_time >= Start[3] and plot_time <= (Start[3]+duration_time)) or All):
                if Fixed and all_data[cur_mode][cur_time]["AMB"] != 1:
                    continue
                if cur_mode not in PLOT_ALL.keys():
                    PLOT_ALL[cur_mode],PLOT_RAW[cur_mode] = {},{}
                    for cur_type in type_list:
                        PLOT_ALL[cur_mode][cur_type],PLOT_RAW[cur_mode][cur_type] = {},{}
                        PLOT_ALL[cur_mode][cur_type][0],PLOT_RAW[cur_mode][cur_type][0] = [],[]
                        PLOT_ALL[cur_mode][cur_type][1],PLOT_RAW[cur_mode][cur_type][1] = [],[]
                for cur_type in type_list:
                    PLOT_ALL[cur_mode][cur_type][0].append(all_data[cur_mode][0][cur_time][cur_type])
                    PLOT_ALL[cur_mode][cur_type][1].append(all_data[cur_mode][1][cur_time][cur_type])
                    PLOT_RAW[cur_mode][cur_type][0].append(all_data[cur_mode][0][cur_time][cur_type])
                    PLOT_RAW[cur_mode][cur_type][1].append(all_data[cur_mode][1][cur_time][cur_type])
    #=== plot ===#
    if Plot_type == "ZWD_DELTA_QQ":
        plot_qq_ZWD_delta(all_data = PLOT_ALL,Ylim = Ylim, Show=Show, Reconvergence = Reconvergence, Percent = Percent, Save_dir = Save_dir)