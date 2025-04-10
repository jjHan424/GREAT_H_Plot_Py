import os
import sys
sys.path.insert(0,os.path.join(os.path.dirname(__file__), '..', 'LibBase'))
sys.path.insert(0,os.path.join(os.path.dirname(__file__), '..', 'LibPlot'))
import numpy as np
import matplotlib as mpl
mpl.use("TkAgg")
import matplotlib.pyplot as plt
import Lib_Plot_Position as PlotPOS
# from LibPlot import Lib_Plot_Position as PlotPOS


#Setup Plot
# site_list = ['ACSO', 'ALBH', 'ALGO', 'AMC4', 'BAIE', 'BAMF', 'BARH', 'BILL', 'BLYT', 'BREW', 'CAGS', 'CHUR', 'CHWK', 'CIT1', 'CMP9', 'COSO', 'CRFP', 'DHLG', 'DRAO', 'DUBO', 'EPRT', 'ESCU', 'FLIN', 'FRDN', 'GODE', 'GODN', 'GODS', 'GODZ', 'GOL2', 'GOLD', 'HLFX', 'HNPT', 'HOLB', 'HOLP', 'JPLM', 'KSU1', 'KUJ2', 'MDO1', 'MONP', 'MRC1', 'NAIN', 'NANO', 'NIST', 'NLIB', 'NRC1', 'P043', 'P051', 'P053', 'P389', 'P779', 'P802', 'PICL', 'PIE1', 'PIN1', 'PRDS', 'QUIN', 'ROCK', 'SASK', 'SCH2', 'SCIP', 'SFDM', 'SGPO', 'SHE2', 'SNI1', 'STFU', 'STJ3', 'STJO', 'STPM', 'TABL', 'TORP', 'TRAK', 'UCAL', 'UCLP', 'UCLU', 'UNB3', 'UNBD', 'UNBJ', 'UNBN', 'USN7', 'USN8', 'USN9', 'VALD', 'VNDP', 'WDC5', 'WDC6', 'WES2', 'WHC1', 'WIDC', 'WILL', 'WLSN']
site_list = ["DAV1"]
file_dir = "/Users/hanjunjie/Gap1/汇报/Image/MagneticStorm2/FLT114"
# path_list = os.listdir(file_dir)
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
    start_time = [2024,6,13,3,0,0]
    end_time = [2024,6,13,24,0,0]
    file_info_list = [
        # [r"E:\PhD_1\4.RTZTD\BNC\BCN_RINEX\2024160\0crd_250331_01DRNX",cur_site,"BNC"],
        # [r"E:\PhD_1\4.RTZTD\BNC\BCN_RINEX\2024160\0crd_250402_01DRNX_05S_WHUSSR_2024160",cur_site,"OLD"],
        #[r"E:\PhD_1\4.RTZTD\BNC\BCN_RINEX\2024160\0crd_250403_AMB_CLK_OFF",cur_site,"NE_OLD"],
        # [r"E:\PhD_1\4.RTZTD\BNC\BCN_RINEX\2024160\0crd_250405",cur_site,"BNC"],
        # [r"E:\PhD_1\4.RTZTD\GREAT\2024160\result\WHU-RTS-DARW-PPP_sta_DF_Float_161_IF_05M.flt",cur_site,"30S"],
                    #   [r"E:\PhD_1\4.RTZTD\BNC\DARW00AUS_20250970000_01D_01S.ppp",cur_site,"1S"],
                    #   [r"E:\PhD_1\4.RTZTD\BNC\DARW00AUS_20250910000_01D_01S.ppp",cur_site,"EC"],
                    #   [r"E:\1Gap_1\HJX\hjx\client_ZWD\TUBO-GEC.flt",cur_site,"GEC"],
                    #   [r"E:\PhD_1\4.RTZTD\BNC\BCN_RINEX\2024160\0crd\DAV100ATA_20241650000_01D_05M_NEWEPH.ppp",cur_site,"OLD"],
                    #   [r"E:\PhD_1\4.RTZTD\BNC\BCN_RINEX\2024160\0crd\DAV100ATA_20241650000_01D_05M_CNE.ppp",cur_site,"OLD"],
                      [r"E:\PhD_1\4.RTZTD\BNC\DARW00AUS_20251000000_01D_05M.ppp",cur_site,"NEW"]
                    ]
    plot_type = ["E","N","U"]
    ylim = 0
    save_dir = "/Users/hanjunjie/Gap1/汇报/Image/MagneticStorm2/FLT132"
    show = True
    fixed = False
    all = True
    mean = True
    time_type = "GPST"
    delta_xlabel = 3
    sigma = 3
    sigma_num = 0
    #Setup Statistics
    delta_data = 30
    reconvergence = 3600
    recon_list = []
    PlotPOS.Plot_timeseries_position(File_info=file_info_list,Start=start_time,End=end_time,Plot_type=plot_type,Ylim=ylim,Save_dir=save_dir,Show=show,Fixed=fixed,All=all,Time_type = time_type,Delta_xlabel = delta_xlabel,Mean=mean,Sigma=sigma,Signum=sigma_num,Delta_data=delta_data,Reconvergence=reconvergence,Recon_list=recon_list)



