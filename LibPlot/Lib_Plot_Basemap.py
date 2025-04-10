from math import ceil
import os
import sys
from turtle import width
from numpy import size
sys.path.insert(0,os.path.join(os.path.dirname(__file__),'..'))
sys.path.insert(0,os.path.join(os.path.dirname(__file__),'..','..'))
sys.path.insert(0,os.path.join(os.path.dirname(__file__),'..','LibBase'))
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

def load_data(CRD_file,site_list = [],Sys_list = {}):
    crd_data,B,L = {},[],[]
    with open(CRD_file,'rt') as f:
        for line in f:
            value = line.split()
            if value[len(value)-1] == "False":
                continue
            if len(site_list) > 0 and value[0] not in site_list:
                continue
            xyz = [float(value[1]),float(value[2]),float(value[3])]
            # if xyz[0] == 0.0:
            #     continue
            crd_data[value[0]] = {}
            crd_data[value[0]]["VALUE"] = value[len(value)-1]
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
            cur_sys_list = {}
            for i in range(len(value)-1):
                if i >= 4:
                    # crd_data[value[0]]["SYS"] = crd_data[value[0]]["SYS"] + value[i]
                    value_list = value[i].split(",")
                    if value_list[0][0] not in cur_sys_list:
                        cur_sys_list[value_list[0][0]] = []
                    for cur_value in value_list:
                        cur_sys_list[value_list[0][0]].append(cur_value[-2:])
            for cur_sys in cur_sys_list:
                crd_data[value[0]]["SYS"] = crd_data[value[0]]["SYS"] + cur_sys
            if len(Sys_list) > 0:
                for cur_sys in Sys_list:
                    if cur_sys in cur_sys_list:
                        for cur_band in Sys_list[cur_sys]:
                            if cur_band not in cur_sys_list[cur_sys]:
                                crd_data[value[0]]["VALUE"] = "False"
                    else:
                        crd_data[value[0]]["VALUE"] = "False"
            if len(Sys_list) > 0:
                if len(cur_sys_list) != len(Sys_list):
                    crd_data[value[0]]["VALUE"] = "False"
            # if blh[0] < 54.8 or blh[0] > 58.8 or blh[1] < 9 or blh[1] > 16.5:
            #     del crd_data[value[0]]
    return crd_data

def load_data_caster(CRD_file,site_list = []):
    crd_data,B,L = {},[],[]
    with open(CRD_file,'rt') as f:
        for line in f:
            value = line.split(";")
            if len(site_list) > 0 and value[1] not in site_list:
                continue
            # if value[8] != "BEL":
            #     continue
            crd_data[value[1]] = {}
            # xyz = [float(value[1]),float(value[2]),float(value[3])]
            # crd_data[value[0]]["XYZ"] = xyz
            blh = [float(value[9]),float(value[10]),0]
            # blh = [blh[0] / glv.deg,blh[1] / glv.deg,blh[2]]
            if blh[1] > 180:
                blh = [blh[0],blh[1] - 360,blh[2]]
            crd_data[value[1]]["BLH"] = blh
            B.append(blh[0])
            L.append(blh[1])
            crd_data[value[1]]["SYS"] = line
            crd_data[value[1]]["Location"] = value[8]
            # if blh[0] < 54.8 or blh[0] > 58.8 or blh[1] < 9 or blh[1] > 16.5:
            #     del crd_data[value[0]]
    return crd_data

def define_grid(Crd_data, Space_resolution):
    B,L = [],[]
    for cur_site in Crd_data.keys():
        if Crd_data[cur_site]["VALUE"] == "False":
            continue
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

def setlabeltick_global(map,corner_grid,space_resolution):
    corner_grid[0],corner_grid[2],corner_grid[5] = -180,180,24
    corner_grid[1],corner_grid[3],corner_grid[4] = -90,90,12
    map.drawparallels(circles=np.linspace(corner_grid[1], corner_grid[3], corner_grid[4] + 1),labels=[0, 0, 0, 0], color='gray',fontsize = tick_size,linewidth=0.5)
    map.drawmeridians(meridians=np.linspace(corner_grid[0], corner_grid[2], corner_grid[5] + 1),labels=[0, 0, 0, 0], color='gray',fontsize = tick_size,linewidth=0.5)
    xlabellon,xlabeltext1,xlabeltext2 = [], [], []
    cur_label = corner_grid[0]
    space_resolution = 15
    for i in range(corner_grid[5] + 1):
        xlabellon.append(cur_label)
        if i%2==0:
            xlabeltext1.append('%.1f$^\circ$E'%(cur_label))
            xlabeltext2.append('')
            
        else:
            xlabeltext2.append('%.1f$^\circ$E'%(cur_label))
            xlabeltext1.append('')
        cur_label = cur_label + space_resolution
    ylabellat,ylabeltext = [], []
    cur_label = corner_grid[1]
    space_resolution = 15
    for i in range(corner_grid[4] + 1):
        ylabellat.append(cur_label)
        ylabeltext.append('%.1f$^\circ$N'%(cur_label))
        cur_label = cur_label + space_resolution
    plt.yticks(ylabellat,ylabeltext,size = tick_size)
    plt.xticks(xlabellon,xlabeltext1,size = tick_size)

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
    marker_list = ['v','v','v']
    legend_list = [0,0,0]
    for cur_group in Site_group.keys():
        index_color = index_color + 1
        for cur_site in Site_group[cur_group]:
            if cur_site not in crd_data.keys():
                continue
            if crd_data[cur_site]["VALUE"] == "False":
                continue
            if cur_group == "Client":
                map.scatter(crd_data[cur_site]["BLH"][1],crd_data[cur_site]["BLH"][0],marker='*',s=200,facecolor='#34BF49',edgecolor='k', linewidth=1)
            else:
                index_color = 0
                # if crd_data[cur_site]["SYS"] == "GEC":
                #     index_color = 0
                # if crd_data[cur_site]["SYS"] == "GE":
                #     index_color = 1
                # if crd_data[cur_site]["SYS"] == "G":
                #     index_color = 2
                legend_list[index_color] = map.scatter(crd_data[cur_site]["BLH"][1],crd_data[cur_site]["BLH"][0],marker=marker_list[index_color],s=100,facecolor=color_list[index_color%3],edgecolor="k", linewidth=1)
    
    # plt.legend((legend_list[0],legend_list[1],legend_list[2]),["GEC","GE","G"],prop = font_text,framealpha=0,facecolor='none',ncol=4,numpoints=5,markerscale=1, 
    #         borderaxespad=0,bbox_to_anchor=(1,1.1),loc=1)

def write_map_mark_name(map,crd_data):
    texts=[]
    for cur_site in crd_data.keys():
        if crd_data[cur_site]["VALUE"] == "False":
            continue
        if cur_site[0] != "N":
            continue
        texts.append(plt.text(crd_data[cur_site]["BLH"][1],crd_data[cur_site]["BLH"][0],cur_site,fontdict=font_text))
    adjust_text(texts)

def Plot_basemap_site(CRD_file = "", SHP_file = [], Site_group = {}, Show = True, Space_resolution = 0.1, Sys_list = {}):
    #=== Load Data ===#
    site_list = []
    for cur_group in Site_group.keys():
        # if cur_group == "Client":
        #     continue
        for cur_site in Site_group[cur_group]:
            site_list.append(cur_site)
    crd_data = load_data(CRD_file,site_list,Sys_list)
    # crd_data_1 = load_data_caster(CRD_file[1],site_list)
    # crd_data.update(crd_data_1)
    #=== Statistics ===#
    corner_grid = define_grid(crd_data, Space_resolution)
    #=== Plot ===#
    fig = plt.figure(figsize=(corner_grid[5]+1,corner_grid[4]+1))
    # fig = plt.figure(figsize=(12,15))
    # set range
    map = Basemap(llcrnrlon=corner_grid[0], llcrnrlat=corner_grid[1], urcrnrlon=corner_grid[2], urcrnrlat=corner_grid[3], resolution='c',projection='cyl')
    # map = Basemap(llcrnrlon=-180, llcrnrlat=-90, urcrnrlon=180, urcrnrlat=90, resolution='c',projection='cyl')
    # map.shadedrelief(scale=1)
    # set lables & ticks
    setlabeltick(map,corner_grid,Space_resolution)
    # setlabeltick_global(map,corner_grid,Space_resolution)
    # plot site
    scatter_map_mark(map,crd_data,Site_group)
    # Marker Name
    write_map_mark_name(map,crd_data)
    # load shp file
    for i in range(len(SHP_file)):
        map.readshapefile(SHP_file[i],'states',drawbounds=True)
    plt.show()