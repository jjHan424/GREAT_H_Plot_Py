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
import Lib_Plot_AUG as PlotAUG

#Setup Plot
file_info_list = [
    # "/Users/hanjunjie/Gap1/ZWD_Retrieval_PPPRTK/Server/Grid_Diff_B2b/FLT_B2b_Single/2023340/CMNCYN-R-C-CROSS/YNJD-GEC3-30.diff",
    "/Users/hanjunjie/Gap1/ZWD_Retrieval_PPPRTK/Server/Grid_Diff_B2b/FLT_B2b_Single/2023340/EPN1-R-C-CROSS/EUSK-GEC3-30.diff",
    # "/Users/hanjunjie/Gap1/IONO_Accuracy_Predict/Res_FromServer/CLIENT/BRUX-GEC3-FIXED-30-10.aug"
    ] #[Raw, Model]

start_time = [2023,12,6,0,0,0]
end_time = [2023,12,7,0,0,0]
plot_type = "DION" # ION, ZWD, NSAT_RAW, NSAT_MODEL, NSAT_COM DION DTRP _GEC
ylim = 0
save_dir = ""
show = True
all = False
time_type = "GPST"
delta_xlabel = 1/4
sigma = 3
sigma_num = 0
delay_model = 0
legend = False

PlotAUG.Plot_timeseries_aug_compare(File_info=file_info_list,Start=start_time,End=end_time,Plot_type=plot_type,Ylim=ylim,Save_dir=save_dir,Show=show,All=all,Time_type = time_type,Delta_xlabel = delta_xlabel,Legend = legend,Sigma=sigma,Signum=sigma_num)
