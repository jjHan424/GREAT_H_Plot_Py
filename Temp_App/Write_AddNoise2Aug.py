from math import floor
import os
import sys
sys.path.insert(0,os.path.dirname(__file__)+'/../LibBase')
sys.path.insert(0,os.path.dirname(__file__)+'/../LibPlot')
import numpy as np

site_list = ["BRUX","FFMJ","WARE"]
file_dir = "/Users/hanjunjie/Gap1/IONO_Accuracy_Predict/Data/2021/AUG"
file_dir_write = "/Users/hanjunjie/Gap1/IONO_Accuracy_Predict/Data/2021/AUG_ZWD_NOISE"
step = 0.005 # m
total_num = 200
for cur_site in site_list:
    raw_file = os.path.join(file_dir,"{}-GEC3-FIXED-30.aug".format(cur_site))
    with open(raw_file,'rt') as f:
        for line in f:
            for cur_accuracy in range(1,total_num + 1):
                write_file = os.path.join(file_dir_write,"{}-GEC3-FIXED-30-{:0>2}.aug".format(cur_site,cur_accuracy))
                with open(write_file,'a') as file:
                    file.write(line)
                file.close()
            if "HEADER" in line:
                break
        for line in f:
            if line[0] == ">":
                for cur_accuracy in range(1,total_num + 1):
                    write_file = os.path.join(file_dir_write,"{}-GEC3-FIXED-30-{:0>2}.aug".format(cur_site,cur_accuracy))
                    with open(write_file,'a') as file:
                        file.write(line)
                    file.close()
            else:
                value = line.split()
                for cur_accuracy in range(1,total_num + 1):
                    index_noise = 0
                    index_iono = -1
                    write_file = os.path.join(file_dir_write,"{}-GEC3-FIXED-30-{:0>2}.aug".format(cur_site,cur_accuracy))
                    white_noise = np.random.normal(0,step*cur_accuracy,40)
                    write_str = value[0]
                    for cur_value in value:
                        index_iono = index_iono + 1
                        if cur_value[0] == "C" or cur_value[0] == "E" or cur_value[0] == "G":
                            continue
                        else:
                            if index_iono == 5:
                                write_str = write_str + "{:>12.4f}".format(float(cur_value) + white_noise[index_noise])
                                # index_noise = index_noise + 1
                            else:
                                write_str = write_str + "{:>12.4f}".format(float(cur_value))
                    file = open(write_file,'a')
                    file.write(write_str + "\n")
                    file.close()
                            



