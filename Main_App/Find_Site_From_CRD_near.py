import os
from re import S
import sys
from turtle import color
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
import glv
import math

import Lib_Plot_Basemap as PlotBasemap

crd_file = "/Users/hanjunjie/Gap1/ZWD_Retrieval_PPPRTK/Site_CRD_New/EPN_ALL.crd"
sys_list = {"G":["L1","L2"],"E":["L1","L5","L7"],"C":["L2","L6","L7"]}

crd_data = PlotBasemap.load_data(crd_file,[],sys_list)
central_site = "UEAU"
space_resolution = 1
grid_count = 6
site_list = []
str_site = ""
if central_site in crd_data.keys():
    BLH_central = crd_data[central_site]["BLH"]
    for cur_site in crd_data.keys():
        # if cur_site == central_site:
        #     continue
        cur_BLH = crd_data[cur_site]["BLH"]
        delta_B,delta_L = math.fabs(BLH_central[0] - cur_BLH[0]),math.fabs(BLH_central[1] - cur_BLH[1])
        if delta_B <= grid_count*space_resolution/2 and delta_L <= grid_count*space_resolution/2 and cur_BLH[1] > 0:
            site_list.append(cur_site)
            str_site = str_site + "_" + cur_site

print(site_list)
print(str_site)