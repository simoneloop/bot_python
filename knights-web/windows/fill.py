import pandas as pd
import json
import os


def fill(x,dict):
    if((x['Cap']==None or x['Cap']=="") and x['Comune']):
        x['Cap']=dict[x['Comune'].lower()]
    return x
region=json.load(open(os.path.join(r"D:\bot_python\knights-web\windows\italy_regions","campania_prova.json"),encoding='UTF-8'))
df=pd.read_excel(r"D:\bot_python\knights-web\windows\estetisti\calabria_prova\crotone.xlsx")
df = df.apply(lambda x: fill(x, region['province'][0]['mapping']), axis=1)