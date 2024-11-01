# from asyncore import write
# from msilib.schema import File
from multiprocessing.dummy import DummyProcess
import os
from socket import SHUT_WR
import sys
from turtle import st
sys.path.insert(0,os.path.dirname(__file__)+'/../LibBase')
from matplotlib.markers import MarkerStyle
import numpy as np
import matplotlib as mpl
mpl.use("TkAgg")
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import scienceplots
plt.style.use(['science','grid','no-latex'])
# plt.style.use('science')
from numpy.core.fromnumeric import shape, size
import dataprocess as dp
import matplotlib.colors as colors
# from matplotlib.pyplot import MultipleLocator
import seaborn as sns
import math
import trans as tr
import glv
import os
from mpl_toolkits.axes_grid1.inset_locator import mark_inset
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

## Position of Station (GREAT PPP-AR)
TRUE_Position = {
           "HKSC":[-2414267.6526,5386768.7552,2407459.7917],"HKTK":[-2418093.0695,5374658.0963,2430428.9388],"HKMW":[-2402484.8351,5395262.2062,2400726.7172],
           "HKCL":[-2392741.6793,5397562.8528,2404757.6381],"HKKS":[-2429526.6128,5377816.4032,2412152.4833],"HKKT":[-2405144.6258,5385195.0303,2420032.2957],
           "HKLM":[-2414046.6682,5391602.1234,2396878.6406],"HKLT":[-2399063.4601,5389237.6196,2417326.8134],"HKNP":[-2392360.9915,5400226.0468,2400094.2194],
           "HKOH":[-2423817.6243,5386056.8703,2399883.1266],"HKPC":[-2405183.7237,5392541.5974,2403645.4824],"HKSL":[-2393383.1399,5393860.9488,2412592.1665],
           "HKSS":[-2424425.8236,5377187.9503,2418617.5000],"HKST":[-2417143.5996,5382345.2556,2415036.7024],"HKWS":[-2430579.7341,5374285.4508,2418956.0864],
           "T430":[-2411015.9437,5380265.4823,2425132.4516],"WUDA":[-2267761.1226,5009370.8398,3220970.5620],"WHYJ":[-2252813.6375,4973121.8230,3286531.2991],
           "N028":[-2191056.9474,5053129.9334,3205815.9843],"N004":[-2334707.5108,5037347.5734,3128918.7498],"N047":[-2350716.9193,4955782.5391,3244265.6248],
           "N068":[-2222210.0878,4963941.9216,3320986.9437],"WHDS":[-2309234.0723,4998958.4644,3207719.1445],"WHSP":[-2277732.7853,5031747.7356,3179072.7779],
           "WHXZ":[-2299689.3578,4975638.9471,3250284.4212],"XGXN":[-2220831.1399,5007544.3179,3256075.5381],"A010":[-2175297.1093,4330326.1005,4133584.2591],
           "K042":[-2132034.8536,4509248.5850,3961882.4343],"K057":[-2061539.3542,4485887.5744,4026181.9595],"K059":[-2211742.6097,4402276.4734,4037240.8884],
           "K101":[-2044552.7122,4330957.9318,4200451.9052],"V092":[-1980661.4288,4556162.0565,3989739.6921],"K070":[-2059482.5470,4437621.0251,4080017.7148],
           "BADH":[4042497.5659,612081.7044,4879251.2303],  "BRUX":[4027881.3392,306998.7821,4919499.0337],  "DENT":[4020711.2694,238851.3971,4928949.8416],
           "DIEP":[3842152.8088,563402.1405,5042888.5845],  "DILL":[4132892.1699,485479.4990,4817740.6194],  "DOUR":[4086777.9038,328452.2746,4869782.8018],
           "EIJS":[4023086.0205,400395.3754,4916655.7137],  "EUSK":[4022105.9791,477011.3654,4910840.9136],  "FFMJ":[4053455.6195,617729.9429,4869395.8771],
           "GOET":[3918911.7136,687523.9448,4968545.6512],  "HOBU":[3778219.5166,698635.7021,5074054.3750],  "IJMU":[3882052.7400,309346.7059,5034330.5759],
           "KARL":[4146524.1169,613138.3527,4791517.3498],  "KLOP":[4041875.1891,620655.5731,4878636.9929],  "KOS1":[3899613.4338,397362.1268,5014739.0067],
           "PTBB":[3844059.6900,709661.5900,5023129.7146],  "REDU":[4091423.1110,368380.8769,4863179.9641],  "TERS":[3798580.3478,346994.3368,5094781.1586],
           "TIT2":[3993787.0349,450204.1864,4936131.8507],  "WARE":[4031946.9452,370151.3253,4911906.1508],  "WSRT":[3828735.5991,443305.2281,5064884.8827]
           }

#=== FONT SET ===#
font_title = {'family' : 'Arial', 'weight' : 300, 'size' : 30}
font_label = {'family' : 'Arial', 'weight' : 300, 'size' : 20}
font_tick = {'family' : 'Arial', 'weight' : 300, 'size' : 35}
font_legend = {'family' : 'Arial', 'weight' : 300, 'size' : 20}
# font_legend = {'family' : 'Times New Roman', 'weight' : 600, 'size' : 15}
font_text = {'family' : 'Arial','weight' : 300,'size'   : 20}
xtick_size = 20
color_list = ["#0099E5","#34BF49","#FF4C4C"]
# color_list = ["#0085c3","#7ab800","#71c6c1","#dc5034","#009bbb",
#               "#b7295a","#6e2585","#f2af00","#5482ab","#ce1126",
#               "#444444","#eeeeee"]

def loaddata(File_name = "", Start = [], End = []):
    #Judge the Head
    file = open(File_name,"r")
    first_line = next(file)
    file.close()
    first_value = first_line.split()
    if first_value[0] == r"%EPO":
        AllData = loaddata_lsq(File_name,Start,End)
    else:
        AllData = loaddata_flt(File_name,Start,End)
    return AllData

def loaddata_flt(File_name = "", Start = [], End = []):
    all_data={}
    soweek_last = 0
    w_last = 0
    head_end = False
    epoch_flag = True
    with open(File_name,'rt') as f:
        for line in f:
            value = line.split()
            if line[0] == " ":
                soweek = float(value[0])
                if (soweek + w_last*604800 < soweek_last):
                    w_last = w_last + 1
                soweek = soweek + w_last*604800
                soweek_last = soweek
                #soweek = hour + minute/60.0 + second/3600.0
                if soweek not in all_data.keys():
                    all_data[soweek]={}
                all_data[soweek]['X'] = float(value[1])
                all_data[soweek]['Y'] = float(value[2])
                all_data[soweek]['Z'] = float(value[3])
                all_data[soweek]['NSAT'] = float(value[13])
                all_data[soweek]['PDOP'] = float(value[14])
                all_data[soweek]['Q'] = float(value[18])
                if value[16] == 'Fixed' and all_data[soweek]['Q']  == 1:
                    all_data[soweek]['AMB'] = 1
                else:
                    all_data[soweek]['AMB'] = 0
                if all_data[soweek]['PDOP'] > 5:
                    all_data[soweek]['AMB'] = 0
                
    return all_data

def loaddata_lsq(File_name = "", Start = [], End = []):
    all_data={}
    w_last = 0
    head_end = False
    with open(File_name,'rt') as f:
        for line in f:
            value = line.split()
            if line[0] == '%':
                head_end = True
                continue
            if head_end:
                ymd = value[1]
                hms = value[2]
                year = float(ymd[0:4])
                month = float(ymd[5:7])
                day = float(ymd[8:10])
                hour = float(hms[0:2])
                minute = float(hms[3:5])
                second = float(hms[6:12])
                [w,soweek] = tr.ymd2gpst(year,month,day,hour,minute,second)
                if (w_last==0):
                    w_last = w
                soweek = soweek + (w-w_last)*604800
                #soweek = hour + minute/60.0 + second/3600.0
                if soweek not in all_data.keys():
                    all_data[soweek]={}
                all_data[soweek]['X'] = float(value[5])
                all_data[soweek]['Y'] = float(value[6])
                all_data[soweek]['Z'] = float(value[7])
                all_data[soweek]['CLK'] = float(value[11])
                all_data[soweek]['NSAT'] = float(value[13])
                all_data[soweek]['GDOP'] = float(value[15])
                all_data[soweek]['PDOP'] = float(value[16])
                if value[17] == 'Fixed':
                    all_data[soweek]['AMB'] = 1
                else:
                    all_data[soweek]['AMB'] = 0
                
    return all_data

def loaddata_ref_IE(filename):
    all_data={}
    soweek_last = 0
    w_last = 0
    head_end = False
    epoch_flag = True
    with open(filename,'rt') as f:
        for line in f:
            value = line.split()
            if line[0] != "%":
                soweek = float(value[1])
                if (soweek < soweek_last):
                    w_last = w_last + 1
                soweek = soweek + w_last*604800
                soweek_last = soweek
                #soweek = hour + minute/60.0 + second/3600.0
                if soweek not in all_data.keys():
                    all_data[soweek]={}
                all_data[soweek]['X'] = float(value[2])
                all_data[soweek]['Y'] = float(value[3])
                all_data[soweek]['Z'] = float(value[4])
                all_data[soweek]['Q'] = float(value[5])
                all_data[soweek]['NSAT'] = float(value[5])
                all_data[soweek]['PDOP'] = float(value[5])
                if value[27] == 'Fixed':
                    all_data[soweek]['AMB'] = 1
                else:
                    all_data[soweek]['AMB'] = 0
                
    return all_data

def XYZ2ENU_static(XYZ = {},REF_XYZ = []):
    all_data = {}
    xyz = []
    ref_xyz = REF_XYZ

    for time in XYZ.keys():
        if time not in all_data:
            all_data[time] = {}
            xyz.append(XYZ[time]["X"])
            xyz.append(XYZ[time]["Y"])
            xyz.append(XYZ[time]["Z"])
            enu = tr.xyz2enu(xyz,ref_xyz)
            xyz.clear()
            all_data[time]["E"] = enu[0]
            all_data[time]["N"] = enu[1]
            all_data[time]["U"] = enu[2]
            all_data[time]["X"] = XYZ[time]["X"]
            all_data[time]["Y"] = XYZ[time]["Y"]
            all_data[time]["Z"] = XYZ[time]["Z"]
            all_data[time]["NSAT"] = XYZ[time]["NSAT"]
            all_data[time]["PDOP"] = XYZ[time]["PDOP"]
            all_data[time]["AMB"] = XYZ[time]["AMB"]
    return all_data

def XYZ2ENU_dynamic(XYZ = {},REF_FILE = ""):
    REF_XYZ = loaddata_ref_IE(REF_FILE)
    all_data = {}
    xyz = []
    ref_xyz = []
    for time in XYZ.keys():
        if time not in all_data and time in REF_XYZ.keys():
            if REF_XYZ[time]["AMB"] != 1:
                continue
            all_data[time] = {}
            xyz.append(XYZ[time]["X"])
            xyz.append(XYZ[time]["Y"])
            xyz.append(XYZ[time]["Z"])
            ref_xyz.append(REF_XYZ[time]["X"])
            ref_xyz.append(REF_XYZ[time]["Y"])
            ref_xyz.append(REF_XYZ[time]["Z"])
            enu = tr.xyz2enu(xyz,ref_xyz)
            xyz.clear()
            ref_xyz.clear()
            all_data[time]["E"] = enu[0]
            all_data[time]["N"] = enu[1]
            all_data[time]["U"] = enu[2]
            all_data[time]["NSAT"] = XYZ[time]["NSAT"]
            all_data[time]["PDOP"] = XYZ[time]["PDOP"]
            all_data[time]["AMB"] = XYZ[time]["AMB"]
    return all_data

def edit_sigma(All_Data, Sigma, Signum):
    type_list = ["E","N","U"]
    type_list_all = ["E","N","U","NSAT","PDOP","AMB","TIME"]
    for cur_key in All_Data.keys():
        Signum_temp = Signum
        while Signum_temp >= 1:
            index_rm_all = np.full((len(All_Data[cur_key]["E"])),False)
            for i in range(len(type_list)):
                np_list = np.array(All_Data[cur_key][type_list[i]])
                std = np.std(np_list)
                mean = np.std(np_list)
                np_list_mean = np.abs(np_list-mean)
                index_rm = np_list_mean > std*Sigma
                index_rm_all = index_rm_all | index_rm
            for i in range(len(type_list_all)):
                All_Data[cur_key][type_list_all[i]] = np.delete(All_Data[cur_key][type_list_all[i]],index_rm_all)
            Signum_temp = Signum_temp - 1
    return All_Data

def edit_mean(All_Data,Raw_Data):
    type_list = ["E","N","U"]
    for cur_mode in All_Data.keys():
        for cur_type in type_list:
            mean_temp = np.mean(All_Data[cur_mode][cur_type])
            All_Data[cur_mode][cur_type] = All_Data[cur_mode][cur_type] - mean_temp
            # Raw_Data[cur_mode][cur_type] = Raw_Data[cur_mode][cur_type] - mean_temp

def statistics(All_Data, Edit_Data, Delta_data, Start_time, Duration_time, Reconvergence, Recon_list, Show = True, Save_dir = ""):
    num_epoch = Duration_time*3600/Delta_data + 1
    statistics_value_edit,statistics_value_all = {},{}
    type_list = ["E","N","U","NSAT"]

    #=== RMS MEAN STD Fixed
    for cur_mode in Edit_Data:
        statistics_value_edit[cur_mode] = {}
        statistics_value_edit[cur_mode]["Integrality"] = len(Edit_Data[cur_mode]["E"]) / num_epoch
        fixed = np.array(Edit_Data[cur_mode]["AMB"])[np.array(Edit_Data[cur_mode]["AMB"]) == 1].size
        statistics_value_edit[cur_mode]["Fixed/Fixed+Float"] = fixed / len(Edit_Data[cur_mode]["E"])
        statistics_value_edit[cur_mode]["RMS"],statistics_value_edit[cur_mode]["MEAN"],statistics_value_edit[cur_mode]["STD"] = {},{},{}
        for cur_type in type_list:
            statistics_value_edit[cur_mode]["STD"][cur_type] = np.std(Edit_Data[cur_mode][cur_type])
            statistics_value_edit[cur_mode]["MEAN"][cur_type] = np.mean(Edit_Data[cur_mode][cur_type])
            statistics_value_edit[cur_mode]["RMS"][cur_type] = np.sqrt(np.mean(np.array(Edit_Data[cur_mode][cur_type])**2))
    for cur_mode in All_Data:
        statistics_value_all[cur_mode] = {}
        statistics_value_all[cur_mode]["Integrality"] = len(All_Data[cur_mode]["E"]) / num_epoch
        fixed = np.array(All_Data[cur_mode]["AMB"])[np.array(All_Data[cur_mode]["AMB"]) == 1].size
        statistics_value_all[cur_mode]["Fixed/Fixed+Float"] = fixed / len(All_Data[cur_mode]["E"])
        statistics_value_all[cur_mode]["RMS"],statistics_value_all[cur_mode]["MEAN"],statistics_value_all[cur_mode]["STD"] = {},{},{}
        for cur_type in type_list:
            statistics_value_all[cur_mode]["STD"][cur_type] = np.std(All_Data[cur_mode][cur_type])
            statistics_value_all[cur_mode]["MEAN"][cur_type] = np.mean(All_Data[cur_mode][cur_type])
            statistics_value_all[cur_mode]["RMS"][cur_type] = np.sqrt(np.mean(np.array(All_Data[cur_mode][cur_type])**2))
    #=== Reconvergence ===#
    # Set
    max_recon_time = 1800
    cont_continue = 20
    # Initialization
    con_horizontal,con_vertical,con_position = {},{},{}
    for cur_mode in Edit_Data.keys():
        if cur_mode not in con_horizontal.keys():
            con_horizontal[cur_mode],con_vertical[cur_mode],con_position[cur_mode] = {},{},{}
            for cur_accuracy in Recon_list:
                con_horizontal[cur_mode][cur_accuracy] = []
                con_vertical[cur_mode][cur_accuracy] = []
                con_position[cur_mode][cur_accuracy] = []
    # Start reconvergence
    if Reconvergence != 0:
        for cur_mode in Edit_Data.keys():
            time_np = np.array(Edit_Data[cur_mode]["TIME"])
            e_np,n_np,u_np = np.array(Edit_Data[cur_mode]["E"]),np.array(Edit_Data[cur_mode]["N"]),np.array(Edit_Data[cur_mode]["U"])
            horizontal = np.sqrt(e_np**2+n_np**2)*100
            vertical = np.abs(u_np)*100
            position = np.sqrt(e_np**2+n_np**2+u_np**2)*100
            cur_time = Start_time[3] * 3600
            # i = 0
            for i in range(int(Duration_time*3600 / Reconvergence)):
                for cur_accuracy in Recon_list:
                    cur_time = Start_time[3] * 3600 + i * Reconvergence
                    con_position_num,con_horizontal_num,con_vertical_num = 0,0,0
                    while cur_time < Start_time[3] * 3600 + (i+1) * Reconvergence:
                        find_time = time_np[time_np == cur_time/3600]
                        find_time_index = time_np == cur_time/3600
                        if find_time.size < 1:
                            cur_time = cur_time + Delta_data
                            continue
                        # 3D position
                        if position[find_time_index] < cur_accuracy:
                            if con_position_num < cont_continue:
                                con_position_num = con_position_num + 1
                        elif con_position_num < cont_continue:
                            con_position_num = 0
                        if con_position_num == cont_continue:
                            con_position[cur_mode][cur_accuracy].append(cur_time - (Start_time[3] * 3600 + i * Reconvergence) - Delta_data * (cont_continue-1))
                            con_position_num = 9999999
                        # vertival
                        if vertical[find_time_index] < cur_accuracy:
                            if con_vertical_num < cont_continue:
                                con_vertical_num = con_vertical_num + 1
                        elif con_vertical_num < cont_continue:
                            con_vertical_num = 0
                        if con_vertical_num == cont_continue:
                            con_vertical[cur_mode][cur_accuracy].append(cur_time - (Start_time[3] * 3600 + i * Reconvergence) - Delta_data * (cont_continue-1))
                            con_vertical_num = 9999999
                        # horizontal
                        if horizontal[find_time_index] < cur_accuracy:
                            if con_horizontal_num < cont_continue:
                                con_horizontal_num = con_horizontal_num + 1
                        elif con_horizontal_num < cont_continue:
                            con_horizontal_num = 0
                        if con_horizontal_num == cont_continue:
                            con_horizontal[cur_mode][cur_accuracy].append(cur_time - (Start_time[3] * 3600 + i * Reconvergence) - Delta_data * (cont_continue-1))
                            con_horizontal_num = 9999999
                        
                        if cur_time - (Start_time[3] * 3600 + i * Reconvergence) > max_recon_time:
                            if con_horizontal_num != 9999999:
                                con_horizontal[cur_mode][cur_accuracy].append(max_recon_time)
                            if con_position_num != 9999999:
                                con_position[cur_mode][cur_accuracy].append(max_recon_time)
                            if con_vertical_num != 9999999:
                                con_vertical[cur_mode][cur_accuracy].append(max_recon_time)
                            break
                        cur_time = cur_time + Delta_data
    
    #===Print Statistical Value===#
    # Static Value Raw
    Static_print = statistics_value_edit
    type_enu = ["E","N","U"]
    # print("{:>23}".format("E-N-U"))
    for cur_type in type_enu:
        print(cur_type)
        print("{:<15}".format("Mode") + "{:>7}".format("RMS(cm)") + \
                                         "{:>14}".format("MEAN(cm)") + \
                                         "{:>14}".format("STD(cm)"))
        for cur_mode in Static_print.keys():
            Str_temp = "{:<15}".format(cur_mode) + "{:>7.2f}".format(Static_print[cur_mode]["RMS"][cur_type]*100) + \
                                                "{:>14.2f}".format(Static_print[cur_mode]["MEAN"][cur_type]*100) + \
                                                "{:>14.2f}".format(Static_print[cur_mode]["STD"][cur_type]*100)
            print(Str_temp)
        # print("\n")
    print("{}".format("RATE"))
    type_others = ["Integrality","Fixed/Fixed+Float","NSAT"]
    print("{:<15}".format("Mode") + "{:>7}".format("Inter") + \
                                         "{:>14}".format("Fixed") + \
                                         "{:>14}".format("NSAT"))
    for cur_mode in Static_print.keys():
        Str_temp = "{:<15}".format(cur_mode) + "{:>6.2f}%".format(Static_print[cur_mode]["Integrality"]*100) + \
                                            "{:>13.2f}%".format(Static_print[cur_mode]["Fixed/Fixed+Float"]*100) + \
                                            "{:>14.2f}".format(Static_print[cur_mode]["MEAN"]["NSAT"])
        print(Str_temp)
    # Print Revonvergence
    for cur_accuracy in Recon_list:
        print("{:>2}cm-RECONVERGENCE".format(cur_accuracy))
        print("{:<15}".format("Mode") + "{:>7}".format("Hor(s)") + \
                                         "{:>14}".format("Ver(s)") + \
                                         "{:>14}".format("3D(s)"))
        for cur_mode in con_position.keys():
            Str_temp = "{:<15}".format(cur_mode) + "{:>7}".format(int(np.mean(con_horizontal[cur_mode][cur_accuracy]))) + \
                                                "{:>14}".format(int(np.mean(con_vertical[cur_mode][cur_accuracy]))) + \
                                                "{:>14}".format(int(np.mean(con_position[cur_mode][cur_accuracy])))
            print(Str_temp)
        # for cur_mode in Static_print.keys():
    
    #===Save Statistical Value===#
    if not Show:
        file_save = Save_dir+".csv"
        while os.path.exists(file_save):
            random = np.random.randint(0, 99, 1)
            file_save = Save_dir+"-{:0>2}.csv".format(random[0])
        file = open(file_save,'a')
        head_str = "{:<10}{:>8}{:>8}{:>8}{:>8}{:>8}{:>8}".format("Mode,","Inter,","Fixed,","NSAT,","E,","N,","U,")
        for cur_accuracy in Recon_list:
            head_str = head_str+"{:>12},{:>12},{:>12},".format("{:0>2}-H".format(cur_accuracy),"{:0>2}-V".format(cur_accuracy),"{:0>2}-3D".format(cur_accuracy))
        head_str = head_str[:-1]
        file.write(head_str+"\n")
        for cur_mode in Static_print.keys():
            Mode_str = "{:<9},{:>6.1f}%,{:>6.1f}%,{:>7.2f},".format(cur_mode,\
                                                                    Static_print[cur_mode]["Integrality"]*100,
                                                                    Static_print[cur_mode]["Fixed/Fixed+Float"]*100,
                                                                    Static_print[cur_mode]["MEAN"]["NSAT"],
                                                                    )
            for cur_type in type_enu:
                Mode_str = Mode_str + "{:>7.2f},".format(Static_print[cur_mode]["RMS"][cur_type]*100)
            for cur_accuracy in Recon_list:
                Mode_str = Mode_str + "{:>12.2f},{:>12.2f},{:>12.2f},".format(int(np.mean(con_horizontal[cur_mode][cur_accuracy])),\
                                                                              int(np.mean(con_vertical[cur_mode][cur_accuracy])),
                                                                              int(np.mean(con_position[cur_mode][cur_accuracy])))

            file.write(Mode_str[:-1]+"\n")
        file.close()



    




def plot_E_N_U(Plot_Data = {}, Plot_type = [], Mode_list = [], Ylim = 0.5, XlabelSet = [], Show = True):
    #===Plot===#
    row = len(Plot_type)
    num_mode = len(Mode_list)
    figP,axP = plt.subplots(row,1,figsize=(9,9),sharey=True,sharex=True)
    for i in range(row):
        for j in range(num_mode):
            axP[i].scatter(Plot_Data[Mode_list[j]]["TIME"],Plot_Data[Mode_list[j]][Plot_type[i]],s=35,color = color_list[j%num_mode])
    

    #===Set Label===#
    axP[0].set_ylim(-Ylim,Ylim)
    axP[row - 1].set_xticklabels(XlabelSet[0])
    axP[row - 1].set_xticks(XlabelSet[1])
    labels = axP[0].get_yticklabels()
    for i in range(row):
        labels = labels + axP[i].get_yticklabels() + axP[i].get_xticklabels()
    [label.set_fontsize(xtick_size) for label in labels]
    [label.set_fontname('Arial') for label in labels]
    for i in range(row):
        if Plot_type[i] == "E":
            axP[i].set_ylabel("East errors (m)",font_label)
        if Plot_type[i] == "N":
            axP[i].set_ylabel("North errors (m)",font_label)
        if Plot_type[i] == "U":
            axP[i].set_ylabel("Up errors (m)",font_label)
    axP[row - 1].set_xlabel("GPS time (hour)",font_label)
    
    #===Set text (RMS)===#
    type_list = ["E","N","U","NSAT","PDOP","AMB","TIME"]
    for i in range(row):
        text_temp = {}
        RMS_value = []
        for j in range(num_mode):
            RMS_value.append(np.sqrt(np.mean(np.array(Plot_Data[Mode_list[j]][type_list[i]])**2))*100)
        MRS_str = "RMS="
        for j in range(len(RMS_value)):
            MRS_str = MRS_str + "{:.2f}cm, ".format(RMS_value[j])
        ax_range = axP[i].axis()
        axP[i].text(ax_range[0],ax_range[3]+Ylim/15,MRS_str[:-2],font_text)

    #===Set legend===#
    axP[0].legend(Mode_list,prop=font_legend,
            framealpha=0,facecolor='none',ncol=4,numpoints=5,markerscale=3, 
            borderaxespad=0,bbox_to_anchor=(1,1.2),loc=1) 
    if Show:
        plt.show()
    plt.close()  

def plot_E_N_U_NSAT(Plot_Data = {}, Plot_type = [], Mode_list = [], Ylim = 0.5, XlabelSet = [], Show = True):
    #===Plot===#
    row = len(Plot_type)
    num_mode = len(Mode_list)
    figP,axP = plt.subplots(row,1,figsize=(9,10),sharey=False,sharex=True)
    for i in range(row):
        for j in range(num_mode):
            if Plot_type[i] == "NSAT":
                axP[i].plot(Plot_Data[Mode_list[j]]["TIME"],Plot_Data[Mode_list[j]]["NSAT"],color = color_list[j%num_mode])
            else:
                axP[i].scatter(Plot_Data[Mode_list[j]]["TIME"],Plot_Data[Mode_list[j]][Plot_type[i]],s=35,color = color_list[j%num_mode])
                axP[i].set_ylim(-Ylim,Ylim)
    axP[row - 1].set_xlabel("GPS time (hour)",font_label)

    #===Set Label===#
    
    axP[row - 1].set_xticklabels(XlabelSet[0])
    axP[row - 1].set_xticks(XlabelSet[1])
    labels = axP[0].get_yticklabels()
    for i in range(row):
        labels = labels + axP[i].get_yticklabels() + axP[i].get_xticklabels()
    [label.set_fontsize(xtick_size) for label in labels]
    [label.set_fontname('Arial') for label in labels]
    for i in range(row):
        if Plot_type[i] == "E":
            axP[i].set_ylabel("East errors (m)",font_label)
        if Plot_type[i] == "N":
            axP[i].set_ylabel("North errors (m)",font_label)
        if Plot_type[i] == "U":
            axP[i].set_ylabel("Up errors (m)",font_label)
        if Plot_type[i] == "NSAT":
            axP[i].set_ylabel("Number of SAT",font_label)

    #===Set text (RMS)===#
    type_list = ["E","N","U","NSAT","PDOP","AMB","TIME"]
    for i in range(row):
        if type_list[i] == "NSAT":
            text_temp = {}
            RMS_value = []
            for j in range(num_mode):
                RMS_value.append(np.mean(Plot_Data[Mode_list[j]][type_list[i]]))
            MRS_str = "MEAN="
            for j in range(len(RMS_value)):
                MRS_str = MRS_str + "{:.2f}, ".format(RMS_value[j])
        else:
            text_temp = {}
            RMS_value = []
            for j in range(num_mode):
                RMS_value.append(np.sqrt(np.mean(np.array(Plot_Data[Mode_list[j]][type_list[i]])**2))*100)
            MRS_str = "RMS="
            for j in range(len(RMS_value)):
                MRS_str = MRS_str + "{:.2f}cm, ".format(RMS_value[j])
        ax_range = axP[i].axis()
        axP[i].text(ax_range[0],ax_range[3]+Ylim/15,MRS_str[:-2],font_text)

    #===Set legend===#
    axP[0].legend(Mode_list,prop=font_legend,
            framealpha=0,facecolor='none',ncol=4,numpoints=5,markerscale=3, 
            borderaxespad=0,bbox_to_anchor=(1,1.24),loc=1) 
    if Show:
        plt.show()
    plt.close()            

def Plot_timeseries_position(File_info = [], Start = [], End = [], Plot_type = [], Ylim = 0.2, Save_dir = "", Show = True, Fixed = False, All = False, Time_type = "", Delta_xlabel = 1, Mean = False, Sigma = 3, Signum = 0, Delta_data = 30, Reconvergence = 3600, Recon_list = []):
    file_num = len(File_info)
    [start_week,start_sow] = tr.ymd2gpst(Start[0],Start[1],Start[2],Start[3],Start[4],Start[5])
    [end_week,end_sow] = tr.ymd2gpst(End[0],End[1],End[2],End[3],End[4],End[5])
    duration_time = ((end_week-start_week)*604800+(end_sow - start_sow))/3600

    #=== Load data & XYZ2ENU ===#
    Data_All = {}
    for i in range(file_num):   
        data_raw_temp = loaddata(File_info[i][0],[start_week,start_sow],[end_week,end_sow])
        # Static
        if not os.path.exists(File_info[i][1]) and len(File_info[i][1]) <= 9:
            if File_info[i][1] not in TRUE_Position:
                continue
            data_ENU_temp = XYZ2ENU_static(XYZ = data_raw_temp,REF_XYZ=TRUE_Position[File_info[i][1]])
        # Dynamic
        else:
            data_ENU_temp = XYZ2ENU_dynamic(XYZ = data_raw_temp,REF_FILE=File_info[i][1])
        Data_All[File_info[i][2]] = data_ENU_temp
    
    #=== Data Convert ===#
    num_mode = len(File_info)
    [XLabel,XTick,cov_time,begT,LastT]=glv.xtick(Time_type,Start[0],Start[1],Start[2],Start[3]+Start[4]/60,duration_time,Delta_xlabel)
    # Initialization
    PLOT_ALL,PLOT_RAW = {},{}
    type_list = ["E","N","U","NSAT","PDOP","AMB","TIME"]
    for i in range(num_mode):
        if File_info[i][2] not in PLOT_ALL:
            PLOT_ALL[File_info[i][2]],PLOT_RAW[File_info[i][2]] = {},{}
            for cur_type in type_list:
                PLOT_ALL[File_info[i][2]][cur_type],PLOT_RAW[File_info[i][2]][cur_type] = [],[]
    # Convert
    for i in range(num_mode):
        for cur_time in Data_All[File_info[i][2]]:
            plot_time = (cur_time - cov_time) / 3600
            if ((plot_time >= Start[3] and plot_time <= (Start[3]+duration_time)) or All):
                if(Fixed and Data_All[File_info[i][2]][cur_time]["AMB"] == 0):
                    continue
                PLOT_ALL[File_info[i][2]]["TIME"].append(plot_time)
                PLOT_RAW[File_info[i][2]]["TIME"].append(plot_time)
                for cur_type in type_list:
                    if cur_type == "TIME":
                        continue
                    PLOT_ALL[File_info[i][2]][cur_type].append(Data_All[File_info[i][2]][cur_time][cur_type])
                    PLOT_RAW[File_info[i][2]][cur_type].append(Data_All[File_info[i][2]][cur_time][cur_type])
    Mode_list = [File_info[i][2] for i in range(num_mode)]
    
    #=== Sigma ===#
    if Signum != 0:
        edit_sigma(All_Data = PLOT_ALL, Sigma=Sigma, Signum = Signum)
    if Mean:
        edit_mean(PLOT_ALL, PLOT_RAW)

    #=== Statistics ===#
    statistics(PLOT_RAW,PLOT_ALL,Delta_data,Start,duration_time,Reconvergence,Recon_list,Show,Save_dir)

    #=== Plot ===#
    if Plot_type == ["E","N","U"]:
        plot_E_N_U(Plot_Data=PLOT_ALL, Plot_type=Plot_type, Mode_list=Mode_list, Ylim=Ylim, XlabelSet = [XLabel,XTick], Show=Show)
    if Plot_type == ["E","N","U","NSAT"]:
        plot_E_N_U_NSAT(Plot_Data=PLOT_ALL, Plot_type=Plot_type, Mode_list=Mode_list, Ylim=Ylim, XlabelSet = [XLabel,XTick], Show=Show)

def plot_percent_vertical(Plot_Data = {}, Plot_type = [], Mode_list = [], Ylim = 0.5, Percentage = 0.0, Duration_time = 3600, Reconvergence = 3600, Start = [], Delta_data = 30, XlabelSet = [], Show = True):
    #=== Data convert===#
    PLOT_ALL,PLOT_RAW = {},{}
    for cur_mode in Plot_Data.keys():
        PLOT_ALL[cur_mode],PLOT_RAW[cur_mode] = {},{}
        PLOT_ALL[cur_mode]["TIME"],PLOT_RAW[cur_mode]["TIME"] = [],[]
        for i in Plot_Data[cur_mode].keys():
            time_np = np.array(Plot_Data[cur_mode][i]["TIME"])
            e_np,n_np,u_np = np.array(Plot_Data[cur_mode][i]["E"]),np.array(Plot_Data[cur_mode][i]["N"]),np.array(Plot_Data[cur_mode][i]["U"])
            horizontal = np.sqrt(e_np**2+n_np**2)*100
            vertical = np.abs(u_np)*100
            position = np.sqrt(e_np**2+n_np**2+u_np**2)*100
            cur_time = Start[3] * 3600
            for j in range(int(Duration_time*3600 / Reconvergence)):
                cur_time = Start[3] * 3600 + j * Reconvergence
                con_position_num,con_horizontal_num,con_vertical_num = 0,0,0
                while cur_time < Start[3] * 3600 + (j+1) * Reconvergence:
                    cur_time_hour = cur_time
                    cur_time_index = cur_time_hour - (Start[3] * 3600 + j * Reconvergence)
                    find_time_index = time_np == cur_time / 3600
                    cur_vertical = vertical[find_time_index]
                    cur_horizontal = horizontal[find_time_index]
                    if cur_vertical.size != 1:
                        cur_time = cur_time + Delta_data
                        continue
                    if cur_time_index not in PLOT_ALL[cur_mode].keys():
                        PLOT_ALL[cur_mode][cur_time_index],PLOT_RAW[cur_mode][cur_time_index] = [],[]
                    PLOT_ALL[cur_mode][cur_time_index].append(cur_vertical[0])
                    PLOT_RAW[cur_mode][cur_time_index].append(cur_horizontal[0])
                    if cur_time_index not in PLOT_ALL[cur_mode]["TIME"]:
                        PLOT_ALL[cur_mode]["TIME"].append(cur_time_index)
                    cur_time = cur_time + Delta_data
    
    for cur_mode in PLOT_ALL.keys():
        PLOT_ALL[cur_mode]["Vertical"],PLOT_ALL[cur_mode]["Horizontal"] = [],[]
        for cur_time in PLOT_ALL[cur_mode].keys():
            if cur_time == "TIME" or cur_time == "Vertical" or cur_time == "Horizontal":
                continue
            if Percentage == 0:
                PLOT_ALL[cur_mode]["Vertical"].append(np.mean(PLOT_ALL[cur_mode][cur_time]))
                PLOT_ALL[cur_mode]["Horizontal"].append(np.mean(PLOT_RAW[cur_mode][cur_time]))
            else:
                temp = np.array(PLOT_ALL[cur_mode][cur_time])
                temp.sort()
                PLOT_ALL[cur_mode]["Vertical"].append(temp[int((temp.size) * Percentage)])
                temp = np.array(PLOT_RAW[cur_mode][cur_time])
                temp.sort()
                PLOT_ALL[cur_mode]["Horizontal"].append(temp[int((temp.size) * Percentage)])
    #=== Plot ===#
    figP,axP = plt.subplots(1,1,figsize=(6,6),sharey=False,sharex=True)
    j = 0
    for cur_mode in PLOT_ALL.keys():
        axP.plot(np.array(PLOT_ALL[cur_mode]["TIME"])/60,PLOT_ALL[cur_mode]["Vertical"],linewidth = 2,color = color_list[j])
        j = j + 1
    #===Set Label===#
    
    # axP.set_xticklabels(XlabelSet[0])
    # axP.set_xticks(XlabelSet[1])
    labels = axP.get_yticklabels() + axP.get_xticklabels()
    [label.set_fontsize(xtick_size) for label in labels]
    [label.set_fontname('Arial') for label in labels]
    axP.set_ylabel("Horizontal errors (cm)",font_label)
    axP.set_xlabel("GPS time (min)",font_label)
    axP.legend(Mode_list,prop=font_legend,
            framealpha=0,facecolor='none',ncol=4,numpoints=5,markerscale=3, 
            borderaxespad=0,bbox_to_anchor=(1,1.1),loc=1)
    leg = axP.get_legend()
    for legobj in leg.legendHandles:
        legobj.set_linewidth(5)
    plt.show()

def plot_percent_horizontal(Plot_Data = {}, Plot_type = [], Mode_list = [], Ylim = 0.5, Percentage = 0.0, Duration_time = 3600, Reconvergence = 3600, Start = [], Delta_data = 30, XlabelSet = [], Show = True):
    #=== Data convert===#
    PLOT_ALL,PLOT_RAW = {},{}
    for cur_mode in Plot_Data.keys():
        PLOT_ALL[cur_mode],PLOT_RAW[cur_mode] = {},{}
        PLOT_ALL[cur_mode]["TIME"],PLOT_RAW[cur_mode]["TIME"] = [],[]
        for i in Plot_Data[cur_mode].keys():
            time_np = np.array(Plot_Data[cur_mode][i]["TIME"])
            e_np,n_np,u_np = np.array(Plot_Data[cur_mode][i]["E"]),np.array(Plot_Data[cur_mode][i]["N"]),np.array(Plot_Data[cur_mode][i]["U"])
            horizontal = np.sqrt(e_np**2+n_np**2)*100
            vertical = np.abs(u_np)*100
            position = np.sqrt(e_np**2+n_np**2+u_np**2)*100
            cur_time = Start[3] * 3600
            for j in range(int(Duration_time*3600 / Reconvergence)):
                cur_time = Start[3] * 3600 + j * Reconvergence
                con_position_num,con_horizontal_num,con_vertical_num = 0,0,0
                while cur_time < Start[3] * 3600 + (j+1) * Reconvergence:
                    cur_time_hour = cur_time
                    cur_time_index = cur_time_hour - (Start[3] * 3600 + j * Reconvergence)
                    find_time_index = time_np == cur_time / 3600
                    cur_vertical = vertical[find_time_index]
                    cur_horizontal = horizontal[find_time_index]
                    if cur_vertical.size != 1:
                        cur_time = cur_time + Delta_data
                        continue
                    if cur_time_index not in PLOT_ALL[cur_mode].keys():
                        PLOT_ALL[cur_mode][cur_time_index],PLOT_RAW[cur_mode][cur_time_index] = [],[]
                    PLOT_ALL[cur_mode][cur_time_index].append(cur_vertical[0])
                    PLOT_RAW[cur_mode][cur_time_index].append(cur_horizontal[0])
                    if cur_time_index not in PLOT_ALL[cur_mode]["TIME"]:
                        PLOT_ALL[cur_mode]["TIME"].append(cur_time_index)
                    cur_time = cur_time + Delta_data
    
    for cur_mode in PLOT_ALL.keys():
        PLOT_ALL[cur_mode]["Vertical"],PLOT_ALL[cur_mode]["Horizontal"] = [],[]
        for cur_time in PLOT_ALL[cur_mode].keys():
            if cur_time == "TIME" or cur_time == "Vertical" or cur_time == "Horizontal":
                continue
            if Percentage == 0:
                PLOT_ALL[cur_mode]["Vertical"].append(np.mean(PLOT_ALL[cur_mode][cur_time]))
                PLOT_ALL[cur_mode]["Horizontal"].append(np.mean(PLOT_RAW[cur_mode][cur_time]))
            else:
                temp = np.array(PLOT_ALL[cur_mode][cur_time])
                temp.sort()
                PLOT_ALL[cur_mode]["Vertical"].append(temp[int((temp.size) * Percentage)])
                temp = np.array(PLOT_RAW[cur_mode][cur_time])
                temp.sort()
                PLOT_ALL[cur_mode]["Horizontal"].append(temp[int((temp.size) * Percentage)])
    #=== Plot ===#
    figP,axP = plt.subplots(1,1,figsize=(6,6),sharey=False,sharex=True)
    j = 0
    for cur_mode in PLOT_ALL.keys():
        axP.plot(np.array(PLOT_ALL[cur_mode]["TIME"])/60,PLOT_ALL[cur_mode]["Horizontal"],linewidth = 2,color = color_list[j])
        j = j + 1
    #===Set Label===#
    
    # axP.set_xticklabels(XlabelSet[0])
    # axP.set_xticks(XlabelSet[1])
    labels = axP.get_yticklabels() + axP.get_xticklabels()
    [label.set_fontsize(xtick_size) for label in labels]
    [label.set_fontname('Arial') for label in labels]
    axP.set_ylabel("Vertical errors (cm)",font_label)
    axP.set_xlabel("GPS time (min)",font_label)
    axP.legend(Mode_list,prop=font_legend,
            framealpha=0,facecolor='none',ncol=4,numpoints=5,markerscale=3, 
            borderaxespad=0,bbox_to_anchor=(1,1.1),loc=1)
    leg = axP.get_legend()
    for legobj in leg.legendHandles:
        legobj.set_linewidth(5)
    plt.show()

def plot_percent_HV(Plot_Data = {}, Plot_type = [], Mode_list = [], Ylim = 0.5, Percentage = 0.0, Duration_time = 3600, Reconvergence = 3600, Start = [], Delta_data = 30, XlabelSet = [], Show = True):
    #=== Data convert===#
    PLOT_ALL,PLOT_RAW = {},{}
    for cur_mode in Plot_Data.keys():
        PLOT_ALL[cur_mode],PLOT_RAW[cur_mode] = {},{}
        PLOT_ALL[cur_mode]["TIME"],PLOT_RAW[cur_mode]["TIME"] = [],[]
        for i in Plot_Data[cur_mode].keys():
            time_np = np.array(Plot_Data[cur_mode][i]["TIME"])
            e_np,n_np,u_np = np.array(Plot_Data[cur_mode][i]["E"]),np.array(Plot_Data[cur_mode][i]["N"]),np.array(Plot_Data[cur_mode][i]["U"])
            horizontal = np.sqrt(e_np**2+n_np**2)*100
            vertical = np.abs(u_np)*100
            position = np.sqrt(e_np**2+n_np**2+u_np**2)*100
            cur_time = Start[3] * 3600
            for j in range(int(Duration_time*3600 / Reconvergence)):
                cur_time = Start[3] * 3600 + j * Reconvergence
                con_position_num,con_horizontal_num,con_vertical_num = 0,0,0
                while cur_time < Start[3] * 3600 + (j+1) * Reconvergence:
                    cur_time_hour = cur_time
                    cur_time_index = cur_time_hour - (Start[3] * 3600 + j * Reconvergence)
                    find_time_index = time_np == cur_time / 3600
                    cur_vertical = vertical[find_time_index]
                    cur_horizontal = horizontal[find_time_index]
                    if cur_vertical.size != 1:
                        cur_time = cur_time + Delta_data
                        continue
                    if cur_time_index not in PLOT_ALL[cur_mode].keys():
                        PLOT_ALL[cur_mode][cur_time_index],PLOT_RAW[cur_mode][cur_time_index] = [],[]
                    PLOT_ALL[cur_mode][cur_time_index].append(cur_vertical[0])
                    PLOT_RAW[cur_mode][cur_time_index].append(cur_horizontal[0])
                    if cur_time_index not in PLOT_ALL[cur_mode]["TIME"]:
                        PLOT_ALL[cur_mode]["TIME"].append(cur_time_index)
                    cur_time = cur_time + Delta_data
    
    for cur_mode in PLOT_ALL.keys():
        PLOT_ALL[cur_mode]["Vertical"],PLOT_ALL[cur_mode]["Horizontal"] = [],[]
        for cur_time in PLOT_ALL[cur_mode].keys():
            if cur_time == "TIME" or cur_time == "Vertical" or cur_time == "Horizontal":
                continue
            if Percentage == 0:
                PLOT_ALL[cur_mode]["Vertical"].append(np.mean(PLOT_ALL[cur_mode][cur_time]))
                PLOT_ALL[cur_mode]["Horizontal"].append(np.mean(PLOT_RAW[cur_mode][cur_time]))
            else:
                temp = np.array(PLOT_ALL[cur_mode][cur_time])
                temp.sort()
                PLOT_ALL[cur_mode]["Vertical"].append(temp[int((temp.size) * Percentage)])
                temp = np.array(PLOT_RAW[cur_mode][cur_time])
                temp.sort()
                PLOT_ALL[cur_mode]["Horizontal"].append(temp[int((temp.size) * Percentage)])
    #=== Plot ===#
    figP,axP = plt.subplots(1,2,figsize=(12,6),sharey=False,sharex=True)
    j = 0
    for cur_mode in PLOT_ALL.keys():
        axP[0].plot(np.array(PLOT_ALL[cur_mode]["TIME"])/60,PLOT_ALL[cur_mode]["Horizontal"],linewidth = 2)
        axP[1].plot(np.array(PLOT_ALL[cur_mode]["TIME"])/60,PLOT_ALL[cur_mode]["Vertical"],linewidth = 2)
        j = j + 1
    #===Set Label===#
    
    # axP.set_xticklabels(XlabelSet[0])
    # axP.set_xticks(XlabelSet[1])
    labels = axP[0].get_yticklabels() + axP[0].get_xticklabels() + axP[1].get_yticklabels() + axP[1].get_xticklabels()
    [label.set_fontsize(xtick_size) for label in labels]
    [label.set_fontname('Arial') for label in labels]
    axP[1].set_ylabel("Vertical errors (cm)",font_label)
    axP[0].set_ylabel("Horizontal errors (cm)",font_label)
    axP[1].set_xlabel("GPS time (min)",font_label)
    axP[0].set_xlabel("GPS time (min)",font_label)
    axP[1].legend(Mode_list,prop=font_legend,
            framealpha=0,facecolor='none',ncol=4,numpoints=5,markerscale=3, 
            borderaxespad=0,bbox_to_anchor=(1,1.1),loc=1)
    leg = axP[1].get_legend()
    for legobj in leg.legendHandles:
        legobj.set_linewidth(5)
    plt.show()

def Plot_percent_position(File_info = [], Start = [], End = [], Plot_type = [], Ylim = 0.2, Percentage = 0.0, Save_dir = "", Show = True, Fixed = False, All = False, Time_type = "", Delta_xlabel = 1, Mean = False, Sigma = 3, Signum = 0, Delta_data = 30, Reconvergence = 3600, Recon_list = []):
    mode_num = len(File_info)
    [start_week,start_sow] = tr.ymd2gpst(Start[0],Start[1],Start[2],Start[3],Start[4],Start[5])
    [end_week,end_sow] = tr.ymd2gpst(End[0],End[1],End[2],End[3],End[4],End[5])
    duration_time = ((end_week-start_week)*604800+(end_sow - start_sow))/3600

    #=== Load data & XYZ2ENU ===#
    Data_All = {}
    for i in range(mode_num):   
        data_raw_temp = loaddata(File_info[i][0],[start_week,start_sow],[end_week,end_sow])
        data_mode_temp = {}
        for j in range(len(File_info[i]) - 2):
            if File_info[i][-2] not in TRUE_Position:
                continue
            data_raw_temp = loaddata(File_info[i][j],[start_week,start_sow],[end_week,end_sow])
            data_mode_temp[j] = XYZ2ENU_static(XYZ = data_raw_temp,REF_XYZ=TRUE_Position[File_info[i][-2]])
        Data_All[File_info[i][-1]] = data_mode_temp

    # Initialization
    PLOT_ALL,PLOT_RAW = {},{}
    type_list = ["E","N","U","AMB","TIME"]
    [XLabel,XTick,cov_time,begT,LastT]=glv.xtick(Time_type,Start[0],Start[1],Start[2],Start[3]+Start[4]/60,duration_time,Delta_xlabel)
    for i in range(mode_num):
        if File_info[i][-1] not in PLOT_ALL:
            PLOT_ALL[File_info[i][-1]],PLOT_RAW[File_info[i][-1]] = {},{}
            for j in range(len(File_info[i]) - 2):
                PLOT_ALL[File_info[i][-1]][j],PLOT_RAW[File_info[i][-1]][j] = {},{}
                for cur_type in type_list:
                    PLOT_ALL[File_info[i][-1]][j][cur_type],PLOT_RAW[File_info[i][-1]][j][cur_type] = [],[]
    # Convert
    for i in range(mode_num):
        for j in range(len(File_info[i]) - 2):
            for cur_time in Data_All[File_info[i][-1]][j]:
                plot_time = ((cur_time - cov_time) / 3600) % 24
                if ((plot_time >= Start[3] and plot_time <= (Start[3]+duration_time)) or All):
                    if(Fixed and Data_All[File_info[i][-1]][j][cur_time]["AMB"] == 0):
                        continue
                    PLOT_ALL[File_info[i][-1]][j]["TIME"].append(plot_time)
                    PLOT_RAW[File_info[i][-1]][j]["TIME"].append(plot_time)
                    for cur_type in type_list:
                        if cur_type == "TIME":
                            continue
                        PLOT_ALL[File_info[i][-1]][j][cur_type].append(Data_All[File_info[i][-1]][j][cur_time][cur_type])
                        PLOT_RAW[File_info[i][-1]][j][cur_type].append(Data_All[File_info[i][-1]][j][cur_time][cur_type])
    Mode_list = [File_info[i][-1] for i in range(mode_num)]

    #=== Plot ===#
    if Plot_type == "Horizontal":
        plot_percent_horizontal(Plot_Data=PLOT_ALL, Plot_type=Plot_type, Mode_list=Mode_list, Ylim=Ylim, Percentage = Percentage, Duration_time = duration_time, Reconvergence = Reconvergence, Delta_data = Delta_data, Start = Start, XlabelSet = [XLabel,XTick], Show=Show)
    if Plot_type == "Vertical":
        plot_percent_vertical(Plot_Data=PLOT_ALL, Plot_type=Plot_type, Mode_list=Mode_list, Ylim=Ylim, Percentage = Percentage, Duration_time = duration_time, Reconvergence = Reconvergence, Delta_data = Delta_data, Start = Start, XlabelSet = [XLabel,XTick], Show=Show)
    if Plot_type == "HV":
        plot_percent_HV(Plot_Data=PLOT_ALL, Plot_type=Plot_type, Mode_list=Mode_list, Ylim=Ylim, Percentage = Percentage, Duration_time = duration_time, Reconvergence = Reconvergence, Delta_data = Delta_data, Start = Start, XlabelSet = [XLabel,XTick], Show=Show)
                    
