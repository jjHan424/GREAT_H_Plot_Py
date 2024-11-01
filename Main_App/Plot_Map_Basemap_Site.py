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

crd_file = "/Users/hanjunjie/Gap1/ZWD_Retrieval_PPPRTK/EPN_SITE/EPN_GEC.crd"
shp_file = ["./SysFile/Shp_File/gadm36_HKG_shp/gadm36_HKG_0","./SysFile/Shp_File/gadm36_CHN_shp/gadm36_CHN_0"]
site_group = {"1":["PASA","SCOA","TLMF","TLSG","TLSE","ESCO","LLIV","BELL","EBRE","CREU","CASE",]} #{"Group":[site1,site2]}
show = True
space_resolution = 0.5
PlotBasemap.Plot_basemap_site(CRD_file = crd_file, SHP_file = shp_file, Site_group = site_group, Space_resolution = space_resolution)



