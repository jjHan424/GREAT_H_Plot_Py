import os
import shutil
import sys
import subprocess

direct_path = "/Users/hanjunjie/Gap1/Data/2023/OBS_CMNC/341"
file_list = os.listdir(direct_path)
crx2rnx = "/Users/hanjunjie/tools/CRX2RNX"
gfzrnx = "/Users/hanjunjie/tools/gfzrnx"
str_list = ""
for cur_file in file_list:
    # print(cur_file[0:4])
    os.chdir(direct_path)
    str_list = str_list + cur_file[0:4] + "_"
    # if cur_file[-1:] == "Z":
    #     gzip_cmd = "gzip -d {}".format(cur_file)
    #     subprocess.getstatusoutput(gzip_cmd)
    #     crx2rnx_cmd = "{} {}".format(crx2rnx,cur_file[:-2])
    #     subprocess.getstatusoutput(crx2rnx_cmd)
    #     rnx2rnx3_cmd = "{} -finp {}o -fout {}o_rx3".format(gfzrnx,cur_file[:-3],cur_file[:-3])
    #     subprocess.getstatusoutput(rnx2rnx3_cmd)
    #     mv_cmd = "mv {}o_rx3 {}o".format(cur_file[:-3],cur_file[:-3])
    #     subprocess.getstatusoutput(mv_cmd)
    #     rm_cmd = "rm {}d".format(cur_file[:-3])
    #     subprocess.getstatusoutput(rm_cmd)
    #     mv_cmd = "mv {}o {}o".format(cur_file[:-3],cur_file[:-3].upper())
    #     subprocess.getstatusoutput(mv_cmd)
print(str_list)