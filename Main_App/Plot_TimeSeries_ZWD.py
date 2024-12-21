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
    ["/Users/hanjunjie/Gap1/ZWD_Retrieval_PPPRTK/Server/ZWD/PPP/2023080/client/KOS1-GEC3-FIXED-30.flt","/Users/hanjunjie/Gap1/Data/2023/ZTD/080/KOS10800.23zpd","PPPRTK"],
    ["/Users/hanjunjie/Gap1/ZWD_Retrieval_PPPRTK/Server/ZWD/PPP/2023080/client/BRUX-GEC3-FIXED-30.flt","/Users/hanjunjie/Gap1/Data/2023/ZTD/080/BRUX0800.23zpd","PPP"]
    ] #[Raw, Ref, Mode] #[file,mode]
# file_info_list = [
#     ["/Users/hanjunjie/Gap1/ZWD_Retrieval_PPPRTK/Project/2023080/client/BRUX-GEC3-FIXED-30-PPP-GRA-Bernese.flt","PPP"],
#     ["/Users/hanjunjie/Gap1/ZWD_Retrieval_PPPRTK/Project/2023080/client/BRUX-GEC3-FIXED-30-PPP-GRA.flt","PPPRTK"],
#     ["/Users/hanjunjie/Gap1/ZWD_Retrieval_PPPRTK/Project/2023080/BRUX0800.23zpd","REF"]
#     ] #[Raw, Ref, Mode] #[file,mode]

start_time = [2023,3,21,0,0,0]
end_time = [2023,3,21,23,0,0]
plot_type = "ZWD_DELTA" # ZWD_DELTA ZWD_RAW GRD_RAW GRD_DELTA
ylim = 0 # mm for Delta
save_dir = ""
fixed = False
show = True
all = False
time_type = "GPST"
delta_xlabel = 2
sigma = 3
sigma_num = 0
delay_model = 0
legend = False

PlotZWD.Plot_timeseries_zwd(File_info=file_info_list,Start=start_time,End=end_time,Plot_type=plot_type,Ylim=ylim,Save_dir=save_dir,Fixed=fixed,Show=show,All=all,Time_type = time_type,Delta_xlabel = delta_xlabel,Legend = legend,Sigma=sigma,Signum=sigma_num)