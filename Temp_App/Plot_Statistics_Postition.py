import os
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
#import seaborn as sns
import trans as tr
import glv

file_name = "/Users/hanjunjie/Gap1/IONO_Accuracy_Predict/Res_FromServer/CLIENT/FFMJ-ION-ConAccuracy.csv"
file_name_temp = "/Users/hanjunjie/Gap1/IONO_Accuracy_Predict/Res_FromServer/CLIENT/FFMJ-ION.csv"
plot_type = "Recon" # Position Fixed Recon
recon_accuracy = 10
#=== Read File ===#
PLOT_ALL = {}
with open(file_name,"r") as f:
    for line in f:
        value = line.split(",")
        if value[0] == "Mode":
            head_list = []
            for i in range(0,len(value)):
                temp = value[i].replace(" ","")
                head_list.append(temp)
                PLOT_ALL[temp] = []
        else:
            for i in range(0,len(value)):
                if head_list[i] == "Inter" or head_list[i] == "Fixed":
                    PLOT_ALL[head_list[i]].append(float(value[i][:-1]))
                elif head_list[i] == "Mode":
                    PLOT_ALL[head_list[i]].append(value[i])
                else:
                    PLOT_ALL[head_list[i]].append(float(value[i]))

PLOT_ALL_temp = {}
with open(file_name_temp,"r") as f:
    for line in f:
        value = line.split(",")
        if value[0] == "Mode":
            head_list = []
            for i in range(0,len(value)):
                temp = value[i].replace(" ","")
                head_list.append(temp)
                PLOT_ALL_temp[temp] = []
        else:
            for i in range(0,len(value)):
                if head_list[i] == "Inter" or head_list[i] == "Fixed":
                    PLOT_ALL_temp[head_list[i]].append(float(value[i][:-1]))
                elif head_list[i] == "Mode":
                    PLOT_ALL_temp[head_list[i]].append(value[i])
                else:
                    PLOT_ALL_temp[head_list[i]].append(float(value[i]))

#=== Plot ===#
if plot_type == "Position":
    figP,axP = plt.subplots(3,1,figsize=(12,8),sharey=False,sharex=True)
    plot_list = {"E":0,"N":1,"U":2}
    for cur_type in plot_list:
        axP[plot_list[cur_type]].axhline(y = PLOT_ALL[cur_type][0],color = glv.color_list[0],ls='--',linewidth = 3)
        axP[plot_list[cur_type]].axhline(y = PLOT_ALL[cur_type][1],color = glv.color_list[1],ls='--',linewidth = 3)
        axP[plot_list[cur_type]].axhline(y = PLOT_ALL[cur_type][2],color = glv.color_list[2],ls='--',linewidth = 3)
    for cur_type in plot_list:
        axP[plot_list[cur_type]].plot(PLOT_ALL[cur_type][3:])
    # axP[3].plot(PLOT_ALL["U"][3:])
    # axP[3].axhline(y = PLOT_ALL["U"][0],color = glv.color_list[0],ls='--',linewidth = 3)
    # axP[3].axhline(y = PLOT_ALL["U"][1],color = glv.color_list[1],ls='--',linewidth = 3)
    # axP[3].axhline(y = PLOT_ALL["U"][2],color = glv.color_list[2],ls='--',linewidth = 3)
    # Bracked Ylabel
    # axP[2].set_ylim(20,46)
    # axP[3].set_ylim(0,2)
    # axP[2].spines.bottom.set_visible(False)
    # axP[3].spines.top.set_visible(False)
    # axP[2].xaxis.tick_top()
    # axP[2].tick_params(labeltop=False)  # don't put tick labels at the top
    # axP[3].xaxis.tick_bottom()
    # d = .5  # proportion of vertical to horizontal extent of the slanted line
    # kwargs = dict(marker=[(-1, -d), (1, d)], markersize=12,
    #         linestyle="none", color='k', mec='k', mew=1, clip_on=False)
    # axP[2].plot([0, 1], [0, 0], transform=axP[2].transAxes, **kwargs)
    # axP[3].plot([0, 1], [1, 1], transform=axP[3].transAxes, **kwargs)
    # Bracked Ylabel End
    # box = axP[0].get_position()
    # axP[0].set_position([box.x0, box.y0 - box.height/3, box.width, box.height*4/3])
    # box = axP[1].get_position()
    # axP[1].set_position([box.x0, box.y0 - box.height*0.75, box.width, box.height*4/3])
    # box = axP[2].get_position()
    # axP[2].set_position([box.x0, box.y0+box.height*0.05, box.width, box.height*0.1*4/3])
    # box = axP[3].get_position()
    # axP[3].set_position([box.x0, box.y0 - box.height*0.05, box.width, box.height*0.9*4/3])
    axP[0].legend(["No Atmosphere","Only Iono","Only Trop"],prop=glv.font_legend,
            framealpha=0,facecolor='none',ncol=3,numpoints=5,markerscale=3, 
            borderaxespad=0,bbox_to_anchor=(1,1.45),loc=1) 
    axP[1].set_ylabel("Positioning errors (cm)",glv.font_label)
    axP[2].set_xlabel("Prior ionosphere accuracy (cm)",glv.font_label)
    axP[0].set_title("East",glv.font_title)
    axP[1].set_title("North",glv.font_title)
    axP[2].set_title("Up",glv.font_title)
    xtick,xtick_label = [],[]
    for i in range(0,201,20):
        xtick.append(i)
        xtick_label.append(int(i*0.5))
    axP[2].set_xticks(xtick)
    axP[2].set_xticklabels(xtick_label)
    labels = axP[0].get_yticklabels()
    for i in range(3):
        labels = labels + axP[i].get_yticklabels() + axP[i].get_xticklabels()
    [label.set_fontsize(glv.xtick_size) for label in labels]
    [label.set_fontname('Arial') for label in labels]

if plot_type == "Fixed":
    figP,axP = plt.subplots(1,1,figsize=(12,6),sharey=False,sharex=True)
    # for cur_type in plot_list:
    #     axP[plot_list[cur_type]].axhline(y = PLOT_ALL[cur_type][0],color = glv.color_list[0],ls='--',linewidth = 3)
    #     axP[plot_list[cur_type]].axhline(y = PLOT_ALL[cur_type][1],color = glv.color_list[1],ls='--',linewidth = 3)
    #     axP[plot_list[cur_type]].axhline(y = PLOT_ALL[cur_type][2],color = glv.color_list[2],ls='--',linewidth = 3)
    
    axP.plot(np.array(PLOT_ALL["Fixed"][3:]) * np.array(PLOT_ALL["Inter"][3:]) / 100, color = glv.color_list[0],linewidth = 2)
    axP.set_ylabel("Fixed rate (%)",glv.font_label)
    axP.set_xlabel("Prior atmosphere accuracy (cm)",glv.font_label)
    xtick,xtick_label = [],[]
    for i in range(0,201,20):
        xtick.append(i)
        xtick_label.append(int(i*0.5))
    axP.set_xticks(xtick)
    axP.set_xticklabels(xtick_label)
    labels = axP.get_yticklabels() + axP.get_xticklabels()
    [label.set_fontsize(glv.xtick_size) for label in labels]
    [label.set_fontname('Arial') for label in labels]
    PLOT_ALL = {}
    file_name = "/Users/hanjunjie/Gap1/IONO_Accuracy_Predict/Res_FromServer/CLIENT/WARE-TRP-ConAccuracy.csv"
    with open(file_name,"r") as f:
        for line in f:
            value = line.split(",")
            if value[0] == "Mode":
                head_list = []
                for i in range(0,len(value)):
                    temp = value[i].replace(" ","")
                    head_list.append(temp)
                    PLOT_ALL[temp] = []
            else:
                for i in range(0,len(value)):
                    if head_list[i] == "Inter" or head_list[i] == "Fixed":
                        PLOT_ALL[head_list[i]].append(float(value[i][:-1]))
                    elif head_list[i] == "Mode":
                        PLOT_ALL[head_list[i]].append(value[i])
                    else:
                        PLOT_ALL[head_list[i]].append(float(value[i]))
    axP.plot(np.array(PLOT_ALL["Fixed"][3:]) * np.array(PLOT_ALL["Inter"][3:]) / 100, color = glv.color_list[1], linewidth = 2)
    axP.legend(["Ionosphere","Tropsphere"],prop=glv.font_legend,
            framealpha=0,facecolor='none',ncol=3,numpoints=5,markerscale=3, 
            borderaxespad=0,bbox_to_anchor=(1,1.1),loc=1)
    leg = axP.get_legend()
    for legobj in leg.legendHandles:
        legobj.set_linewidth(5)

if plot_type == "Recon":
    figP,axP = plt.subplots(1,2,figsize=(12,6),sharey=True,sharex=True)
    # for cur_type in plot_list:
    #     axP[plot_list[cur_type]].axhline(y = PLOT_ALL[cur_type][0],color = glv.color_list[0],ls='--',linewidth = 3)
    #     axP[plot_list[cur_type]].axhline(y = PLOT_ALL[cur_type][1],color = glv.color_list[1],ls='--',linewidth = 3)
    #     axP[plot_list[cur_type]].axhline(y = PLOT_ALL[cur_type][2],color = glv.color_list[2],ls='--',linewidth = 3)
    accuracy_list = np.array(range(0,81))
    axP[0].set_ylim(0,700)
    axP[0].plot(PLOT_ALL["{:0>2}-H".format(recon_accuracy)][3:], color = 'k',linewidth = 2)
    axP[0].plot(PLOT_ALL_temp["{:0>2}-H".format(recon_accuracy)][3:], color = 'gray',linewidth = 2)
    axP[0].set_ylabel("Reconvergence time (s)",glv.font_label)
    axP[0].set_xlabel("Prior ionosphere accuracy (cm)",glv.font_label)
    axP[0].set_title("Horizontal",glv.font_title)
    axP[0].axhline(y = PLOT_ALL["{:0>2}-H".format(recon_accuracy)][0],color = glv.color_list[0],ls='--',linewidth = 3)
    axP[0].axhline(y = PLOT_ALL["{:0>2}-H".format(recon_accuracy)][1],color = glv.color_list[1],ls='--',linewidth = 3)
    axP[0].axhline(y = PLOT_ALL["{:0>2}-H".format(recon_accuracy)][2],color = glv.color_list[2],ls='--',linewidth = 3)
    # index_temp = np.array(PLOT_ALL["{:0>2}-H".format(recon_accuracy)][3:]) > PLOT_ALL["{:0>2}-H".format(recon_accuracy)][0]
    # temp_acc = accuracy_list[index_temp]
    # if temp_acc.size > 0:
    #     axP[0].axvline(x = temp_acc[0], ymin = 0, ymax =  PLOT_ALL["{:0>2}-H".format(recon_accuracy)][0]/1000,color = glv.color_list[0],ls='--',linewidth = 3)
    #     ax_range = axP[0].axis()
    #     axP[0].text(temp_acc[0]+1,50,"{:.1f}cm".format(temp_acc[0]*0.5),glv.font_text)

    axP[1].axhline(y = PLOT_ALL["{:0>2}-V".format(recon_accuracy)][0],color = glv.color_list[0],ls='--',linewidth = 3)
    axP[1].axhline(y = PLOT_ALL["{:0>2}-V".format(recon_accuracy)][1],color = glv.color_list[1],ls='--',linewidth = 3)
    axP[1].axhline(y = PLOT_ALL["{:0>2}-V".format(recon_accuracy)][2],color = glv.color_list[2],ls='--',linewidth = 3)
    axP[1].plot(PLOT_ALL["{:0>2}-V".format(recon_accuracy)][3:], color = 'k',linewidth = 2)
    axP[1].plot(PLOT_ALL_temp["{:0>2}-V".format(recon_accuracy)][3:], color = 'gray',linewidth = 2)
    # index_temp = np.array(PLOT_ALL["{:0>2}-V".format(recon_accuracy)][3:]) > PLOT_ALL["{:0>2}-V".format(recon_accuracy)][0]
    # temp_acc = accuracy_list[index_temp]
    # axP[1].axvline(x = temp_acc[0], ymin = 0, ymax =  PLOT_ALL["{:0>2}-V".format(recon_accuracy)][0]/1000,color = glv.color_list[0],ls='--',linewidth = 3)
    # ax_range = axP[1].axis()
    # axP[1].text(temp_acc[0]+1,50,"{:.1f}cm".format(temp_acc[0]*0.5),glv.font_text)
    axP[1].set_xlabel("Prior ionosphere accuracy (cm)",glv.font_label)
    axP[1].set_title("Vertical",glv.font_title)
    
    xtick,xtick_label = [],[]
    for i in range(0,201,20):
        xtick.append(i)
        xtick_label.append(int(i*0.5))
    axP[0].set_xticks(xtick)
    axP[0].set_xticklabels(xtick_label)
    labels = axP[0].get_yticklabels() + axP[0].get_xticklabels() + axP[1].get_yticklabels() + axP[1].get_xticklabels()
    [label.set_fontsize(glv.xtick_size) for label in labels]
    [label.set_fontname('Arial') for label in labels]
    axP[1].legend(["No Atmosphere","Only Iono","Only Trop"],prop=glv.font_legend,
            framealpha=0,facecolor='none',ncol=3,numpoints=5,markerscale=3, 
            borderaxespad=0,bbox_to_anchor=(1,1.15),loc=1)
     


plt.show()
# plt.savefig("/Users/hanjunjie/Gap1/汇报/Image/FFMJ-ION-ConAccuracy-Reconvergence_ION.jpg",dpi = 600)
