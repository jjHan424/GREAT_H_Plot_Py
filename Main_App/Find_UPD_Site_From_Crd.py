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
import math

crd_file = "/Users/hanjunjie/Gap1/ZWD_Retrieval_PPPRTK/Site_CRD_New/EPN_ALL.crd"
sys_list = {"G":["L1","L2"],"E":["L1","L5","L7"],"C":["L2","L6","L7"]}
crd_data = PlotBasemap.load_data(crd_file,[],sys_list)
space_resolution = 4.5
[minLon,minLat,maxLon,maxLat, count_lat, count_lon] = PlotBasemap.define_grid(crd_data,space_resolution)
site_list = []
site_str = ""
for i in range(count_lat):
    for j in range(count_lon):
        cur_lat,cur_lon = maxLat - i*space_resolution,minLon + j*space_resolution
        min_dis = 999999999
        cur_min_dis_site = ""
        for cur_site in crd_data.keys():
            BLH = crd_data[cur_site]["BLH"]
            cur_dis = math.sqrt((BLH[0]-cur_lat)*(BLH[0]-cur_lat)+(BLH[1]-cur_lon)*(BLH[1]-cur_lon))
            if cur_dis < min_dis:
                cur_min_dis_site = cur_site
                min_dis = cur_dis
        if cur_min_dis_site not in site_list:
            site_list.append(cur_min_dis_site)
            site_str = site_str+"_"+cur_min_dis_site

print(site_list)
print(site_str)