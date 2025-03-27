import os
import sys

# from networkx import project
sys.path.insert(0,os.path.dirname(__file__)+'/../LibBase')
sys.path.insert(0,os.path.dirname(__file__)+'/../LibPlot')
from matplotlib.colors import Normalize
import numpy as np
import readfile as rf
import matplotlib as mpl
from matplotlib.colorbar import ColorbarBase
mpl.use("TkAgg")
import matplotlib.pyplot as plt
import dataprocess as dp
import draw as dr
#import seaborn as sns
import trans as tr
import Lib_Plot_Basemap as PlotBasemap
import Lib_Plot_ROTI as PlotROTI
from mpl_toolkits.basemap import Basemap
from datetime import datetime
font_title = {'family' : 'Arial', 'weight' : 300, 'size' : 15}

roti_dir = "/Users/hanjunjie/Gap1/Magnetic_storm/Server/ROTI"
shp_file = ["/Users/hanjunjie/tools/GREAT_H_Plot_Py/SysFile/Shp_File/world-administrative-boundaries/world-administrative-boundaries"]
save_dir = "/Users/hanjunjie/Gap1/汇报/Image/MagneticStorm2/IPP_ROTI_Map_20240511_North"
all_file = os.listdir(roti_dir)
all_site_data = {}
max_roti = 1.5
min_roti = 0
cur_start = [2024,5,11,0,0,0]
while cur_start[3] < 24:
    date = datetime(cur_start[0],cur_start[1],cur_start[2],cur_start[3],cur_start[4],cur_start[5])
    for cur_file in all_file:
        if cur_file[8:11] != "132":
            continue
        roti_file = os.path.join(roti_dir,cur_file)
        all_data = {}
        all_data = {}
        all_data["ROTI"] = {}
        PlotROTI.load_data_roti(roti_file,all_data=all_data, data_type = "ROTI" , start_week = 0, Time = cur_start)
        all_site_data[cur_file[0:4]] = all_data
    fig = plt.figure(figsize=(8,7))
    # map = Basemap(llcrnrlon=-180, llcrnrlat=-90, urcrnrlon=180, urcrnrlat=90, resolution='c',projection='cyl')
    # PlotBasemap.setlabeltick_global(map,[0,0,0,0,0,0],0)
    map = Basemap(projection='nplaea',boundinglat=0.1,lon_0=0,resolution='i')
    map.readshapefile(shp_file[0],'states',drawbounds=True)
    map.drawmeridians(np.arange(-180,180,15),labels=[1, 0, 0, 1], fontsize = 15,fmt = '%d$^\circ$',)
    map.drawparallels(np.arange(0,75,15))
    # plt.xticks([0,1],[0,1],size = 15)
    lat_list,lon_list,roti_list = [],[],[]
    map.nightshade(date)
    for cur_site in all_site_data.keys():
        for cur_time in all_site_data[cur_site]["ROTI"].keys():
            for cur_sat in all_site_data[cur_site]["ROTI"][cur_time].keys():
                lat,lon = all_site_data[cur_site]["ROTI"][cur_time][cur_sat]["Lat"],all_site_data[cur_site]["ROTI"][cur_time][cur_sat]["Lon"]
                roti = all_site_data[cur_site]["ROTI"][cur_time][cur_sat]["ROTI"]
                ele = all_site_data[cur_site]["ROTI"][cur_time][cur_sat]["Ele"]
                if ele < 30:
                    continue
                lat_list.append(lat)
                lon_list.append(lon)
                roti_list.append(roti)
                
    # max_roti = np.array(roti_list).max()
    # min_roti = np.array(roti_list).min()
    # print("Min = {:.2f}, Max = {:.2f}".format(min_roti,max_roti))
    for i in range(len(lat_list)):
        norm_heat_value =(roti_list[i] - min_roti) / (max_roti - min_roti)
        heat_color = plt.cm.jet(norm_heat_value)
        map.tissot(lon_list[i],lat_list[i],1,100,facecolor=heat_color)
    plt.title("{}-{:0>2}-{:0>2} {:0>2}:{:0>2}:{:0>2}".format(cur_start[0],cur_start[1],cur_start[2],cur_start[3],cur_start[4],cur_start[5]),font_title)
    for i in range(len(shp_file)):
        map.readshapefile(shp_file[i],'states',drawbounds=True)

    norm = Normalize(vmin = min_roti,vmax=max_roti)
    cax = plt.axes([0.89,0.1,0.015,0.8]) #left down width height
    cb = ColorbarBase(cax,cmap = plt.cm.jet,norm=norm,orientation='vertical')
    cb.set_label('ROTI (TECU/min)',fontsize=15,fontname="Arial")
    cb.set_ticks([0,0.3,0.6,0.9,1.2,1.5])
    cb.set_ticklabels([0,0.3,0.6,0.9,1.2,1.5],fontsize=15,fontname="Arial")
    plt.savefig(os.path.join(save_dir,"{}-{:0>2}-{:0>2}_{:0>2}:{:0>2}:{:0>2}.jpg".format(cur_start[0],cur_start[1],cur_start[2],cur_start[3],cur_start[4],cur_start[5])),dpi=600)
    plt.close()
    cur_start[4] = cur_start[4] + 5
    if cur_start[4] == 60:
        cur_start[3] = cur_start[3] + 1
        cur_start[4] = 0


