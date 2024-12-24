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
    ["/Users/hanjunjie/Gap1/ZWD_Retrieval_PPPRTK/Server/ZWD/PPP/2023080/client/BRUX-GEC3-FIXED-30-3600.flt","/Users/hanjunjie/Gap1/Data/2023/ZTD/080/BRUX0800.23zpd","Server"],
    ["/Users/hanjunjie/Gap1/ZWD_Retrieval_PPPRTK/Project/2023080/client/BRUX-GEC3-FIXED-30-3600-LSQ.flt","/Users/hanjunjie/Gap1/Data/2023/ZTD/080/BRUX0800.23zpd","Raw"],
    ["/Users/hanjunjie/Gap1/ZWD_Retrieval_PPPRTK/Project/2023080/client/BRUX-GEC3-FIXED-30-3600-LSQ-MeanBug.flt","/Users/hanjunjie/Gap1/Data/2023/ZTD/080/BRUX0800.23zpd","Test1"],
    ["/Users/hanjunjie/Gap1/ZWD_Retrieval_PPPRTK/Project/2023080/client/BRUX-GEC3-FIXED-30-3600-LSQ-MeanBug-5MIN.flt","/Users/hanjunjie/Gap1/Data/2023/ZTD/080/BRUX0800.23zpd","Test2"],
    ["/Users/hanjunjie/Gap1/ZWD_Retrieval_PPPRTK/Project/2023080/client/BRUX-GEC3-FIXED-30-3600-LSQ-MAX.flt","/Users/hanjunjie/Gap1/Data/2023/ZTD/080/BRUX0800.23zpd","Test3"],
    # ["/Users/hanjunjie/Gap1/ZWD_Retrieval_PPPRTK/Server/ZWD/PPPRTK/2023080/client/BRUX-GEC3-FIXED-30-3600.flt","/Users/hanjunjie/Gap1/Data/2023/ZTD/080/BRUX0800.23zpd","Test"],
    ] #[Raw, Ref, Mode] #[file,mode]
# file_info_list = [
#     ["/Users/hanjunjie/Gap1/ZWD_Retrieval_PPPRTK/Server/ZWD/PPPRTK/2023080/client/BRUX-GEC3-FIXED-30-3600.flt","Server"],
#     ["/Users/hanjunjie/Gap1/ZWD_Retrieval_PPPRTK/Project/2023080/client/BRUX-GEC3-FIXED-30-3600-RAW.flt","Mac"],
#     ["/Users/hanjunjie/Gap1/Data/2023/ZTD/080/BRUX0800.23zpd","REF"]
#     ] #[Raw, Ref, Mode] #[file,mode]

start_time = [2023,3,21,2,0,0]
end_time = [2023,3,21,24,0,0]
plot_type = "ZWD_DELTA" # ZWD_DELTA ZWD_RAW GRD_RAW GRD_DELTA
ylim = 200 # mm for Delta
save_dir = ""
fixed = False
show = True
all = False
time_type = "GPST"
delta_xlabel = 1
sigma = 3
sigma_num = 0
delay_model = 0
legend = False
inter_zpd = True
reconvergence = 3600
recon_list = [50]

# PlotZWD.Plot_timeseries_zwd(File_info=file_info_list,Start=start_time,End=end_time,Plot_type=plot_type,Ylim=ylim,Save_dir=save_dir,Fixed=fixed,Show=show,All=all,Time_type = time_type,Delta_xlabel = delta_xlabel,Legend = legend,Sigma=sigma,Signum=sigma_num)
PlotZWD.Plot_MultiDay_timeseries_zwd(File_info=file_info_list,Start=start_time,End=end_time,Plot_type=plot_type,Ylim=ylim,Save_dir=save_dir,Fixed=fixed,Show=show,All=all,Time_type = time_type,Delta_xlabel = delta_xlabel,Legend = legend,Sigma=sigma,Signum=sigma_num,Inter_zpd=inter_zpd,Reconvergence=3600,Recon_list=recon_list)