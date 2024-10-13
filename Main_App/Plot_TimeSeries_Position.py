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
import Lib_Plot_Position as PlotPOS


#Setup Plot
file_info_list = [
    ["/Users/hanjunjie/Gap1/IONO_Accuracy_Predict/Project/2021315/client/BRUX-GEC3-FIXED-30-VIR-0.flt", "BRUX", "COR"],
    # ["/Users/hanjunjie/Gap1/IONO_Accuracy_Predict/Project/2021315/client/BRUX-GEC3-FIXED-30-COR_ION.flt", "BRUX", "COR_ZWD"],
    ["/Users/hanjunjie/Gap1/IONO_Accuracy_Predict/Project/2021315/client/BRUX-GEC3-FIXED-30-VIR.flt", "BRUX", "VIR"],
    ] #[filedir, station_name, mode_name] for static station // #[filedir, ref_file, mode_name] for dynamic station

start_time = [2021,11,11,2,0,0]
end_time = [2021,11,11,24,0,0]
plot_type = ["E","N","U"]
ylim = 0.1
save_dir = ""
show = True
fixed = False
all = False
mean = False
time_type = "GPST"
delta_xlabel = 1
sigma = 3
sigma_num = 0
#Setup Statistics
delta_data = 30
reconvergence = 3600
recon_list = [2,5,10]

PlotPOS.plot_timeseries_position(File_info=file_info_list,Start=start_time,End=end_time,Plot_type=plot_type,Ylim=ylim,Save_dir=save_dir,Show=show,Fixed=fixed,All=all,Time_type = time_type,Delta_xlabel = delta_xlabel,Mean=mean,Sigma=sigma,Signum=sigma_num,Delta_data=delta_data,Reconvergence=reconvergence,Recon_list=recon_list)



