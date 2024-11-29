from math import ceil
import os
import sys
from turtle import width
from numpy import size
sys.path.insert(0,os.path.dirname(__file__)+'/..')
sys.path.insert(0,os.path.dirname(__file__)+'/../..')
import folium
from folium.features import DivIcon
import matplotlib.pyplot as plt
import webbrowser
import trans as tr
import glv
# import readfile as rf
# from shapely.ops import triangulate
# from shapely import wkt
import math
import matplotlib as mpl
import numpy as np
from folium.plugins import HeatMap
import seaborn as sns
from mpl_toolkits.basemap import Basemap
from adjustText import adjust_text
from matplotlib.colors import Normalize
from matplotlib.colorbar import ColorbarBase
font_title = {'family' : 'Arial', 'weight' : 300, 'size' : 10}
font_label = {'family' : 'Arial', 'weight' : 300, 'size' : 15}
font_label_new = {'family' : 'Arial', 'size' : 15}
font_tick = {'family' : 'Arial', 'weight' : 300, 'size' : 35}
font_legend = {'family' : 'Arial', 'weight' : 300, 'size' : 30}
# font_legend = {'family' : 'Times New Roman', 'weight' : 600, 'size' : 15}
font_text = {'family' : 'Arial','weight' : 300,'size'   : 15}
tick_size = 15
color_list = ["#0099E5","#34BF49","#FF4C4C"]
# color_list = ["#0085c3","#7ab800","#71c6c1","#dc5034","#009bbb",
#               "#b7295a","#6e2585","#f2af00","#5482ab","#ce1126",
#               "#444444","#eeeeee"]

def load_data(CRD_file,site_list = []):
    crd_data,B,L = {},[],[]
    with open(CRD_file,'rt') as f:
        for line in f:
            value = line.split()
            if value[len(value)-1] == "False":
                continue
            if len(site_list) > 0 and value[0] not in site_list:
                continue
            crd_data[value[0]] = {}
            xyz = [float(value[1]),float(value[2]),float(value[3])]
            crd_data[value[0]]["XYZ"] = xyz
            blh = tr.xyz2blh(xyz[0],xyz[1],xyz[2])
            blh = [blh[0] / glv.deg,blh[1] / glv.deg,blh[2]]
            if blh[1] > 180:
                blh = [blh[0],blh[1] - 360,blh[2]]
            crd_data[value[0]]["BLH"] = blh
            B.append(blh[0])
            L.append(blh[1])
            crd_data[value[0]]["SYS"] = ""
            for i in range(len(value)-1):
                if i >= 4:
                    crd_data[value[0]]["SYS"] = crd_data[value[0]]["SYS"] + value[i]
            crd_data[value[0]]["VALUE"] = value[len(value)-1]
            # if blh[0] < 54.8 or blh[0] > 58.8 or blh[1] < 9 or blh[1] > 16.5:
            #     del crd_data[value[0]]
    return crd_data

def define_grid(Crd_data, Space_resolution):
    B,L = [],[]
    for cur_site in Crd_data.keys():
        B.append(Crd_data[cur_site]["BLH"][0])
        L.append(Crd_data[cur_site]["BLH"][1])
    B,L = np.array(B),np.array(L)
    delta_Lat = B.max() - B.min()
    delta_Lon = L.max() - L.min()
    num_lat = 1 - (delta_Lat / Space_resolution - int(delta_Lat / Space_resolution))
    num_lon = 1 - (delta_Lon / Space_resolution - int(delta_Lon / Space_resolution))
    maxLat = B.max() + num_lat * Space_resolution / 2.0
    minLat = B.min() - num_lat * Space_resolution / 2.0
    minLon = L.min() - num_lon * Space_resolution / 2.0
    maxLon = L.max() + num_lon * Space_resolution / 2.0
    cur_Lat = maxLat
    cur_Lon = minLon
    print("Top Left Corner : ({:>.4f},{:>.4f})".format(minLon,maxLat))
    return ([minLon,minLat,maxLon,maxLat, math.ceil(delta_Lat / Space_resolution), math.ceil(delta_Lon / Space_resolution)])

def setlabeltick(map,corner_grid,space_resolution):
    map.drawparallels(circles=np.linspace(corner_grid[1], corner_grid[3], corner_grid[4] + 1),labels=[0, 0, 0, 0], color='gray',fontsize = tick_size,linewidth=0.5)
    map.drawmeridians(meridians=np.linspace(corner_grid[0], corner_grid[2], corner_grid[5] + 1),labels=[0, 0, 0, 0], color='gray',fontsize = tick_size,linewidth=0.5)
    xlabellon,xlabeltext = [], []
    cur_label = corner_grid[0]
    for i in range(corner_grid[5] + 1):
        xlabellon.append(cur_label)
        xlabeltext.append('%.1f$^\circ$E'%(cur_label))
        cur_label = cur_label + space_resolution
    ylabellat,ylabeltext = [], []
    cur_label = corner_grid[1]
    for i in range(corner_grid[4] + 1):
        ylabellat.append(cur_label)
        ylabeltext.append('%.1f$^\circ$N'%(cur_label))
        cur_label = cur_label + space_resolution
    plt.yticks(ylabellat,ylabeltext,size = tick_size)
    plt.xticks(xlabellon,xlabeltext,size = tick_size)

def scatter_map_mark(map,crd_data = {},Site_group = {}):
    #=== Plot Marker ===#
    if len(Site_group) == 0:
        Site_group[0] = []
        for cur_site in crd_data.keys():
            Site_group[0].append(cur_site)
    elif len(Site_group) == 1:
        for cur_group in Site_group.keys():
            if cur_group == "Client":
                Site_group[0] = []
                for cur_site in crd_data.keys():
                    if cur_site in Site_group["Client"]:
                        continue
                    Site_group[0].append(cur_site)
                break
    
    index_color = -1
    for cur_group in Site_group.keys():
        index_color = index_color + 1
        for cur_site in Site_group[cur_group]:
            if cur_group == "Client":
                map.scatter(crd_data[cur_site]["BLH"][1],crd_data[cur_site]["BLH"][0],marker='*',s=200,facecolor='#FF4C4C',edgecolor='k', linewidth=1)
            else:
                map.scatter(crd_data[cur_site]["BLH"][1],crd_data[cur_site]["BLH"][0],marker='v',s=100,facecolor=color_list[index_color%3],edgecolor="k", linewidth=1)

def write_map_mark_name(map,crd_data):
    texts=[]
    for cur_site in crd_data.keys():
        texts.append(plt.text(crd_data[cur_site]["BLH"][1],crd_data[cur_site]["BLH"][0],cur_site,fontdict=font_text))
    adjust_text(texts)

def Plot_basemap_site(CRD_file = "", SHP_file = [], Site_group = {}, Show = True, Space_resolution = 0.1):
    #=== Load Data ===#
    site_list = []
    for cur_group in Site_group.keys():
        if cur_group == "Client":
            continue
        for cur_site in Site_group[cur_group]:
            site_list.append(cur_site)
    crd_data = load_data(CRD_file,site_list)
    #=== Statistics ===#
    corner_grid = define_grid(crd_data, Space_resolution)
    #=== Plot ===#
    fig = plt.figure(figsize=(corner_grid[5]+1,corner_grid[4]+1))
    # set range
    map = Basemap(llcrnrlon=corner_grid[0], llcrnrlat=corner_grid[1], urcrnrlon=corner_grid[2], urcrnrlat=corner_grid[3], resolution='c',projection='cyl')
    # set lables & ticks
    setlabeltick(map,corner_grid,Space_resolution)
    # plot site
    scatter_map_mark(map,crd_data,Site_group)
    # Marker Name
    write_map_mark_name(map,crd_data)
    # load shp file
    for i in range(len(SHP_file)):
        map.readshapefile(SHP_file[i],'states',drawbounds=True)
    plt.show()