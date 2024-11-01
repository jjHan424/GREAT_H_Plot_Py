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

file_info_list = [
    ["/Users/hanjunjie/Gap1/IONO_Accuracy_Predict/Res_FromServer/CLIENT/TrpAcc/FFMJ-GEC3-FIXED-TRP-10-30-3600.flt","FFMJ","5"],
    ["/Users/hanjunjie/Gap1/IONO_Accuracy_Predict/Res_FromServer/CLIENT/TrpAcc/FFMJ-GEC3-FIXED-TRP-20-30-3600.flt","FFMJ","10"],
    # ["/Users/hanjunjie/Gap1/IONO_Accuracy_Predict/Res_FromServer/CLIENT/TrpAcc/FFMJ-GEC3-FIXED-TRP-25-30-3600.flt","FFMJ","30"],
    ["/Users/hanjunjie/Gap1/IONO_Accuracy_Predict/Res_FromServer/CLIENT/TrpAcc/FFMJ-GEC3-FIXED-TRP-60-30-3600.flt","FFMJ","30"],
    ["/Users/hanjunjie/Gap1/IONO_Accuracy_Predict/Res_FromServer/CLIENT/TrpAcc/FFMJ-GEC3-FIXED-TRP-100-30-3600.flt","FFMJ","50"],
] #[[File1, File2, ..., Filen, Site, Mode1]]

start_time = [2021,11,11,2,0,0]
end_time = [2021,11,11,24,0,0]
plot_type = "HV" #Horizontal Vertical HV
save_dir = ""
ylim = 0.5
percentage = 0.95
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

PlotPOS.Plot_percent_position(File_info=file_info_list,Start=start_time,End=end_time,Plot_type=plot_type,Ylim=ylim,Percentage = percentage,Save_dir=save_dir,Show=show,Fixed=fixed,All=all,Time_type = time_type,Delta_xlabel = delta_xlabel,Mean=mean,Sigma=sigma,Signum=sigma_num,Delta_data=delta_data,Reconvergence=reconvergence,Recon_list=recon_list)