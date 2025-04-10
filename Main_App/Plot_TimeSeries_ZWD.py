import os
import sys
sys.path.insert(0,os.path.dirname(__file__)+'/../LibBase')
sys.path.insert(0,os.path.dirname(__file__)+'/../LibPlot')
import numpy as np
import readfile as rf
import matplotlib as mpl
mpl.use("TkAgg")
import matplotlib.pyplot as plt
#import seaborn as sns
import Lib_Plot_ZWD as PlotZWD

#Setup Plot
file_info_list = [
    # [r"E:\PhD_1\4.RTZTD\BNC\BCN_RINEX\2024160\0crd\UPC1WHURTS_20241610000_01D_30S_DARW00AUS_TRO_SAVE.TRO",r"E:\PhD_1\4.RTZTD\Data\ZTD\161\IGS0OPSFIN_20241610000_01D_05M_DARW00AUS_TRO.TRO","OLD"],
     [r"E:\PhD_1\4.RTZTD\BNC\UPC1WHURTS_20250970000_01D_05S_DARW00AUS_TRO.TRO",r"E:\PhD_1\4.RTZTD\BNC\UPC1WHURTS_20250970000_01D_05M_DARW00AUS_TRO.TRO","GREAT"],
    #  [r"E:\PhD_1\4.RTZTD\BNC\BCN_RINEX\2024160\0crd\UPC1CNERTS_20241610000_01D_30S_DARW00AUS_TRO.TRO",r"E:\PhD_1\4.RTZTD\Data\ZTD\161\IGS0OPSFIN_20241610000_01D_05M_DARW00AUS_TRO.TRO","BNC"],
    ] #[Raw, Ref, Mode] #[file,mode]
# file_info_list = [
#     [r"E:\PhD_1\4.RTZTD\BNC\UPC1CNERTS_20250960000_01D_05S_DARW00AUS_TRO.TRO","1S"],
#     [r"E:\PhD_1\4.RTZTD\BNC\UPC1CNERTS_20250960000_01D_05M_DARW00AUS_TRO.TRO","5M"],
#     # [r"E:\PhD_1\4.RTZTD\Data\ZTD\161\IGS0OPSFIN_20241610000_01D_05M_DARW00AUS_TRO.TRO","REF"]
#     ] #[Raw, Ref, Mode] #[file,mode]

start_time = [2025,4,7,0,0,0]
end_time = [2025,4,7,10,0,0]
plot_type = "ZWD_DELTA" # ZWD_DELTA ZWD_RAW GRD_RAW GRD_DELTA
ylim = 0 # mm for Delta
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
inter_zpd = False
reconvergence = 3600
recon_list = [50]

# PlotZWD.Plot_timeseries_zwd(File_info=file_info_list,Start=start_time,End=end_time,Plot_type=plot_type,Ylim=ylim,Save_dir=save_dir,Fixed=fixed,Show=show,All=all,Time_type = time_type,Delta_xlabel = delta_xlabel,Legend = legend,Sigma=sigma,Signum=sigma_num)
PlotZWD.Plot_MultiDay_timeseries_zwd(File_info=file_info_list,Start=start_time,End=end_time,Plot_type=plot_type,Ylim=ylim,Save_dir=save_dir,Fixed=fixed,Show=show,All=all,Time_type = time_type,Delta_xlabel = delta_xlabel,Legend = legend,Sigma=sigma,Signum=sigma_num,Inter_zpd=inter_zpd,Reconvergence=3600,Recon_list=recon_list)