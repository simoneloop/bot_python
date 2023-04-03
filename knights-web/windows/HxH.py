import requests
import selenium
import json
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import pandas as pd
import re
from selenium.webdriver.chrome.options import Options
from threading import Thread
import math
import numpy as np
import sys, os

chrome_options = Options()
chrome_options.add_argument("--headless")
URL_GOOGLE = 'https://www.google.it';

service = Service(executable_path=ChromeDriverManager().install())


typo_list=os.listdir(r"D:\bot_python\knights-web\windows\typos")
regions_list=os.listdir(r"D:\bot_python\knights-web\windows\italy_regions")
tmp={}

def fill(x,dict):
    if(math.isnan(float(x['Cap']))):
        if(x['Comune']!=None and str(x['Comune']).lower() in dict['mapping']):
            x['Cap']=dict['mapping'][str(x['Comune']).lower()]
        elif(x['Comune']==None):
            x['comune']='controllare'
        else:
            x['Nome'] = None
            x['Indirizzo'] = None
            x['Telefono'] = None
            x["Comune"] = None
            x["Sito web"] = None
    else:
        cap=str(int(float(x['Cap'])))
        if(not cap in dict['caps']):
            x['Nome']=None
            x['Indirizzo']=None
            x['Telefono']=None
            x["Comune"] = None
            x["Sito web"] = None
        else:
            x['Cap']=cap
    return x

def formatTel(telefono):
    if(telefono=="N/A"):
        return telefono
    telefono=str(telefono)
    if (telefono[0] == '0'):
        prefix = telefono[:4]
        rest = telefono[4:]
        telefono = str(prefix)+' '+str(rest)
    elif (telefono[0] == '3'):
        prefix = telefono[:3]
        rest = telefono[3:]
        telefono = str(prefix) + ' ' + str(rest)
    return telefono

def get_link(elem):
    link = elem.find_element(By.CLASS_NAME, "VkpGBb")
    link = link.find_elements(By.TAG_NAME, "a")
    for l in link:
        if(l.text=="SITO WEB"):
            return l.get_attribute("href")
    return None

def get_data(value):
    value=value.split('\n')
    numero=None
    comune=None
    nome = value[0]
    for i in value:
        found=False
        tmp=i.split('·')
        for j in range(len(tmp)):
            tmpT=tmp[j].replace(" ","")
            if(re.search(r"[0-9]{9}",tmpT)):
                found=True
                numero=tmpT
            if(found):
                comune=tmp[j-1].strip().split(" ")[:-1]
                comune=(" ").join(comune)
    return nome,comune,numero

def respect_keywords(value):
    values=value.split("\n")
    for v in values:
        tmp=v.split("·")
        for t in tmp:
            if(t.lower().strip()in typo["keywords"]):
                return True
    return False





for i in range(len(typo_list)):
    tmp[i]=typo_list[i].split(".")[0]

for i in range(len(tmp)):
    print(i,tmp[i])
key=input("tipo di azienda da cercare: ")


typo=json.load(open(os.path.join(r"D:\bot_python\knights-web\windows\typos",tmp[int(key)]+".json")))
typo_path=tmp[int(key)]
for i in range(len(regions_list)):
    print(i,regions_list[i])
reg=input("regione in quale cercarla")

region=json.load(open(os.path.join(r"D:\bot_python\knights-web\windows\italy_regions",regions_list[int(reg)]),encoding='windows-1252'))

def contains(list,com):
    com=str(com).lower().replace("\(","")
    for l in list:
        tmpL=str(l).lower()
        if(re.search(com,tmpL)):
            return True
    return False
def hunt(typo,prov):
    #browser = webdriver.Chrome(service=service, options=chrome_options)
    browser = webdriver.Chrome(service=service)
    browser.get(URL_GOOGLE);
    dataframe = pd.DataFrame(columns=['Nome','Indirizzo','Comune','Cap', 'Telefono', 'Sito web'])

    browser.find_elements(By.ID, "L2AGLb")[0].click()
    for com in prov['comuni']:
        finished = False

        while (not finished):

            try:
                print("mappo: ", com)
                browser.get(URL_GOOGLE);
                com=com.lower()
                search = browser.find_element(By.NAME, "q")
                search.clear()
                search.send_keys(typo["id"]," vicino "+com+", "+prov['capoluogo'])
                search.submit()

                try:
                    showAll = browser.find_elements(By.TAG_NAME,"g-more-link")[0]
                    showAll.click()
                    found=False
                    tried = 0
                    while ((not found) and (tried<3)):
                        tried += 1
                        time.sleep(2)
                        elementi=browser.find_elements(By.CLASS_NAME,"uMdZh")
                        time.sleep(1)
                        if(len(elementi)>5):
                            found=True
                        else:
                            browser.close()
                            browser = webdriver.Chrome(service=service)
                            browser.get(URL_GOOGLE);

                            browser.find_elements(By.ID, "L2AGLb")[0].click()
                            search = browser.find_element(By.NAME, "q")
                            search.send_keys(typo["id"]," vicino "+com+", "+prov['capoluogo'])
                            search.submit()
                            showAll = browser.find_elements(By.TAG_NAME, "g-more-link")[0]
                            showAll.click()
                            time.sleep(2)
                            elementi = browser.find_elements(By.CLASS_NAME, "uMdZh")
                            time.sleep(1)
                            print("elementi ",len(elementi))
                            if (len(elementi) > 5):
                                found = True
                    atleastone=True
                    cunt=0

                    while atleastone:
                        elementi = browser.find_elements(By.CLASS_NAME, "uMdZh")
                        atleastone = False

                        for i in range(len(elementi)):
                            try:
                                el=browser.find_elements(By.CLASS_NAME, "uMdZh")[i]
                                testo=el.text
                                indirizzo=None
                                nome, comune, numero=get_data(testo)
                                if(numero==None):
                                    numero="N/A"
                                respect_key=respect_keywords(testo)

                                link=get_link(el)
                                dict = {}
                                if(comune!=None):
                                    comune=comune.split("(")
                                    comune=(" ").join(comune)
                                if(comune!=None and re.search(comune,com) and respect_key):
                                    atleastone=True


                                    dict["Nome"] = nome
                                    dict["Comune"] = comune
                                    dict["Telefono"] = formatTel(numero) if numero!=None else "N/A"
                                    dict["Sito web"] = link



                                    cunt+=1

                                elif( (comune==None or(comune!=None and not contains(prov['comuni'],comune.lower())))  and respect_key):

                                    el=browser.find_elements(By.CLASS_NAME, "uMdZh")[i]
                                    toclick = el.find_element(By.CLASS_NAME, "VkpGBb")
                                    toclick =toclick.find_elements(By.TAG_NAME, "a")[0]

                                    time.sleep(1)
                                    toclick.click()
                                    time.sleep(1)
                                    cap = None
                                    data = browser.find_elements(By.CLASS_NAME,"t3HED")[0]
                                    testo = data.text
                                    testi = testo.split("\n")

                                    for t in testi:

                                        if (re.search(r"Indirizzo:", t)):
                                            tmp = re.split(r"Indirizzo:", t)
                                            indirizzo = tmp[1]
                                            if (re.search("\s[0-9]{5}\\b", indirizzo)):
                                                s = re.split("\s[0-9]{5}\\b", indirizzo)
                                                cap = re.search("\s[0-9]{5}\\b", indirizzo)
                                                if(cap):
                                                    cap=str(cap.group(0))
                                                indirizzo = s[0].strip()
                                                cap = cap.strip()
                                                dict["Cap"]=cap
                                                s = s[1].strip()
                                                s = re.split("[A-Z]{2}", s)
                                                comune = s[0].strip()

                                            else:
                                                lista = indirizzo.split(",")
                                                for l in lista:
                                                    if (re.search("[A-Z]{2}", l)):
                                                        lista.remove(l)
                                                        indirizzo = ','.join(lista)
                                                        comune = re.split("[A-Z]{2}", l)[0]
                                    taken=False
                                    if (indirizzo!=None):
                                        indirizzo = indirizzo.strip().replace(",","")

                                    if (comune!=None and comune.lower() == com.lower()):
                                        taken = True

                                    else:
                                        # print("provo a vedere se per ogni comune in prov  comuni trovo la stringa in indirizzo")
                                        for c in prov['comuni']:
                                            if(indirizzo!=None):
                                                indirizzo=indirizzo.replace('[";:,.\/?\\-]', '').lower()
                                                if(re.search(c.lower(),indirizzo)):
                                                    indirizzo=indirizzo.replace(c.lower(),"")
                                                    comune=c.lower()
                                                    abbr = re.search("[a-z]{2}", indirizzo)
                                                    if(abbr):
                                                        indirizzo=indirizzo.replace(abbr.group(0),"")
                                                    taken=True



                                    if(not taken):

                                        if(cap and str(cap) in prov['caps']):
                                            comune=None
                                            taken=True


                                    if(taken):
                                        atleastone = True
                                        dict["Nome"] = nome
                                        dict["Comune"] = comune
                                        dict["Indirizzo"]=indirizzo
                                        dict["Telefono"] = formatTel(numero) if numero!=None else "N/A"
                                        dict["Sito web"] = link
                                        cunt += 1
                                df=pd.DataFrame(dict,index=[0])
                                print(df)
                                dataframe=pd.concat([dataframe,df])
                            except Exception as e:

                                print("primo errore",e)
                                exc_type, exc_obj, exc_tb = sys.exc_info()
                                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                                print(exc_type, fname, exc_tb.tb_lineno)
                                i-=1
                        if(atleastone):
                            try:
                                next = browser.find_element(By.ID, "pnnext")
                                next.click()
                                time.sleep(2)
                            except Exception as e:
                                print("secondo errore",e)

                                atleastone=False
                            print("##################################")
                    print("trovati a: ",com," : " ,cunt)
                except Exception as e:
                    print("terzo errore",e)
                    pass

                finally:
                    finished=True
            except Exception as e:
                # print(e)
                time.sleep(60)

    cond_nan = np.where(dataframe['Telefono'] == 'N/A')
    i_nan = (dataframe.iloc[cond_nan])
    dataframe=dataframe.drop_duplicates(subset=["Telefono"],keep="last")
    dataframe=pd.concat([dataframe,i_nan])
    dataframe=dataframe.drop_duplicates(subset=['Nome','Telefono'])
    dataframe = dataframe.apply(lambda x: fill(x, prov), axis=1)
    dataframe = dataframe.dropna(how="all")
    exist_typo=os.path.isdir(typo_path)
    if(not exist_typo):
        os.mkdir(typo_path)
    path_regione = os.path.join(typo_path, regions_list[int(reg)].split(".")[0])
    exist_regione = os.path.isdir(path_regione)

    if (not exist_regione):
        os.mkdir(path_regione);
    path_final=os.path.join(path_regione,prov['capoluogo'] + ".xlsx")
    if(not os.path.isfile(path_final)):
        dataframe.to_excel(path_final, index=False)
    else:
        dft=pd.read_excel(path_final)
        dft=pd.concat([dft,dataframe])
        cond_nan = np.where(dft['Telefono'] == 'N/A')
        i_nan = (dft.iloc[cond_nan])
        dft = dft.drop_duplicates(subset=["Telefono"], keep="last")
        dft = pd.concat([dft, i_nan])
        dft = dft.drop_duplicates(subset=['Nome', 'Telefono'], keep="last")
        dft.to_excel(path_final, index=False)


nThread=len(region['province'])
for i in range(nThread):
    for j in range(len(region['province'][i]['comuni'])):
        region['province'][i]['comuni'][j] =region['province'][i]['comuni'][j].lower()
    t = Thread(target=hunt, args=(typo, region['province'][i],))
    t.start()