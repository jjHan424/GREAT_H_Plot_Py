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
import Lib_Plot_ZWD as PlotZWD

#Setup Plot
file_info_list = [
    ["/Users/hanjunjie/Gap1/ZWD_Retrieval_PPPRTK/Server/ZWD_GRD_CHEN/PPP/2023073/client/ONS1-GEC3-FIXED-30.flt","/Users/hanjunjie/Gap1/ZWD_Retrieval_PPPRTK/Server/ZWD_GRD_CHEN/PPP/2023073/client/ONSA-GEC3-FIXED-30.flt","PPP"],
    ["/Users/hanjunjie/Gap1/ZWD_Retrieval_PPPRTK/Server/ZWD_GRD_CHEN/PPPRTK/2023073/client/ONS1-GEC3-FIXED-30.flt","/Users/hanjunjie/Gap1/ZWD_Retrieval_PPPRTK/Server/ZWD_GRD_CHEN/PPP/2023073/client/ONSA-GEC3-FIXED-30.flt","PPPRTK"]
    ] #[Raw, Ref, Mode] #[file,mode]
# file_info_list = [
#     ["/Users/hanjunjie/Gap1/ZWD_Retrieval_PPPRTK/Server/ZWD/PPP/2023073/client/BUDD-GEC3-FIXED-30.flt","PPP"],
#     ["/Users/hanjunjie/Gap1/ZWD_Retrieval_PPPRTK/Server/ZWD/PPPRTK/2023073/client/BUDD-GEC3-FIXED-30.flt","PPPRTK"],
#     ["/Users/hanjunjie/Gap1/Data/2023/ZTD/073/BUDP0730.23zpd","REF"]
#     ] #[Raw, Ref, Mode] #[file,mode]
site_list = ['WSRT','KOS1','BRUX','TIT2','REDU','FFMJ']
site_list_pair = ['ENSG-MLVL']
for site_pair in site_list_pair:
# for site in site_list:
    ref_dir = "/Users/hanjunjie/Gap1/Data/2023/ZTD"
    # cal_dir = "/Users/hanjunjie/Gap1/ZWD_Retrieval_PPPRTK/Server/ZWD_GRD_CHEN"
    cal_dir = "/Users/hanjunjie/Gap1/ZWD_Retrieval_PPPRTK/Server/ZWD"
    # cal_dir = "/Users/hanjunjie/Gap1/ZWD_Retrieval_PPPRTK/Server/ZWD_KINEMATIC"
    # start_time = [2023,3,14,0,0,0]
    # end_time =   [2023,12,31,0,0,0]
    # start_time = [2023,12,15,0,0,0]
    # end_time =   [2023,12,31,0,0,0]
    start_time = [2024,12,7,0,0,0]
    end_time =   [2024,12,13,0,0,0]
    start_hour,end_hour = 3,24
    start_doy = tr.ymd2doy(start_time[0],start_time[1],start_time[2],start_time[3],start_time[4],start_time[5])
    end_doy = tr.ymd2doy(end_time[0],end_time[1],end_time[2],end_time[3],end_time[4],end_time[5])
    cur_doy = start_doy
    plot_type = "ZWD_DELTA_CDF" # ZWD_DELTA ZWD_RAW GRD_RAW GRD_DELTA ZWD_DELTA_CDF ZWD_DELTA_DISTRIBUTION
    file_info_list = []
    PPP_file,PPPRTK_file,REF_file = "","",""
    PPP_file1,PPPRTK_file1 = "",""
    PPP_file2,PPPRTK_file2 = "",""
    PPP_file_float = ""
    mode = "FIXED"
    while cur_doy <= end_doy:
        # PPP_file = PPP_file +             os.path.join(cal_dir+"","PPP","{}{:0>3}".format(2023,cur_doy),"client",   "{}-GEC3-{}-30.flt".format(site,mode)) + ","
        # PPP_file_float = PPP_file_float + os.path.join(cal_dir+"","PPP","{}{:0>3}".format(2023,cur_doy),"client",   "{}-GEC3-{}-30.flt".format(site,"FLOAT")) + ","
        # PPPRTK_file = PPPRTK_file +       os.path.join(cal_dir+"","PPPRTK","{}{:0>3}".format(2023,cur_doy),"client","{}-GEC3-{}-30.flt".format(site,mode)) + ","
        # PPPRTK_file1 = PPPRTK_file1 +     os.path.join(cal_dir+"","PPPRTK","{}{:0>3}".format(2023,cur_doy),"client","{}-GEC3-{}-30.flt".format(site,"FLOAT")) + ","
        # REF_file = REF_file + os.path.join(ref_dir,"{:0>3}".format(cur_doy),"{}{:0>3}0.23zpd".format(site,cur_doy)) + ","
        
        #=== Zero baseline ===#
        site1,site2 = site_pair.split('-')[0], site_pair.split('-')[1]
        PPP_file1 = PPP_file1 + os.path.join(cal_dir,"PPP","{}{:0>3}".format(start_time[0],cur_doy),"client",         "{}-GEC2-{}-30.flt".format(site1,mode)) + ","
        PPP_file2 = PPP_file2 + os.path.join(cal_dir,"PPP","{}{:0>3}".format(start_time[0],cur_doy),"client",         "{}-GEC2-{}-30.flt".format(site2,mode)) + ","
        PPPRTK_file1 = PPPRTK_file1 + os.path.join(cal_dir,"PPPRTK","{}{:0>3}".format(start_time[0],cur_doy),"client","{}-GEC2-{}-30.flt".format(site1,mode)) + ","
        PPPRTK_file2 = PPPRTK_file2 + os.path.join(cal_dir,"PPPRTK","{}{:0>3}".format(start_time[0],cur_doy),"client","{}-GEC2-{}-30.flt".format(site2,mode)) + ","
        cur_doy = cur_doy + 1
    if "DELTA" in plot_type:
        # file_info_list = [
        #     [PPP_file[:-1],REF_file[:-1],"PPP-AR: {}".format(site)],
        #     # [PPP_file_float[:-1],REF_file[:-1],"PPP-{}".format(site)],
        #     [PPPRTK_file[:-1],REF_file[:-1],"IONO-W: {}".format(site)],
        #     # [PPPRTK_file1[:-1],REF_file[:-1],"PPPRTK-FLOAT{}".format(site)]
        # ]
        file_info_list = [
            [PPP_file1[:-1],PPP_file2[:-1],"PPP-AR: {}".format(site1)],
            [PPPRTK_file1[:-1],PPP_file2[:-1],"IONO-W: {}".format(site1)]
        ]
    else:
        # file_info_list = [
        #     [PPP_file[:-1],"PPPAR-{}".format(site_pair[0:4])],
        #     [PPPRTK_file[:-1],"PPPRTK-{}".format(site_pair[5:])],
        #     # [REF_file[:-1],"REF-{}".format(site)]
        # ]
        file_info_list = [
            [PPP_file1[:-1],"PPP-{}".format(site1)],
            [PPP_file2[:-1],"PPP-{}".format(site2)],
            # [PPPRTK_file1[:-1],"PPPRTK-{}".format(site2)],
            # [REF_file[:-1],"REF-{}".format(site)]
        ]

    ylim = 0 # mm for Delta
    # save_dir = "/Users/hanjunjie/Gap1/汇报/Image/20241219_Centipede_ZWD"
    save_dir = "./"
    Fixed = False
    show = False
    all = False
    time_type = "GPST"
    delta_xlabel = 72
    sigma = 3
    sigma_num = 0
    delay_model = 0
    legend = False
    inter_zpd = True
    reconvergence = 0
    recon_list = [50]

    PlotZWD.Plot_MultiDay_timeseries_zwd(File_info=file_info_list,Start=start_time,End=end_time,Plot_type=plot_type,Ylim=ylim,Save_dir=save_dir,Fixed=Fixed,Show=show,All=all,Time_type = time_type,Delta_xlabel = delta_xlabel,Legend = legend,Sigma=sigma,Signum=sigma_num,Start_hour = start_hour,End_hour = end_hour, Inter_zpd = inter_zpd, Reconvergence = reconvergence, Recon_list=recon_list)
