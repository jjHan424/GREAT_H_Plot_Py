import os
import sys
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
import Lib_Plot_ROTI as PlotROTI

start_time_list = [[2021,11,1,0,0,0],[2023,2,23,0,0,0],[2023,3,21,0,0,0],[2023,4,21,0,0,0],[2023,11,3,0,0,0],[2024,3,21,0,0,0],[2024,5,9,0,0,0],[2024,8,1,0,0,0],[2024,8,9,0,0,0],[2024,9,10,0,0,0],[2024,10,5,0,0,0],[2021,6,25,0,0,0],[2024,1,28,0,0,0]]
end_time_list =   [[2021,11,8,0,0,0],[2023,3,2,0,0,0],[2023,3,28,0,0,0],[2023,4,28,0,0,0],[2023,11,11,0,0,0],[2024,3,29,0,0,0],[2024,5,23,0,0,0],[2024,8,10,0,0,0],[2024,8,18,0,0,0],[2024,9,23,0,0,0],[2024,10,19,0,0,0],[2021,7,2,0,0,0],[2024,2,4,0,0,0]]

# start_time_list = [[2018,12,22,0,0,0]]
# end_time_list =   [[2018,12,29,0,0,0]]

plot_type = ["ROTI","Dst"] # ROTI_GEC ROTI_G_E_C ROTI_Multi_Site #ROTI Dst
ylim = 2.5
save_dir = ""
show = False
all = False
time_type = "UTC"
delta_xlabel = 12
delta_date = 3
site_list = ['MAS1', 'NABG', 'LPAL', 'IZAN', 'NICO', 'ALME', 'ALME', 'RAEG', 'ANK2', 'SONS', 'ELBA', 'ESCO', 'BRMF', 'COMO', 'BBYS', 'MLVL', 'LODZ', 'VLN1', 'RANT', 'SAS2', 'JON6', 'SPT0', 'LEK6', 'QAQ1', 'UME6', 'OST6', 'ARJ6', 'OVE6', 'KEV2', 'TRO1', 'SCOR', 'VARS', 'WUTH', 'NYA1', 'NYA1', 'NYAL']
# site_list = ['SAS2', 'JON6', 'SPT0', 'LEK6', 'QAQ1', 'UME6', 'OST6', 'ARJ6', 'OVE6', 'KEV2', 'TRO1', 'SCOR', 'VARS', 'WUTH', 'NYA1', 'NYA1', 'NYAL']
site_list = ["HKSC"]
for cur_site in site_list:
    for i in range(len(start_time_list)):
        file_info_list = {
                  "ROTI_{}".format(cur_site):[],
                  "Dst":["/Users/hanjunjie/Gap1/LX/Dst_2021-01-01_2024-06-30_P.dat"]
                }
        start_time_list = [[2021,11,1,0,0,0],[2023,2,23,0,0,0],[2023,3,21,0,0,0],[2023,4,21,0,0,0],[2023,11,3,0,0,0],[2024,3,21,0,0,0],[2024,5,9,0,0,0],[2024,8,1,0,0,0],[2024,8,9,0,0,0],[2024,9,10,0,0,0],[2024,10,5,0,0,0],[2021,6,25,0,0,0],[2024,1,28,0,0,0]]
        end_time_list =   [[2021,11,8,0,0,0],[2023,3,2,0,0,0],[2023,3,28,0,0,0],[2023,4,28,0,0,0],[2023,11,11,0,0,0],[2024,3,29,0,0,0],[2024,5,23,0,0,0],[2024,8,10,0,0,0],[2024,8,18,0,0,0],[2024,9,23,0,0,0],[2024,10,19,0,0,0],[2021,7,2,0,0,0],[2024,2,4,0,0,0]]
        # start_time_list = [[2018,12,22,0,0,0]]
        # end_time_list =   [[2018,12,29,0,0,0]]
        cur_start_time  = start_time_list[i]
        cur_end_time = end_time_list[i]
        cur_doy = tr.ymd2doy(cur_start_time[0],cur_start_time[1],cur_start_time[2],cur_start_time[3],cur_start_time[4],cur_start_time[5])
        end_doy = tr.ymd2doy(cur_end_time[0],cur_end_time[1],cur_end_time[2],cur_end_time[3],cur_end_time[4],cur_end_time[5])
        save_dir = "/Users/hanjunjie/Gap1/LX/ROTI_Image/{}{}{:0>3}.jpg".format(cur_site,cur_start_time[0],cur_doy)
        while cur_doy < end_doy:
            file_info_list["ROTI_{}".format(cur_site)].append("/Users/hanjunjie/Gap1/LX/ROTI/{}{}{:0>3}_GEC.ismr".format(cur_site,cur_start_time[0],cur_doy))
            cur_doy = cur_doy + 1
        PlotROTI.Plot_timeseries_ROTI(File_info=file_info_list,Start=cur_start_time,Plot_type=plot_type,Ylim=ylim,Delta_xlabel=delta_xlabel,Delta_date = delta_date,End=cur_end_time,Save_dir=save_dir,Show=show,All=all,Time_type=time_type)
