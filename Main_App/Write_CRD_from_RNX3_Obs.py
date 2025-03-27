from email.mime import base
import os
import sys
sys.path.insert(0,os.path.dirname(__file__)+'/../LibBase')
sys.path.insert(0,os.path.dirname(__file__)+'/../LibPlot')
import numpy as np
import matplotlib as mpl
mpl.use("TkAgg")
import matplotlib.pyplot as plt
import Lib_Plot_Basemap as basemap
obs_path = r"/Users/hanjunjie/Gap1/Data/2024/OBS_IGS/114"
out_crd_path = r"/Users/hanjunjie/Gap1/Site_CRD_New/IGS_ALL_SYS.crd"
is_crd_out = True
out_csv_path = r"/Users/hanjunjie/Gap1/ZWD_Retrieval_PPPRTK/Site_CRD_New/Centipete_France_40.csv"
is_xml_out = False
obs_list = os.listdir(obs_path)
is_check_obs = False
all_data,select_site = {},[]
crd_caster = basemap.load_data_caster("/Users/hanjunjie/Gap1/ZWD_Retrieval_PPPRTK/CRDSITE/centipede.crd")
# with open(select_site_file,'rt') as f:
#     for line in f:
#         select_site.append(line[0:4])

#readfile
for cur_obs in obs_list:
    cur_path = os.path.join(obs_path, cur_obs)
    cur_marker = ""
    cur_obs_num = 0
    cur_marker = cur_obs[0:4]
    all_data[cur_marker] = {}
    with open(cur_path,'rt') as f:
        for line in f:
            if "END OF HEADER" in line:
                break
            if "RINEX VERSION / TYPE" in line:
                value = line.split()
                version = float(value[0])
                if version < 3:
                    break
            if "MARKER NAME" in line and cur_marker == "" and line[0] != " ":
                value = line.split(" ")
                cur_marker = value[0][0:4].upper()
                all_data[cur_marker] = {}
                select_site.append(value[0][0:4])
            if "APPROX POSITION XYZ" in line and cur_marker != "" and "COMMENT" not in line:
                value = line.split()
                all_data[cur_marker]["X"] = float(value[0])
                all_data[cur_marker]["Y"] = float(value[1])
                all_data[cur_marker]["Z"] = float(value[2])
            if "SYS / # / OBS TYPES" in line and cur_obs_num == 0:
                sys_type = []
                value = line.split()
                sys_type.append(value[0])
                cur_obs_num = int(value[1])
                for cur_type in value:
                    if "SYS" != cur_type and "/" != cur_type and "#" != cur_type and "OBS" != cur_type and "TYPES" != cur_type and len(cur_type) >=2:
                        if cur_type[0:2] not in sys_type:
                            sys_type.append(cur_type[0:2])
                while cur_obs_num - 13 > 0:
                    cur_obs_num = cur_obs_num - 13
                    line = next(f)
                    value = line.split()
                    for cur_type in value:
                        if "SYS" != cur_type and "/" != cur_type and "#" != cur_type and "OBS" != cur_type and "TYPES" != cur_type and len(cur_type) >=2:
                            if cur_type[0:2] not in sys_type:
                                sys_type.append(cur_type[0:2])
                cur_obs_num = 0
                all_data[cur_marker][sys_type[0]] = sys_type[1:len(sys_type)]
#write crd file
if is_crd_out:
    for cur_site in all_data.keys():
        G,E,C2,C3 = False,False,False,False
        with open(out_crd_path,'a') as file:
            str_write = ""
            str_write = str_write + "{:<8}{:>15.4f}{:>15.4f}{:>15.4f}".format(cur_site,all_data[cur_site]["X"],all_data[cur_site]["Y"],all_data[cur_site]["Z"])
            # file.write("{:<8}{:>15.4f}{:>15.4f}{:>15.4f}".format(cur_site,all_data[cur_site]["X"],all_data[cur_site]["Y"],all_data[cur_site]["Z"]))
            sys_str = "G:"
            if "G" in all_data[cur_site].keys():
                for cur_band in all_data[cur_site]["G"]:
                    if "L" in cur_band:
                        sys_str = sys_str + cur_band + ","
                str_write = str_write + "{:>20}".format(sys_str[0:-1])
            else:
                str_write = str_write + "{:>20}".format("")
            sys_str = "E:"
            if "E" in all_data[cur_site].keys():
                for cur_band in all_data[cur_site]["E"]:
                    if "L" in cur_band:
                        sys_str = sys_str + cur_band + ","
                str_write = str_write + "{:>25}".format(sys_str[0:-1])
            else:
                str_write = str_write + "{:>25}".format("")
            sys_str = "C:"
            if "C" in all_data[cur_site].keys():
                for cur_band in all_data[cur_site]["C"]:
                    if "L" in cur_band:
                        sys_str = sys_str + cur_band + ","
                str_write = str_write + "{:>25}".format(sys_str[0:-1])
            else:
                str_write = str_write + "{:>25}".format("")
            file.write(str_write)
            if cur_site in select_site:
                file.write("  True\n")
            else:
                file.write("  False\n")


