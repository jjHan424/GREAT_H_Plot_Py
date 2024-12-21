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

EPN_file = "/Users/hanjunjie/Gap1/ZWD_Retrieval_PPPRTK/EPN_SITE/EPN_GEC.crd"
Centipede_file = "/Users/hanjunjie/Gap1/ZWD_Retrieval_PPPRTK/CRDSITE/CMNC_ALL.crd"

crd_data_epn = PlotBasemap.load_data(EPN_file,[])
crd_data_centipede = PlotBasemap.load_data(Centipede_file,[])

B_epn,L_epn = [],[]
for cur_site in crd_data_epn.keys():
    B_epn.append(crd_data_epn[cur_site]["BLH"][0])
    L_epn.append(crd_data_epn[cur_site]["BLH"][1])
B_max,B_min,L_max,L_min = np.array(B_epn).max(),np.array(B_epn).min(),np.array(L_epn).max(),np.array(L_epn).min()

site_list = []
dis_min_list = []
country_list = {}
min_lon,max_lat, = 98.8,26.6
max_lon,min_lat, = 103.8,21.4
cent_list  = []
for cur_site in crd_data_centipede.keys():
    B_cen = (crd_data_centipede[cur_site]["BLH"][0])
    L_cen = (crd_data_centipede[cur_site]["BLH"][1])
    min_dis = 99999
    if B_cen < max_lat and B_cen > min_lat and L_cen < max_lon and L_cen > min_lon:
        cent_list.append(cur_site)
    else:
        continue
    # if "UM980" not in crd_data_centipede[cur_site]["SYS"]:
    #     continue
    # if crd_data_centipede[cur_site]["Location"] == "FRA" or crd_data_centipede[cur_site]["Location"] == "BEL":
    #     for cur_site_epn in crd_data_epn.keys():
    #         B_epn = (crd_data_epn[cur_site_epn]["BLH"][0])
    #         L_epn = (crd_data_epn[cur_site_epn]["BLH"][1])
    #         cur_dis = math.sqrt((B_cen - B_epn) * (B_cen - B_epn) + (L_cen - L_epn) * (L_cen - L_epn))
    #         if cur_dis < min_dis:
    #             min_dis = cur_dis
    #             site_pair = cur_site + "-" + cur_site_epn
    #     site_list.append(site_pair)
    #     dis_min_list.append(min_dis)
print(cent_list)
np_dis_min = np.array(dis_min_list)
np_dis_min.sort() 
np_dis_min_raw = np.array(dis_min_list)
np_site_list = np.array(site_list)
epn_list,cen_list = [],[]
# for i in range(30):
#     index = np_dis_min_raw == np_dis_min[i]
#     cur_site_pair = np_site_list[index][0]
#     if cur_site_pair.split("-")[1] not in epn_list:
#         epn_list.append(cur_site_pair.split("-")[1])
#     if cur_site_pair.split("-")[0] not in cen_list:
#         cen_list.append(cur_site_pair.split("-")[0])
#     print(np_dis_min[i])
#     print(crd_data_centipede[cur_site_pair.split("-")[0]]["SYS"])
# print(epn_list)
# print(cen_list)

min_lon,max_lat, = 0.7145,49.1308
max_lon,min_lat, = 0.7145+1.5*5,49.1308 - 1.5*4
# central grid
cur_lon,cur_lat = 74.6241 - 5,53.5023 + 5
cur_grid_site_list = []
for i in range(14):
    cur_lon = cur_lon + 5
    # cur_lat = 49.1308 + 1.5
    cur_lat = 53.5023 + 5
    for j in range(9):
        cur_lat = cur_lat - 5
        min_dis = 9999
        for cur_site in crd_data_centipede:
            B_cur,L_cur = crd_data_centipede[cur_site]["BLH"][0],crd_data_centipede[cur_site]["BLH"][1]
            if math.sqrt((B_cur-cur_lat) * (B_cur-cur_lat) + (L_cur - cur_lon)*(L_cur - cur_lon)) < min_dis:
                min_dis = math.sqrt((B_cur-cur_lat) * (B_cur-cur_lat) + (L_cur - cur_lon)*(L_cur - cur_lon))
                cur_grid_site = cur_site
        if cur_grid_site not in cur_grid_site_list:
            cur_grid_site_list.append(cur_grid_site)
print(cur_grid_site_list)


