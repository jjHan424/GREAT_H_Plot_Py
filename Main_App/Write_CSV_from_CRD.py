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
import csv

crd_file = "/Users/hanjunjie/Gap1/ZWD_Retrieval_PPPRTK/Site_CRD_New/Centipete_France_40.crd"
csv_file_in = "/Users/hanjunjie/tools/generate_xml_great/sys_file/EUREF_Permanent_GNSS_Network_NEW.csv"
csv_file_out = "/Users/hanjunjie/Gap1/ZWD_Retrieval_PPPRTK/Site_CRD_New/Centipete_ALL.csv"
with open(csv_file_out,'a') as f:
    f.write("\"Name\",\"Latitude\",\"Longitude\",\"Elevation\",\"X\",\"Y\",\"Z\"\n")

crd_data = PlotBasemap.load_data(crd_file,[],{})
file = open(csv_file_in)
site_list_csv = csv.DictReader(file)
for cur_dic in site_list_csv:
    for cur_site_short in crd_data:
        if cur_site_short.upper() in cur_dic["Name"]:
            crd_data[cur_site_short]["LongName"] = cur_dic["Name"]

for cur_site in crd_data.keys():
    with open(csv_file_out,'a') as f:
        f.write("\"{}\",\"{:.4f}\",\"{:.4f}\",\"{:.4f}\",\"{:.4f}\",\"{:.4f}\",\"{:.4f}\"\n".\
                format(cur_site,crd_data[cur_site]["BLH"][0],crd_data[cur_site]["BLH"][1],crd_data[cur_site]["BLH"][2],
                       crd_data[cur_site]["XYZ"][0],crd_data[cur_site]["XYZ"][1],crd_data[cur_site]["XYZ"][2]))

