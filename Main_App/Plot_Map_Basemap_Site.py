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
import Lib_Plot_Basemap as PlotBasemap

crd_file = ["/Users/hanjunjie/Gap1/ZWD_Retrieval_PPPRTK/EPN_SITE/EPN_GEC.crd","/Users/hanjunjie/Gap1/ZWD_Retrieval_PPPRTK/CRDSITE/centipede.crd"]
# crd_file = "/Users/hanjunjie/Gap1/ZWD_Retrieval_PPPRTK/CRDSITE/CMNC_ALL.crd"
# crd_file = "/Users/hanjunjie/Gap1/ZWD_Retrieval_PPPRTK/CRDSITE/EPN_SPAIN.crd"
# crd_file = "/Users/hanjunjie/Gap1/ZWD_Retrieval_PPPRTK/CRDSITE/CHN_HK_16.crd"
# shp_file = ["./SysFile/Shp_File/gadm36_HKG_shp/gadm36_HKG_0","./SysFile/Shp_File/gadm36_CHN_shp/gadm36_CHN_0"]
# shp_file = ["./SysFile/Shp_File/gadm36_CHN_shp/gadm36_CHN_2"]
shp_file = ["/Users/hanjunjie/tools/GREAT_H_Plot_Py/SysFile/Shp_File/world-administrative-boundaries/world-administrative-boundaries"]
# site_group = {"1":["BADH","BRUX","BUDD","BUDP","DENT","DIEP","DILL","DOUR","EIJS","EUSK","FFMJ","GOET","HAS6","HOBU","IJMU","JON6","KARL","KLOP","KOS1","ONS1","ONSA","PTBB","REDU","SPT0","SPT7","SULD","TERS","TIT2","VAE6","WARE","WSRT"]} #{"Group":[site1,site2]}
# site_group = {"1":['MLVL', 'AXPV', 'BSCN', 'TLMF', 'AJAC', 'ZZON', 'INVR', 'GUIP', 'VLIS', 'BRMF']}
# site_group = {"1":['MAS1', 'NABG', 'LPAL', 'NICO', 'ALME', 'ANK2', 'ELBA', 'BRMF', 'BBYS', 'LODZ', 'RANT', 'JON6', 'LEK6', 'UME6', 'ARJ6', 'KEV2', 'SCOR', 'WUTH', 'NYA1']}
# site_group = {"1":["MAS1","LPAL", "NICO", "ALME", "ANK2", "ELBA", "BRMF", "BBYS", "LODZ", "RANT", "JON6", "LEK6", "UME6", "ARJ6", "KEV2", "WUTH", "NYA1", "NABG"],
#               "Client":["IZAN", "ALME", "SONS", "ESCO", "COMO", "MLVL", "VLN1", "SAS2", "SPT0", "OST6", "OVE6", "TRO1", "VARS", "NYAL"]}
site_group = {
    # 1:["TERS","IJMU",'DIEP','WARE','EIJS','EUSK','DOUR','DILL','KARL','BADH','WSRT','KLOP'],"Client":['KOS1','BRUX','TIT2','REDU','FFMJ']
    # 1:['VAE6','JON6','BUDP','HAS6','SULD'],"Client":['ONS1','SPT0','SPT7','ONSA']
    1:['MALL','TERU','PASA','CACE','VALE','SONS','COBA','ALAC','ZARA','VIGO','CREU','ALBA','CARG','ALME','LLIV','HUEL','LEON','CEU1','SALA','ESCO','CASE','VALA','BELL','ACOR'],"Client":['CEBR','EBRE','MELI','SFER','VILL','YEBE']
    }
site_group = {
              "EPN1":['MLVL', 'IGNF', 'AXPV', 'BSCN', 'TLMF', 'TLSG', 'BRMF', 'ENTZ', 'PUYV', 'BRMG', 'VFCH', 'GRAS'],
              # "EPN":['ACOR','AJAC','ALME','ARIS','AUBG','AUTN','BACA','BRTS','BUTE','COMO','DEVA','DYNG','EGLT','ENTZ','GELL','GOET','GOML','HAS6','HELG','HETT','IJMU','INVR','IRBE','IZMI','LAMA','LDB2','LEIJ','LEK6','LODZ','LOV6','MAH1','MALL','MARS','METG','MIKL','MMET','MNSK','NICO','NOR7','OLK2','ORID','OST6','OVE6','POLV','PYHA','RANT','REDZ','ROM2','SAVU','SCOA','SMLA','SNEO','SPT7','SUN6','SWAS','TER2','TLL1','TRO1','VAIN','VARS','VILL','WARE','WTZZ','ZADA','ZYWI'],
            #   "Centipede":['ENSG', 'STME', 'SIGEO', 'ENSMM', 'ENFP', 'UEAU', 'RICE', 'BEFF', 'OFFNE', 'STJ9', 'UCBL', 'TOUR', 'PROS', 'BORD', 'LAWI', 'BIO', 'WL36', 'LAUR', 'STLYS', 'MANTA', 'KIKI'], # Same EPN
              # "Centipede":['ADNC', 'AE1', 'AGDE', 'AGF1', 'AGFM', 'AGTIC', 'AIGL', 'AL89', 'ALPE', 'ALTD', 'AP36', 'ASAGI', 'ASD21', 'ASHW', 'ASSAS', 'ATCC', 'AUB1', 'AUBU', 'AURI', 'AVR2', 'BALI', 'BANN', 'BARB', 'BATIV', 'BAU5', 'BAYS1', 'BDN', 'BEAU45', 'BEDEDE', 'BEFF', 'BELOS', 'BENG', 'BIO', 'BLIX', 'BNFL', 'BO12', 'BORD', 'BOU70', 'BRET', 'BTCHZ', 'BTD1', 'BURA', 'CABA', 'CARA', 'CAVX', 'CDA1', 'CDA2', 'CERM', 'CETTE', 'CH27', 'CHA2', 'CHAMB', 'CHARO', 'CHAT', 'CHAUMES', 'CHBE', 'CHSL', 'CHTL', 'CIAS', 'CLAP', 'CLAUD', 'CLFA', 'CLMRY', 'COIC', 'COMBE', 'COND', 'CPN26', 'CRK', 'CRO2', 'CRTK', 'CRUS', 'CVRA', 'DECO', 'DELMO', 'DELTA', 'DIA1', 'DMZ', 'DUVAL', 'EIDS', 'EJPB', 'ELA5', 'ENFP', 'ENSG', 'ENSG2', 'ENSIL', 'ENSMM', 'EOAA', 'EPI21', 'ERCK', 'ETOIL', 'FASPE', 'FAVE', 'FCMR', 'FD41', 'FDN1', 'FIGUE', 'FLO18', 'FM70', 'FOON', 'FORCA', 'FORG', 'FOUR1', 'FR45', 'FRNK', 'FRTK18', 'FRTK52', 'FSS02', 'GAECJ', 'GARRI', 'GERM', 'GM21', 'GPTR', 'GRAV', 'GRBS', 'GREZ77', 'GRIG', 'GROF', 'GRPE', 'GUIGO', 'GUIL', 'GVIL', 'GY45', 'HAF3', 'HAFL', 'HAME', 'HBC77', 'HNVA', 'HOFF', 'HONO', 'HOUSY', 'HSG68', 'IUTC', 'JBR', 'JD45', 'JGUI', 'JUAN', 'KAL1', 'KIKI', 'KIRR', 'LAJ39', 'LAUR', 'LAVKO', 'LAWI', 'LDOC', 'LEBE', 'LELEU', 'LEND', 'LH41', 'LHER', 'LHUI', 'LLENX', 'LLS1', 'LMSN', 'LNE1', 'LOLO', 'LORI', 'LULE', 'LUNE', 'LXLY', 'M2O', 'MACO', 'MAGC', 'MAMR', 'MANTA', 'MARS', 'MDA21', 'MELCAS', 'MICH', 'MIL70', 'MITTE', 'MNE1', 'MONTS', 'MORA', 'MPZT', 'MTLDR', 'MTP2', 'MTVAL', 'NATI', 'NATT', 'NGD1', 'NICE', 'NINA', 'NINO', 'NOUE', 'OFFNE', 'OGAG', 'OLIMI', 'OMB', 'OUIL', 'PA71', 'PALLU', 'PARC', 'PARD', 'PARIG', 'PARYG', 'PAU1', 'PDA1', 'PEPE', 'PGUI45', 'PHAC', 'PLQ1', 'PM52', 'PNPAI', 'PNRLF', 'POL25', 'POSD', 'POUZ', 'PRDR', 'PROS', 'RAMA', 'RAYN', 'RB81', 'RDHB7', 'REM57', 'REMKA', 'REVE', 'RICE', 'RIOM', 'RITZ', 'RIVAU', 'RSTL', 'RTK23', 'SABI', 'SAM1', 'SAUDU', 'SAUV', 'SC89', 'SCV1', 'SEDB', 'SEL12', 'SGC', 'SGHF', 'SHLT87', 'SIGEO', 'SKYF', 'SLM27', 'SLVT', 'SMVD', 'SOPH', 'SOUQ', 'SOY25', 'SPB28', 'SROG', 'SSB', 'STCRE', 'STJ9', 'STJEA', 'STLYS', 'STME', 'STMR', 'STOO', 'SVB7', 'SYSD', 'T001', 'T002', 'TBVU', 'TD04', 'TDPT', 'TG89', 'TH23', 'THAIS', 'TOOK', 'TOUR', 'TRALY', 'TUCH', 'TUTU', 'UCBL', 'UEAU', 'URC90', 'VAGC', 'VAU', 'VDM51', 'VIN26', 'VLG89', 'VLS1', 'WAHB', 'WINTZ', 'WITT', 'WIWI', 'WL36', 'WLBH', 'WP45', 'YOYO', 'YUUKI'], # All
              "Centipede":['CDA1', 'AP36', 'RIVAU', 'MTVAL', 'GPTR', 'GRBS', 'MAGC', 'CABA', 'HAME', 'IUTC', 'PDA1', 'DMZ', 'DUVAL', 'TOUR', 'CRO2', 'FORCA', 'WLBH', 'HAFL', 'SCV1', 'NICE'], # Central Grid
              # "Centipede":['CH27', 'FD41', 'WIWI', 'FOUR1', 'MPZT', 'OUIL', 'AUB1', 'FRNK', 'AURI', 'TUTU', 'PLQ1', 'TG89', 'MTLDR', 'PROS', 'CETTE', 'STCRE', 'EPI21', 'SEDB', 'GRPE', 'LLENX', 'BENG', 'URC90', 'CHSL', 'GUIL', 'SOPH', 'JBR', 'BIO', 'SGHF', 'NICE'] # Grid Node
              } 
# site_group = {1:['XJTC', 'XJWQ', 'XJWU', 'XJBL', 'TASH', 'XZGE', 'XZBG', 'XJZS', 'XJHT', 'XZRT', 'XZZB', 'XZZF', 'XJBE', 'XJDS', 'XJQM', 'XZGZ', 'XZYD', 'XJAL', 'XJFY', 'XJML', 'QHMY', 'XZSH', 'XZRK', 'YNRL', 'XJQH', 'XJJJ', 'QHLH', 'QHTT', 'XZCY', 'LALP', 'NMEJ', 'QHQI', 'QHMQ', 'SCXC', 'YNGM', 'NMWT', 'NMAZ', 'GSWD', 'SCJU', 'YNWS', 'NMEL', 'SNYA', 'XIAA', 'HNMY', 'GXWZ', 'QION', 'HLAR', 'NMDW', 'NMZL', 'HELQ', 'HAQS', 'HNLY', 'GUAN', 'GDZH', 'HLMH', 'NMAL', 'SDCY', 'JSYC', 'ZJJD', 'XIAM', 'GDST', 'HLWD', 'CHUN', 'LNDD', 'JSNT', 'ZJZS', 'FJPT', 'HLHG', 'JLYJ', 'JLCB', 'SDRC', 'ZJWZ', 'HLFY']} #CMNC_UPD
# site_group = {1:['SCPZ', 'YNLA', 'YNDC', 'KMIN', 'XIAG', 'YNYL', 'YNMH', 'YNTH', 'YNML', 'YNYM', 'YNLC', 'YNMO', 'YNSD', 'YNJD', 'YNCX', 'YNGM', 'YNSM', 'YNHZ', 'YNYA', 'YNMZ', 'YNJP']}
show = True
space_resolution = 1.5
# site_group = {}
PlotBasemap.Plot_basemap_site(CRD_file = crd_file, SHP_file = shp_file, Site_group = site_group, Space_resolution = space_resolution)



