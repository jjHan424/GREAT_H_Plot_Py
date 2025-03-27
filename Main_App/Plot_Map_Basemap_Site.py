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
import Lib_Plot_Basemap as PlotBasemap

# crd_file = "/Users/hanjunjie/Gap1/ZWD_Retrieval_PPPRTK/CRDSITE/CMNC_ALL.crd"
crd_file = "/Users/hanjunjie/Phd_1/0. GREAT/HJX/_PPPRTK/station.crd"
# crd_file = "/Users/hanjunjie/Gap1/ZWD_Retrieval_PPPRTK/CRDSITE/CHN_HK_16.crd"

shp_file = ["/Users/hanjunjie/tools/GREAT_H_Plot_Py/SysFile/Shp_File/gadm36_CHN_shp/gadm36_CHN_3"]

site_group = {
           "1":["N052"]
              } 
sys_list = {}
show = True
space_resolution = 0.1
site_group = {}
sys_list = {}
PlotBasemap.Plot_basemap_site(CRD_file = crd_file, SHP_file = shp_file, Site_group = site_group, Space_resolution = space_resolution, Sys_list = sys_list)



