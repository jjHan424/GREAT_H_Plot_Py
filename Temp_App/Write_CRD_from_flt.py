from calendar import c
import os
import shutil
import sys
import subprocess
path = "/Users/hanjunjie/Gap1/ZWD_Retrieval_PPPRTK/Server/"
out_crd_path = r"/Users/hanjunjie/Gap1/ZWD_Retrieval_PPPRTK/CRDSITE/CMNC_ALL_FLT.pyxml"
obs_list = os.listdir(path)
for cur_file in obs_list:
    cur_path = os.path.join(path,cur_file)
    with open(cur_path,'rt') as f:
        lines = f.readlines()
        if len(lines) < 2000:
            continue
        last_line = lines[-10]
        values = last_line.split()
        str_write = "{:<8}{:>15.4f}{:>15.4f}{:>15.4f}".format(cur_file[0:4],float(values[1]),float(values[2]),float(values[3]))
        str_write = str_write + "    {} ".format("G")
        str_write = str_write + "      "
        str_write = str_write + "      "
        str_write = str_write + "      "
        str_write = "\"{}00CHN\",\"\",\"\",\"\",\"\",\"\",\"\",\"\",\"\",\"\",\"\",\"\",\"{:.4f}\",\"{:.4f}\",\"{:.4f}\",\"\",\"\",\"\",\"\",\"\",\"\"".format(cur_file[0:4],float(values[1]),float(values[2]),float(values[3]))
        with open(out_crd_path,'a') as file:
            file.write(str_write+"\n")
            # file.write("  True\n")
