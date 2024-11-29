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
# shp_file = ["./SysFile/Shp_File/gadm36_HKG_shp/gadm36_HKG_0","./SysFile/Shp_File/gadm36_CHN_shp/gadm36_CHN_0"]
shp_file = ["./SysFile/Shp_File/world-administrative-boundaries/world-administrative-boundaries"]
# site_group = {"1":["BADH","BRUX","BUDD","BUDP","DENT","DIEP","DILL","DOUR","EIJS","EUSK","FFMJ","GOET","HAS6","HOBU","IJMU","JON6","KARL","KLOP","KOS1","ONS1","ONSA","PTBB","REDU","SPT0","SPT7","SULD","TERS","TIT2","VAE6","WARE","WSRT"]} #{"Group":[site1,site2]}
site_group = {"1":['ALAC', 'ALBA', 'ALME', 'COBA', 'HUEL', 'SONS']}
# site_group = {"1":['MAS1', 'NABG', 'LPAL', 'NICO', 'ALME', 'ANK2', 'ELBA', 'BRMF', 'BBYS', 'LODZ', 'RANT', 'JON6', 'LEK6', 'UME6', 'ARJ6', 'KEV2', 'SCOR', 'WUTH', 'NYA1']}
# site_group = {"1":["MAS1","LPAL", "NICO", "ALME", "ANK2", "ELBA", "BRMF", "BBYS", "LODZ", "RANT", "JON6", "LEK6", "UME6", "ARJ6", "KEV2", "WUTH", "NYA1", "NABG"],
#               "2":["IZAN", "ALME", "SONS", "ESCO", "COMO", "MLVL", "VLN1", "SAS2", "SPT0", "OST6", "OVE6", "TRO1", "VARS", "NYAL"]}
# site_group = {"1":"MAS1_NABG_LPAL_IZAN_NICO_ALME_ALME_RAEG_ANK2_SONS_ELBA_ESCO_BRMF_COMO_BBYS_MLVL_LODZ_VLN1_RANT_SAS2_JON6_SPT0_LEK6_QAQ1_UME6_OST6_ARJ6_OVE6_KEV2_TRO1_SCOR_VARS_WUTH_NYA1_NYA1_NYAL".split("_")}
show = True
space_resolution = 0.5
PlotBasemap.Plot_basemap_site(CRD_file = crd_file, SHP_file = shp_file, Site_group = site_group, Space_resolution = space_resolution)



