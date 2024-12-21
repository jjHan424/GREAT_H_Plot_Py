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
site_list = ['KOS1','WSRT','BRUX','TIT2','REDU','FFMJ']
site_list_pair = ['ONS1-ONSA',"SPT0-SPT7","BUDP-BUDD"]
# for site_pair in site_list_pair:
file_info_list = [[],[]]
for site in site_list:
    ref_dir = "/Users/hanjunjie/Gap1/Data/2023/ZTD"
    # cal_dir = "/Users/hanjunjie/Gap1/ZWD_Retrieval_PPPRTK/Server/ZWD_GRD_CHEN"
    cal_dir = "/Users/hanjunjie/Gap1/ZWD_Retrieval_PPPRTK/Server/ZWD"
    start_time = [2023,3,17,2,0,0]
    end_time = [2023,3,28,23,59,30]
    start_hour,end_hour = 2,24
    start_doy = tr.ymd2doy(start_time[0],start_time[1],start_time[2],start_time[3],start_time[4],start_time[5])
    end_doy = tr.ymd2doy(end_time[0],end_time[1],end_time[2],end_time[3],end_time[4],end_time[5])
    cur_doy = start_doy
    plot_type = "ZWD_DELTA" # ZWD_DELTA ZWD_RAW GRD_RAW GRD_DELTA
    file_info_list = [[],[]]
    PPP_file,PPPRTK_file,REF_file = "","",""
    PPP_file1,PPPRTK_file1 = "",""
    PPP_file2,PPPRTK_file2 = "",""
    mode = "FIXED"
    while cur_doy <= end_doy:
        file_info_list[0].append(os.path.join(cal_dir,"PPP","{}{:0>3}".format(2023,cur_doy),"client",   "{}-GEC3-{}-30-3600.flt".format(site,mode)))
        file_info_list[1].append(os.path.join(cal_dir,"PPPRTK","{}{:0>3}".format(2023,cur_doy),"client","{}-GEC3-{}-30-3600.flt".format(site,mode)))
        cur_doy = cur_doy + 1
    file_info_list[0].append(site)
    file_info_list[0].append("PPP")
    file_info_list[1].append(site)
    file_info_list[1].append("PPPRTK")
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