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
    ["/Users/hanjunjie/Master_3/1-IUGG/ResFromServer/HKNP-GEC2-FIXED-30.flt", "HKNP", "HKNP"],
    ["/Users/hanjunjie/Master_3/1-IUGG/ResFromServer/HKOH-GEC2-FIXED-30.flt", "HKOH", "HKOH"],
    ] #[filedir, station_name, mode_name] for static station // #[filedir, ref_file, mode_name] for dynamic station

start_time = [2021,12,10,17,0,0]
end_time = [2021,12,10,24,0,0]
plot_type = ["E","N","U"]
ylim = 0.15
save_dir = ""
show = True
fixed = True
all = False
mean = True
time_type = "GPST"
delta_xlabel = 3
sigma = 3
sigma_num = 0
#Setup Statistics
delta_data = 30
reconvergence = 3600
recon_list = [2,5,10]

PlotPOS.plot_timeseries_position(File_info=file_info_list,Start=start_time,End=end_time,Plot_type=plot_type,Ylim=ylim,Save_dir=save_dir,Show=show,Fixed=fixed,All=all,Time_type = time_type,Delta_xlabel = delta_xlabel,Mean=mean,Sigma=sigma,Signum=sigma_num,Delta_data=delta_data,Reconvergence=reconvergence,Recon_list=recon_list)



