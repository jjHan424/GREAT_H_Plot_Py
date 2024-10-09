# from asyncore import write
from multiprocessing.dummy import DummyProcess
import os
from socket import SHUT_WR
import sys
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

def xtick_min(time,year,mon,day,starttime,LastT,deltaT):
    if "+" in time:
        end_time = len(time)
        delta_Time = int(time[4:end_time]) + starttime
        begT = int(time[4:end_time]) + starttime
    else:
        delta_Time = starttime
        begT=starttime
    #for time in data[mode[0]].keys():
    secow_start = tr.ymd2gpst(year,mon,day,0,00,00)
    doy = tr.ymd2doy(year,mon,day,0,00,00)
    cov_Time = secow_start[1] - 0 * 3600
    if "+" in time:
        value = time.split("+")
        cov_Time = secow_start[1] - int(value[1]) * 3600
    end_Time = begT + LastT
    delta_X = math.ceil((LastT)/deltaT)
    XLabel = []
    XTick = []
    starttime = begT - deltaT

    # for i in range(delta_X):
    #     starttime = starttime + deltaT
    #     cur_Str_X = '%02d' % (starttime % 24) + ":{:0>2}".format(int((starttime-int(starttime))*60))
    #     XLabel.append(cur_Str_X)
    #     XTick.append((starttime))       
    
    while starttime < end_Time:
        starttime = starttime + deltaT
        if (starttime >= end_Time):
            cur_Str_X = '%02d' % (end_Time % 24) + ":{:0>2}".format(round((end_Time-int(end_Time))*60))
            # cur_Str_X = '%d' % (end_Time % 24)
            XLabel.append(cur_Str_X)
            XTick.append((end_Time))
            break
        cur_Str_X = '%02d' % (starttime % 24) + ":{:0>2}".format(round((starttime-int(starttime))*60))
        # cur_Str_X = '%d' % (starttime % 24)
        XLabel.append(cur_Str_X)
        XTick.append((starttime))
    
    return (XLabel,XTick,cov_Time,begT,LastT)

def loaddata(File_name = "", Start = [], End = []):
    #Judge the Head
    file = open(File_name,"r")
    first_line = next(file)
    file.close()
    first_value = first_line.split()
    if first_line == "#EOP":
        i=1
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

def plot_E_N_U(Plot_Data = {}, Plot_type = [], Mode_list = [], Ylim = 0.5, XlabelSet = [], Show = True):
    #===Plot===#
    row = len(Plot_type)
    num_mode = len(Mode_list)
    figP,axP = plt.subplots(row,1,figsize=(9,9),sharey=True,sharex=True)
    for i in range(row):
        for j in range(num_mode):
            if Plot_type[i] == "NSAT":
                axP[i].plot(Plot_Data[Mode_list[j]]["TIME"],Plot_Data[Mode_list[j]]["NSAT"])
            else:
                axP[i].scatter(Plot_Data[Mode_list[j]]["TIME"],Plot_Data[Mode_list[j]][Plot_type[i]],s=35,color = color_list[j%num_mode])
    axP[row - 1].set_xlabel("GPS time (hour)",font_label)

    #===Set Label===#
    axP[0].set_ylim(-Ylim,Ylim)
    axP[row - 1].set_xticklabels(XlabelSet[0])
    axP[row - 1].set_xticks(XlabelSet[1])
    labels = axP[0].get_yticklabels()
    for i in range(row):
        labels = labels + axP[i].get_yticklabels() + axP[i].get_xticklabels()
    [label.set_fontsize(xtick_size) for label in labels]
    [label.set_fontname('Times New Roman') for label in labels]
    for i in range(row):
        if Plot_type[i] == "E":
            axP[i].set_ylabel("East errors (m)",font_label)
        if Plot_type[i] == "N":
            axP[i].set_ylabel("North errors (m)",font_label)
        if Plot_type[i] == "U":
            axP[i].set_ylabel("Up errors (m)",font_label)

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


    

def plot_timeseries_position(File_info = [], Start = [], End = [], Plot_type = [], Ylim = 0.2, Save_dir = "", Show = True, Fixed = False, All = False, Time_type = "", Delta_xlabel = 1, Mean = False, Sigma = 3, Signum = 0, Delta_data = 30, Reconvergence = 3600, Recon_list = []):
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
    [XLabel,XTick,cov_time,begT,LastT]=xtick_min(Time_type,Start[0],Start[1],Start[2],Start[3]+Start[4]/60,duration_time,Delta_xlabel)
    # Initialization
    PLOT_ALL = {}
    type_list = ["E","N","U","NSAT","PDOP","AMB","TIME"]
    for i in range(num_mode):
        if File_info[i][2] not in PLOT_ALL:
            PLOT_ALL[File_info[i][2]] = {}
            for cur_type in type_list:
                PLOT_ALL[File_info[i][2]][cur_type] = []
    # Convert
    for i in range(num_mode):
        for cur_time in Data_All[File_info[i][2]]:
            plot_time = (cur_time - cov_time) / 3600
            if ((plot_time >= Start[3] and plot_time <= (Start[3]+duration_time)) or All):
                if(Fixed and Data_All[File_info[i][2]][cur_time]["AMB"] == 0):
                    continue
                PLOT_ALL[File_info[i][2]]["TIME"].append(plot_time)
                for cur_type in type_list:
                    if cur_type == "TIME":
                        continue
                    PLOT_ALL[File_info[i][2]][cur_type].append(Data_All[File_info[i][2]][cur_time][cur_type])
    Mode_list = [File_info[i][2] for i in range(num_mode)]
    
    #=== Sigma ===#
    PLOT_EDIT = PLOT_ALL
    if Signum != 0:
        PLOT_EDIT = edit_sigma(All_Data = PLOT_ALL, Sigma=Sigma, Signum = Signum)
    #=== Plot ===#
    if Plot_type == ["E","N","U"]:
        plot_E_N_U(Plot_Data=PLOT_EDIT, Plot_type=Plot_type, Mode_list=Mode_list, Ylim=Ylim, XlabelSet = [XLabel,XTick], Show=Show)
    #=== Static ===#
    

