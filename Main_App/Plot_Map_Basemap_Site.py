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
crd_file = "/Users/hanjunjie/Gap1/ZWD_Retrieval_PPPRTK/Site_CRD_New/ALL.crd"
# crd_file = "/Users/hanjunjie/Gap1/ZWD_Retrieval_PPPRTK/CRDSITE/CHN_HK_16.crd"

shp_file = ["/Users/hanjunjie/tools/GREAT_H_Plot_Py/SysFile/Shp_File/world-administrative-boundaries/world-administrative-boundaries"]

site_group = {
              "EPN":['SHOE', 'BRUX', 'MAN2', 'DENT', 'IGNF', 'REDU', 'VFCH', 'DOUR', 'VLIS', 'WARE', 'AUTN', 'LIL2', 'HERT', 'MLVL'],
              "Client":["ENSG"]
              } 
# sys_list = {"G":["L1","L2"],"E":["L1","L5","L7"],"C":["L2","L6","L7"]}
show = True
space_resolution = 1
# site_group = {1:['TLSG', 'TLMF', 'PUYV', 'TLSE', 'CREU', 'BCLN', 'EBRE', 'LLIV', 'CASE', 'ESCO', 'EGLT', 'BELL', 'UEAU']}
sys_list = {}
PlotBasemap.Plot_basemap_site(CRD_file = crd_file, SHP_file = shp_file, Site_group = site_group, Space_resolution = space_resolution, Sys_list = sys_list)



