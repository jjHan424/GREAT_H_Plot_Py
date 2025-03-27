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
import Lib_Plot_Position as PlotPOS


#Setup Plot
site_list = ['ACSO', 'ALBH', 'ALGO', 'AMC4', 'BAIE', 'BAMF', 'BARH', 'BILL', 'BLYT', 'BREW', 'CAGS', 'CHUR', 'CHWK', 'CIT1', 'CMP9', 'COSO', 'CRFP', 'DHLG', 'DRAO', 'DUBO', 'EPRT', 'ESCU', 'FLIN', 'FRDN', 'GODE', 'GODN', 'GODS', 'GODZ', 'GOL2', 'GOLD', 'HLFX', 'HNPT', 'HOLB', 'HOLP', 'JPLM', 'KSU1', 'KUJ2', 'MDO1', 'MONP', 'MRC1', 'NAIN', 'NANO', 'NIST', 'NLIB', 'NRC1', 'P043', 'P051', 'P053', 'P389', 'P779', 'P802', 'PICL', 'PIE1', 'PIN1', 'PRDS', 'QUIN', 'ROCK', 'SASK', 'SCH2', 'SCIP', 'SFDM', 'SGPO', 'SHE2', 'SNI1', 'STFU', 'STJ3', 'STJO', 'STPM', 'TABL', 'TORP', 'TRAK', 'UCAL', 'UCLP', 'UCLU', 'UNB3', 'UNBD', 'UNBJ', 'UNBN', 'USN7', 'USN8', 'USN9', 'VALD', 'VNDP', 'WDC5', 'WDC6', 'WES2', 'WHC1', 'WIDC', 'WILL', 'WLSN']

file_dir = "/Users/hanjunjie/Gap1/汇报/Image/MagneticStorm2/FLT114"
path_list = os.listdir(file_dir)
site_list_new = []
# for cur_site in path_list:
#     if cur_site[0] == ".":
#         continue
#     site_list_new.append(cur_site[0:4])
# print(site_list_new)
for cur_site in site_list:
    if cur_site[0] == ".":
        continue
    cur_site = cur_site[0:4]
    file_info_list = [
        ["/Users/hanjunjie/Gap1/Magnetic_storm/Server/FLT_KIN/132/{}-GEC3-FLOAT-30.flt".format(cur_site), cur_site, cur_site]
        ] #[filedir, station_name, mode_name] for static station // #[filedir, ref_file, mode_name] for dynamic station
    start_time = [2024,5,11,0,0,0]
    end_time = [2024,5,11,24,0,0]
    plot_type = ["E","N","U","NSAT"]
    ylim = 3
    save_dir = "/Users/hanjunjie/Gap1/汇报/Image/MagneticStorm2/FLT132"
    show = False
    fixed = False
    all = False
    mean = False
    time_type = "GPST"
    delta_xlabel = 2
    sigma = 3
    sigma_num = 0
    #Setup Statistics
    delta_data = 30
    reconvergence = 3600
    recon_list = [10]
    PlotPOS.Plot_timeseries_position(File_info=file_info_list,Start=start_time,End=end_time,Plot_type=plot_type,Ylim=ylim,Save_dir=save_dir,Show=show,Fixed=fixed,All=all,Time_type = time_type,Delta_xlabel = delta_xlabel,Mean=mean,Sigma=sigma,Signum=sigma_num,Delta_data=delta_data,Reconvergence=reconvergence,Recon_list=recon_list)



