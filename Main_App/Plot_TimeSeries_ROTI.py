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



file_info_list = {"ROTI_  30S":["/Users/hanjunjie/Gap1/Magnetic_storm/Server/ROTI_HK/30S_5MIN/HKSC2021305_GEC.ismr"],
                  "ROTI_  1S-10EPOCHS":  ["/Users/hanjunjie/Gap1/Magnetic_storm/Server/ROTI_HK/1S_10S/HKSC2021305_GEC.ismr"],
                  "ROTI_  1S-10MINS":  ["/Users/hanjunjie/Gap1/Magnetic_storm/Server/ROTI_HK/1S_5MIN/HKSC2021305_GEC.ismr"],
                }
# file_info_list = {
#                   "ROTI_NYAL":["/Users/hanjunjie/Gap1/LX/ROTI/NYAL2021176_GEC.ismr","/Users/hanjunjie/Gap1/LX/ROTI/NYAL2021177_GEC.ismr","/Users/hanjunjie/Gap1/LX/ROTI/NYAL2021178_GEC.ismr","/Users/hanjunjie/Gap1/LX/ROTI/NYAL2021179_GEC.ismr"],
#                   "Dst":["/Users/hanjunjie/Gap1/LX/isgi_data_1732176910_490726/Dst_2021-01-01_2024-06-30_P.dat"]
#                 }

start_time = [2021,11,1,0,0,0]
end_time = [2021,11,1,24,0,0]
plot_type = ["ROTI_Multi_Site"] # ROTI_GEC ROTI_G_E_C ROTI_Multi_Site #ROTI Dst
ylim = 0
save_dir = ""
show = True
all = False
time_type = "UTC"
delta_xlabel = 6
delta_date = 2

PlotROTI.Plot_timeseries_ROTI(File_info=file_info_list,Start=start_time,Plot_type=plot_type,Ylim=ylim,Delta_xlabel=delta_xlabel,Delta_date = delta_date,End=end_time,Save_dir=save_dir,Show=show,All=all,Time_type=time_type)