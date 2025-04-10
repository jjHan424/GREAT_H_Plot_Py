import os
import sys
sys.path.insert(0,os.path.dirname(__file__)+'/../LibBase')
sys.path.insert(0,os.path.dirname(__file__)+'/../LibPlot')
import numpy as np
import matplotlib as mpl
mpl.use("TkAgg")
import trans as tr
import glv
import matplotlib.pyplot as plt

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

file_info_list = [
     [r"E:\PhD_1\4.RTZTD\BNC\CNE_01S.log","1S"],
     [r"E:\PhD_1\4.RTZTD\BNC\CNE_05M_TestMem.log","5M"],
     [r"E:\PhD_1\4.RTZTD\BNC\CNE_CORR.log","Base"],
]
start_time = [2025,4,7,15,47,48]
end_time = [2025,4,7,16,0,0]
All = True
Data_Plot = {}
[start_week,start_sow] = tr.ymd2gpst(start_time[0],start_time[1],start_time[2],start_time[3],start_time[4],start_time[5])
[end_week,end_sow] = tr.ymd2gpst(end_time[0],end_time[1],end_time[2],end_time[3],end_time[4],end_time[5])

duration_time = ((end_week-start_week)*604800+(end_sow - start_sow))/3600
mode_list = []
[XLabel,XTick,cov_time,begT,LastT]=glv.xtick("UTC",start_time[0],start_time[1],start_time[2],start_time[3]+start_time[4]/60,duration_time,1)
for cur_file in file_info_list:
    Data_Plot[cur_file[1]] = {}
    Data_Plot[cur_file[1]]["TIME"] = []
    Data_Plot[cur_file[1]]["DATA"] = []
    timeline = False
    ymd = [start_time[0],start_time[1],start_time[2]]
    soweek_last = -1
    mode_list.append(cur_file[1])
    with open(cur_file[0],'rt') as f:
        for line in f:
            if "top" in line:
                timeline = False
                value = line.split()
                time = value[2]
                hour,min,sec = float(time.split(":")[0]),float(time.split(":")[1]),float(time.split(":")[2])
                [w,soweek] = tr.ymd2gpst(ymd[0],ymd[1],ymd[2],hour,min,sec)
                if soweek < soweek_last and soweek_last!=-1:
                    ymd[2] = ymd[2]+1
                    [w,soweek] = tr.ymd2gpst(ymd[0],ymd[1],ymd[2],hour,min,sec)
                soweek_last = soweek
                soweek = (w-end_week)*604800+soweek
                if w >= start_week and w <= end_week:
                    if soweek >= start_sow and soweek <= start_sow+duration_time*3600:
                        timeline = True
                if All:
                    timeline = True
            if "guille" in line and timeline:
                value = line.split()
                if float(value[8]) == 0.0:
                    continue
                Data_Plot[cur_file[1]]["TIME"].append((soweek - cov_time)/3600)
                Data_Plot[cur_file[1]]["DATA"].append(float(value[8]))
                # Data_Plot[cur_file[1]]["DATA"].append(float(value[4][:-1]))

figP,axP = plt.subplots(1,1,figsize=(12,6),sharey=True,sharex=True)
j=0
for cur_type in Data_Plot.keys():
    axP.plot(Data_Plot[cur_type]["TIME"],Data_Plot[cur_type]["DATA"],color = color_list[j%3])
    # axP.scatter(Data_Plot[cur_type]["TIME"],Data_Plot[cur_type]["DATA"],color = color_list[j%3])
    j=j+1
#===Set Label===#
if not All:
    axP.set_xticks(XTick)
    axP.set_xticklabels(XLabel)
labels = axP.get_yticklabels() + axP.get_xticklabels()
[label.set_fontsize(xtick_size) for label in labels]
[label.set_fontname('Arial') for label in labels]
axP.set_xlabel('UTC+2 (hour)',font_label)
# axP.set_xlabel('Time (YYYY-MM-DD)',font_label)
axP.set_ylabel('CPU (%)',font_label)
#===Set legend===#
axP.legend(mode_list,prop=font_legend,
        framealpha=0,facecolor='none',ncol=4,numpoints=5,markerscale=3, 
        borderaxespad=0,bbox_to_anchor=(1,1.08),loc=1)
MRS_str = "MEAN:"
RMS_value = []
for cur_mode in Data_Plot.keys():
    MRS_str = MRS_str + " {:.1f}%,".format(np.sqrt(np.mean(np.array(Data_Plot[cur_mode]["DATA"])**2)))
    # RMS_value.append(np.sqrt(np.mean(np.array(Plot_Data[cur_mode]["ZWD"])[index_rms]**2)))
# MRS_str = MRS_str + " {:.2f}%,".format((RMS_value[0] - RMS_value[1])/RMS_value[0]*100)
ax_range = axP.axis()
axP.text(ax_range[0],ax_range[3],MRS_str[:-1],font_text)
print(MRS_str[:-1])
plt.show()


