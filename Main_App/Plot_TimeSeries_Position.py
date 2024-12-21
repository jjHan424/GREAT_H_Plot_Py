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
    # ["/Users/hanjunjie/Gap1/ZWD_Retrieval_PPPRTK/Project/2021162/client/GAMG-GEC3-FLOAT-30-WUM-ULTRALSP3.flt", "GAMG", "WUM1"],
    # ["/Users/hanjunjie/Gap1/ZWD_Retrieval_PPPRTK/Project/2021162/client/GAMG-GEC3-FLOAT-30-WUM-KIN.flt", "GAMG", "WUM-GEC"],
    ["/Users/hanjunjie/Gap1/ZWD_Retrieval_PPPRTK/Server/ZWD_KINEMATIC/PPPRTK/2023073/client/TIT2-GEC3-FIXED-30-3600.flt", "TIT2", "PPP"],
    ["/Users/hanjunjie/Gap1/ZWD_Retrieval_PPPRTK/Server/ZWD/PPPRTK/2023073/client/TIT2-GEC3-FIXED-30-3600.flt", "TIT2", "PPPRTK"],
    # ["/Users/hanjunjie/Gap1/ZWD_Retrieval_PPPRTK/Server/ZWD/PPP/2023073/client/KOS1-GEC3-FIXED-30-3600.flt", "BRUX", "GFZ"],
    # ["/Users/hanjunjie/Gap1/ZWD_Retrieval_PPPRTK/Project/2024282/client/GAMG-GEC3-FLOAT-30.flt", "GAMG", "GFZ-GEC"],
    # ["/Users/hanjunjie/Gap1/ZWD_Retrieval_PPPRTK/Project/2021162/client/GAMG-GEC3-FLOAT-30-GFZ-KIN.flt", "GAMG", "GFZ-GEC"],
    # ["/Users/hanjunjie/Gap1/ZWD_Retrieval_PPPRTK/Project/2021162/client/GAMG-GEC3-FLOAT-30-COD-KIN.flt", "GAMG", "COD"],
    # ["/Users/hanjunjie/Gap1/ZWD_Retrieval_PPPRTK/Project/2023341/server/HKSC-GEC2-FIXED-30.flt", "HKSC", "NONE"],
    ] #[filedir, station_name, mode_name] for static station // #[filedir, ref_file, mode_name] for dynamic station
start_time = [2023,3,14,2,0,0]
end_time = [2023,3,15,0,0,0]
plot_type = ["E","N","U"]
ylim = 0.4
save_dir = ""
show = True
fixed = False
all = False
mean = True
time_type = "GPST"
delta_xlabel = 1
sigma = 3
sigma_num = 0
#Setup Statistics
delta_data = 30
reconvergence = 3600
recon_list = [2,5,10]

PlotPOS.Plot_timeseries_position(File_info=file_info_list,Start=start_time,End=end_time,Plot_type=plot_type,Ylim=ylim,Save_dir=save_dir,Show=show,Fixed=fixed,All=all,Time_type = time_type,Delta_xlabel = delta_xlabel,Mean=mean,Sigma=sigma,Signum=sigma_num,Delta_data=delta_data,Reconvergence=reconvergence,Recon_list=recon_list)



