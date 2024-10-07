import os
import sys
sys.path.insert(0,os.path.dirname(__file__)+'/../LibPlot')
sys.path.insert(0,os.path.dirname(__file__)+'/../LibBase')
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

PlotPOS.TRUE_Position

#Setup
file_info_list = [
    ["/Users/hanjunjie/Master_3/1-IUGG/ResFromServer/CLIENT/FLT_CROSS/2021272/HKCL-GEC2-FIXED-0-30.flt","HKCL","111"],
    ["/Users/hanjunjie/Master_3/1-IUGG/ResFromServer/CLIENT/FLT_CROSS/2021272/HKCL-GEC2-FIXED-0-30.flt","HKCL","222"],
    ] #[filedir,station_name,mode_name]
start_time = [2021,9,29,2,0,0]
end_time = [2021,9,29,24,0,0]
plot_type = ["E","N","U"]
show = True
save_dir = ""
