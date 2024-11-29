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
import Lib_Plot_Solar as PlotSolar

#Format IAGA-2002

# file_info_list = [["Kp","/Users/hanjunjie/Gap1/LX/isgi_data_1732176731_517437/Kp_2021-01-01_2024-10-31_D.dat"],
#                   ["Dst","/Users/hanjunjie/Gap1/LX/isgi_data_1732176910_490726/Dst_2021-01-01_2024-06-30_P.dat"]]
file_info_list = [["Kp","/Users/hanjunjie/Gap1/LX/Kp_2016-01-01_2020-01-01_D.dat"],
                  ["Dst","/Users/hanjunjie/Gap1/LX/Dst_2016-01-01_2020-01-01_D.dat"]]

start_time = [2016,1,1,0,0,0]
end_time = [2020,1,1,0,0,0]
plot_type = ["Kp","Dst"] # Kp ap Dst
save_dir = ""
show = True
all = False
time_type = "UTC"
delta_xlabel = 1

PlotSolar.Plot_timeseries_solar(File_info=file_info_list,Start=start_time,Plot_type=plot_type,End=end_time,Save_dir=save_dir,Show=show,All=all,Time_type=time_type)

