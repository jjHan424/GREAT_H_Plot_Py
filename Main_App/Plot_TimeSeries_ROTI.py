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



file_info_list = {"ROTI_NYAL":["/Users/hanjunjie/Gap1/LX/ROTI/NYAL2023054_GEC.ismr","/Users/hanjunjie/Gap1/LX/ROTI/NYAL2023055_GEC.ismr","/Users/hanjunjie/Gap1/LX/ROTI/NYAL2023056_GEC.ismr","/Users/hanjunjie/Gap1/LX/ROTI/NYAL2023057_GEC.ismr","/Users/hanjunjie/Gap1/LX/ROTI/NYAL2023058_GEC.ismr","/Users/hanjunjie/Gap1/LX/ROTI/NYAL2023059_GEC.ismr","/Users/hanjunjie/Gap1/LX/ROTI/NYAL2023060_GEC.ismr"],
                  "ROTI_SONS":["/Users/hanjunjie/Gap1/LX/ROTI/SONS2023054_GEC.ismr","/Users/hanjunjie/Gap1/LX/ROTI/SONS2023055_GEC.ismr","/Users/hanjunjie/Gap1/LX/ROTI/SONS2023056_GEC.ismr","/Users/hanjunjie/Gap1/LX/ROTI/SONS2023057_GEC.ismr","/Users/hanjunjie/Gap1/LX/ROTI/SONS2023058_GEC.ismr","/Users/hanjunjie/Gap1/LX/ROTI/SONS2023059_GEC.ismr","/Users/hanjunjie/Gap1/LX/ROTI/SONS2023060_GEC.ismr"],
                  "ROTI_NYAL":["/Users/hanjunjie/Gap1/LX/ROTI/NYAL2023054_GEC.ismr","/Users/hanjunjie/Gap1/LX/ROTI/NYAL2023055_GEC.ismr","/Users/hanjunjie/Gap1/LX/ROTI/NYAL2023056_GEC.ismr","/Users/hanjunjie/Gap1/LX/ROTI/NYAL2023057_GEC.ismr","/Users/hanjunjie/Gap1/LX/ROTI/NYAL2023058_GEC.ismr","/Users/hanjunjie/Gap1/LX/ROTI/NYAL2023059_GEC.ismr","/Users/hanjunjie/Gap1/LX/ROTI/NYAL2023060_GEC.ismr"],
                }
file_info_list = {
                  "ROTI_NYAL":["/Users/hanjunjie/Gap1/LX/ROTI/NYAL2021176_GEC.ismr","/Users/hanjunjie/Gap1/LX/ROTI/NYAL2021177_GEC.ismr","/Users/hanjunjie/Gap1/LX/ROTI/NYAL2021178_GEC.ismr","/Users/hanjunjie/Gap1/LX/ROTI/NYAL2021179_GEC.ismr"],
                  "Dst":["/Users/hanjunjie/Gap1/LX/isgi_data_1732176910_490726/Dst_2021-01-01_2024-06-30_P.dat"]
                }

start_time = [2021,6,25,0,0,0]
end_time = [2021,7,1,0,0,0]
plot_type = ["ROTI","Dst"] # ROTI_GEC ROTI_G_E_C ROTI_Multi_Site #ROTI Dst
ylim = 0
save_dir = ""
show = True
all = False
time_type = "UTC"
delta_xlabel = 6
delta_date = 2

PlotROTI.Plot_timeseries_ROTI(File_info=file_info_list,Start=start_time,Plot_type=plot_type,Ylim=ylim,Delta_xlabel=delta_xlabel,Delta_date = delta_date,End=end_time,Save_dir=save_dir,Show=show,All=all,Time_type=time_type)