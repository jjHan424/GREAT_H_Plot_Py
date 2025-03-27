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
font_tick = {'family' : 'Arial', 'weight' : 300, 'size' : 20}
font_legend = {'family' : 'Arial', 'weight' : 300, 'size' : 20}
# font_legend = {'family' : 'Times New Roman', 'weight' : 600, 'size' : 15}
font_text = {'family' : 'Arial','weight' : 300,'size'   : 20}
xtick_size = 20
color_list = ["#0099E5","#34BF49","#FF4C4C"] #Blue #Green # Red ##f2af00 Yellow
# color_list = ["#0085c3","#7ab800","#71c6c1","#dc5034","#009bbb",
#               "#b7295a","#6e2585","#f2af00","#5482ab","#ce1126",
#               "#444444","#eeeeee"]

def loaddata_Kp(File_name,Start_gpst = [0,0]):
    all_data = {}
    with open(File_name,'rt') as f:
        for line in f:
            value_blank = line.split()
            if "|" not in line:
                value_ymd = value_blank[0].split("-")
                value_hms = value_blank[1].split(":")
                [cur_gpst_week,cur_gpst_sow] = tr.ymd2gpst(float(value_ymd[0]),float(value_ymd[1]),float(value_ymd[2]),float(value_hms[0]),float(value_hms[1]),float(value_hms[2]))
                cur_time = ((cur_gpst_week-Start_gpst[0])*7*24*3600 + (cur_gpst_sow - Start_gpst[1])) / 3600
                if cur_time not in all_data.keys():
                    all_data[cur_time] = []
                if "-" in value_blank[3]:
                    Kp = float(value_blank[3][0]) - 1/3
                elif "+" in value_blank[3]:
                    Kp = float(value_blank[3][0]) + 1/3
                elif "o" in value_blank[3]:
                    Kp = float(value_blank[3][0])
                all_data[cur_time] = [Kp,float(value_blank[4])]
    return all_data

def loaddata_Dst(File_name,Start_gpst = [0,0]):
    all_data = {}
    with open(File_name,'rt') as f:
        for line in f:
            value_blank = line.split()
            if "|" not in line:
                value_ymd = value_blank[0].split("-")
                value_hms = value_blank[1].split(":")
                [cur_gpst_week,cur_gpst_sow] = tr.ymd2gpst(float(value_ymd[0]),float(value_ymd[1]),float(value_ymd[2]),float(value_hms[0]),float(value_hms[1]),float(value_hms[2]))
                cur_time = ((cur_gpst_week-Start_gpst[0])*7*24*3600 + (cur_gpst_sow - Start_gpst[1])) / 3600
                all_data[cur_time] = float(value_blank[3])
    return all_data

def load_data(File_info,Start_gpst = [0,0]):
    if File_info[0] == "Kp":
        all_data = loaddata_Kp(File_info[1],Start_gpst)
    elif File_info[0] == "Dst":
        all_data = loaddata_Dst(File_info[1],Start_gpst)
    return all_data

def plot_Kp_ap_Dst(PLOT_ALL,Start,End,Show):
    #=== Plot ===#
    figP,axP = plt.subplots(3,1,figsize=(12,10),sharey=False,sharex=True)
    axP[0].bar(PLOT_ALL["Kp-TIME"],PLOT_ALL["Kp"])
    axP[1].bar(PLOT_ALL["ap-TIME"],PLOT_ALL["ap"])
    axP[2].plot(PLOT_ALL["Dst-TIME"],PLOT_ALL["Dst"])
    if Show:
        plt.show()

def plot_Kp_Dst(PLOT_ALL,Start,End,Show):
    #=== Plot ===#
    figP,axP = plt.subplots(2,1,figsize=(12,9),sharey=False,sharex=True)
    #Plot Kp 56 789
    Kp_numpy = np.array(PLOT_ALL["Kp"])
    index_89 = Kp_numpy >= 8-1/3
    index_7 = (Kp_numpy >= 7-1/3) & (Kp_numpy <= 7+1/3)
    index_4 = Kp_numpy < 5-1/3
    index_5 = Kp_numpy>=5-1/3
    index_6 = Kp_numpy<=6+1/3
    index_56 = index_5 & index_6
    axP[0].scatter(np.array(PLOT_ALL["Kp-TIME"])[index_4],Kp_numpy[index_4],color = "#34BF49",s=7)
    axP[0].scatter(np.array(PLOT_ALL["Kp-TIME"])[index_56],Kp_numpy[index_56],color = "#FFD700",s=7)
    axP[0].scatter(np.array(PLOT_ALL["Kp-TIME"])[index_7],Kp_numpy[index_7],color = "#FF8C00",s=7)
    axP[0].scatter(np.array(PLOT_ALL["Kp-TIME"])[index_89],Kp_numpy[index_89],color = "#FF4C4C",s=7)
    #Quite
    Dst_numpy = np.array(PLOT_ALL["Dst"])
    index_0 = Dst_numpy > -30
    cur_time = np.array(PLOT_ALL["Dst-TIME"])[index_0]
    cur_time_diff = np.diff(cur_time)
    index_time = cur_time_diff != 1
    x,y = [],[]
    i=0
    for cur_value in index_time:
        if cur_value == False:
            x.append(cur_time[i])
            y.append(Dst_numpy[index_0][i])
        else:
            # x.append(cur_time[i])
            # y.append(Dst_numpy[index_0][i])
            axP[1].scatter(x,y,color = "#34BF49",s=5)
            x,y = [],[]
        i = i+1
    if len(x) != 0:
        axP[1].scatter(x,y,color = "#34BF49",s=5)
    #moderate
    index_0 = (Dst_numpy >= -100) & (Dst_numpy < -30)
    cur_time = np.array(PLOT_ALL["Dst-TIME"])[index_0]
    cur_time_diff = np.diff(cur_time)
    index_time = cur_time_diff != 1
    x,y = [],[]
    i=0
    for cur_value in index_time:
        if cur_value == False:
            x.append(cur_time[i])
            y.append(Dst_numpy[index_0][i])
        else:
            # x.append(cur_time[i])
            # y.append(Dst_numpy[index_0][i])
            axP[1].scatter(x,y,color = "#FFD700",s=5)
            x,y = [],[]
        i = i+1
    if len(x) != 0:
        axP[1].scatter(x,y,color = "#FFD700",s=5)
    #intense
    index_0 = (Dst_numpy >= -200) & (Dst_numpy < -100)
    cur_time = np.array(PLOT_ALL["Dst-TIME"])[index_0]
    cur_time_diff = np.diff(cur_time)
    index_time = cur_time_diff != 1
    x,y = [],[]
    i=0
    for cur_value in index_time:
        if cur_value == False:
            x.append(cur_time[i])
            y.append(Dst_numpy[index_0][i])
        else:
            # x.append(cur_time[i])
            # y.append(Dst_numpy[index_0][i])
            axP[1].scatter(x,y,color = "#FF8C00",s=5)
            x,y = [],[]
        i = i+1
    if len(x) != 0:
        axP[1].scatter(x,y,color = "#FF8C00",s=5)
    #super-storm
    index_0 = Dst_numpy < -200
    cur_time = np.array(PLOT_ALL["Dst-TIME"])[index_0]
    cur_time_diff = np.diff(cur_time)
    index_time = cur_time_diff != 1
    x,y = [],[]
    i=0
    for cur_value in index_time:
        if cur_value == False:
            x.append(cur_time[i])
            y.append(Dst_numpy[index_0][i])
        else:
            # x.append(cur_time[i])
            # y.append(Dst_numpy[index_0][i])
            axP[1].scatter(x,y,color = "#FF4C4C",s=5)
            x,y = [],[]
        i = i+1
    if len(x) != 0:
        axP[1].scatter(x,y,color = "#FF4C4C",s=5)
    #=== Set Kp index labels ===#
    axP[0].set_ylabel("Kp index",font = font_label)
    axP[0].set_ylim(0,9)
    y_ticks = []
    y_ticklabels = []
    for i in range(10):
        if i != 0:
            y_ticks.append(i-1/3)
            y_ticklabels.append("")
        y_ticks.append(i)
        if i%2==0:
            y_ticklabels.append("{}o".format(i))
        else:
            y_ticklabels.append("")
        if i != 9:
            y_ticks.append(i+1/3)
            # y_ticklabels.append("{}+".format(i))
            y_ticklabels.append("")
    axP[0].set_yticks(y_ticks)
    axP[0].set_yticklabels(y_ticklabels,font=font_tick)
    #=== Set Dst index labels ===#
    axP[1].set_ylabel("Dst (nT)",font = font_label)
    axP[1].set_ylim(-450,50)
    axP[1].set_yticks([-450,-350,-250,-150,-50,50])
    axP[1].set_yticklabels([-450,-350,-250,-150,-50,50],font=font_tick)
    #Xlabel
    delta_month = 4
    delta_day = 1
    start_doy = tr.ymd2doy(Start[0],Start[1],Start[2],Start[3],Start[4],Start[5])
    end_doy = tr.ymd2doy(End[0],End[1],End[2],End[3],End[4],End[5])
    [start_week,start_sow] = tr.ymd2gpst(Start[0],Start[1],Start[2],Start[3],Start[4],Start[5])
    x_ticks,x_ticklabels = [],[]
    cur_year,cur_doy = Start[0],start_doy
    Cur_time = Start
    [cur_week,cur_sow] = [start_week,start_sow]
    while (cur_year*365 + cur_doy) <= (End[0]*365 + end_doy):
        x_ticks.append((cur_week-start_week)*7*24+(cur_sow-start_sow)/3600)
        x_ticklabels.append("{}-{:0>2}-{:0>2}".format(Cur_time[0],Cur_time[1],int(Cur_time[2])))
        #=== Delta month
        # Cur_time[1] = Cur_time[1] + delta_month
        # if Cur_time[1] > 12:
        #     Cur_time[0] = Cur_time[0] + 1
        #     Cur_time[1] = Cur_time[1] - 12
        # cur_year = Cur_time[0]
        #=== Delta Day
        mjd = tr.ymd2mjd(Cur_time[0],Cur_time[1],Cur_time[2])
        mjd = mjd + delta_day
        [Cur_time[0],Cur_time[1],Cur_time[2]] = tr.mjd2ymd(mjd)

        cur_doy = tr.ymd2doy(Cur_time[0],Cur_time[1],Cur_time[2],Cur_time[3],Cur_time[4],Cur_time[5])
        [cur_week,cur_sow] = tr.ymd2gpst(Cur_time[0],Cur_time[1],Cur_time[2],Cur_time[3],Cur_time[4],Cur_time[5])
    axP[1].set_xticks(x_ticks)
    axP[1].set_xticklabels(x_ticklabels,font = font_tick, rotation = 30)
    #Legend
    axP[0].legend(["Quite","Moderate","Intense","Super"],prop=font_legend,
            framealpha=0,facecolor='none',ncol=4,numpoints=5,markerscale=3, 
            borderaxespad=0,bbox_to_anchor=(1,1.13),loc=1) 
    if Show:
        plt.show()

def Plot_timeseries_solar(File_info=[],Start=[],End=[],Plot_type=[],Save_dir="",Show=True,All=False,Time_type = "GPST"):
    [start_week,start_sow] = tr.ymd2gpst(Start[0],Start[1],Start[2],Start[3],Start[4],Start[5])
    [end_week,end_sow] = tr.ymd2gpst(End[0],End[1],End[2],End[3],End[4],End[5])
    duration_time = (((end_week-start_week)*604800+(end_sow - start_sow))/3600)
    all_data = {}

    #=== load data ===#
    for i in range(len(File_info)):
        if File_info[i][0] not in all_data.keys():
            all_data[File_info[i][0]] = {}
        all_data[File_info[i][0]] = load_data(File_info[i],[start_week,start_sow])

    #=== convert data ===#
    plot_list = ["Kp","ap","Dst"]
    PLOT_ALL, PLOT_RAW = {},{}
    for cur_mode in plot_list:
        if cur_mode not in PLOT_ALL.keys():
            PLOT_ALL[cur_mode],PLOT_ALL[cur_mode+"-TIME"] = [],[]
    for cur_mode in all_data.keys():
        for cur_time in all_data[cur_mode].keys():
            if (cur_time > 0 and cur_time <= duration_time) or All:
                if cur_mode == "Kp":
                    PLOT_ALL["Kp"].append(all_data[cur_mode][cur_time][0])
                    PLOT_ALL["ap"].append(all_data[cur_mode][cur_time][1])
                    PLOT_ALL["Kp-TIME"].append(cur_time)
                    PLOT_ALL["ap-TIME"].append(cur_time)
                elif cur_mode == "Dst":
                    PLOT_ALL["Dst"].append(all_data[cur_mode][cur_time])
                    PLOT_ALL["Dst-TIME"].append(cur_time)
    #=== Plot ===#
    if "Kp" in Plot_type and "Dst" in Plot_type and "ap" in Plot_type:
        plot_Kp_ap_Dst(PLOT_ALL,Start,End,Show)
    if "Kp" in Plot_type and "Dst" in Plot_type:
        plot_Kp_Dst(PLOT_ALL,Start,End,Show)

    