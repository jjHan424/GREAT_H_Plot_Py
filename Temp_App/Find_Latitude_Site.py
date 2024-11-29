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

import Lib_Plot_Basemap as PlotBasemap

crd_file = PlotBasemap.load_data("/Users/hanjunjie/Gap1/ZWD_Retrieval_PPPRTK/EPN_SITE/EPN_GEC.crd")
delta_lat = 5

lat_list,site_list = [],[]
for cur_site in crd_file.keys():
    lat_list.append(crd_file[cur_site]["BLH"][0])
    site_list.append(cur_site)
np_lat_list = np.array(lat_list)
np_site_list = np.array(site_list)

min_lat = np_lat_list.min()
max_lat = np_lat_list.max()

site_select = []
ref_como = "BBYS"
# site_select.append(np_site_list[np_lat_list==min_lat][0])
# site_select.append(np_site_list[np_lat_list==max_lat][0])

# cur_lat = min_lat + delta_lat

# while cur_lat < max_lat:
#     diff_lat_list = np.abs(np_lat_list-cur_lat)
#     site_select.append(np_site_list[diff_lat_list==diff_lat_list.min()][0])
#     cur_site = np_site_list[diff_lat_list==diff_lat_list.min()][0]
#     diff_lat_list[diff_lat_list==diff_lat_list.min()] = 100
#     site_select.append(np_site_list[diff_lat_list==diff_lat_list.min()][0])
#     cur_site = cur_site + "-" + np_site_list[diff_lat_list==diff_lat_list.min()][0]
#     cur_lat = cur_lat + delta_lat
#     print(cur_site)
# print(site_select)

ref_blh = crd_file[ref_como]["BLH"]
max_b,min_b,max_l,min_l = ref_blh[0] + delta_lat, ref_blh[0] - delta_lat, ref_blh[1] + delta_lat, ref_blh[1] - delta_lat
for cur_site in site_list:
    # if crd_file[cur_site]["BLH"][0] >= min_b and crd_file[cur_site]["BLH"][0] <= max_b and crd_file[cur_site]["BLH"][1] >= min_l and crd_file[cur_site]["BLH"][1] <= max_l:
    #     site_select.append(cur_site)
    if crd_file[cur_site]["BLH"][0] >= 25 and crd_file[cur_site]["BLH"][0] <= 40:
        site_select.append(cur_site)
lon_list = []
for cur_site in site_select:
    lon_list.append(crd_file[cur_site]["BLH"][1])
min_lon,max_lon = np.array(lon_list).min(),np.array(lon_list).max()
cur_min_lon = min_lon
site_max_num = {}
while cur_min_lon + delta_lat*2 <= max_lon:
    if cur_min_lon not in site_max_num.keys():
        site_max_num[cur_min_lon] = []
    for cur_site in site_select:
        if crd_file[cur_site]["BLH"][1] >= cur_min_lon and crd_file[cur_site]["BLH"][1] <= cur_min_lon + delta_lat*2:
            site_max_num[cur_min_lon].append(cur_site)
    cur_min_lon = cur_min_lon+delta_lat/2
max_num = 0
for cur_lon in site_max_num.keys():
    if len(site_max_num[cur_lon]) > max_num:
        max_num_lon = cur_lon
        max_num = len(site_max_num[cur_lon])
print(site_max_num[max_num_lon])
