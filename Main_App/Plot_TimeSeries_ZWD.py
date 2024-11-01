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
    ["/Users/hanjunjie/Gap1/ZWD_Retrieval_PPPRTK/Plot_test/EBRE-GE-FIXED-30.flt","/Users/hanjunjie/Gap1/ZWD_Retrieval_PPPRTK/Plot_test/ebre3100.21zpd","EBRE"],
    ["/Users/hanjunjie/Gap1/ZWD_Retrieval_PPPRTK/Plot_test/KOS1-GE-FIXED-30.flt","/Users/hanjunjie/Gap1/ZWD_Retrieval_PPPRTK/Plot_test/kos13100.21zpd","KOS1"]
    ] #[Raw, Ref, Mode] #[file,mode]
# file_info_list = [
#     ["/Users/hanjunjie/Gap1/ZWD_Retrieval_PPPRTK/Plot_test/KOS1-GE-FIXED-30.flt","PPP-RTK"],
#     ["/Users/hanjunjie/Gap1/ZWD_Retrieval_PPPRTK/Plot_test/kos13100.21zpd","REF"]
#     ] #[Raw, Ref, Mode] #[file,mode]

start_time = [2021,11,6,2,0,0]
end_time = [2021,11,6,24,0,0]
plot_type = "DELTA" # DELTA RAW
ylim = 20 # mm for Delta
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

PlotZWD.Plot_timeseries_zwd(File_info=file_info_list,Start=start_time,End=end_time,Plot_type=plot_type,Ylim=ylim,Save_dir=save_dir,Fixed=fixed,Show=show,All=all,Time_type = time_type,Delta_xlabel = delta_xlabel,Legend = legend,Sigma=sigma,Signum=sigma_num)