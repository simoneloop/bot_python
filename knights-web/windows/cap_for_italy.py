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

chrome_options = Options()
chrome_options.add_argument("--headless")
URL_GOOGLE = 'https://www.google.it';

service = Service(executable_path=ChromeDriverManager().install())

browser = webdriver.Chrome(service=service)


regions_list=os.listdir(r"D:\bot_python\knights-web\windows\italy_regions")

for i in range(len(regions_list)):
    print(i,regions_list[i])
reg=input("regione in quale cercarla")

region=json.load(open(os.path.join(r"D:\bot_python\knights-web\windows\italy_regions",regions_list[int(reg)]),encoding='UTF-8'))



for i in region['province']:
    prov_tmp=i['capoluogo']
    i['caps']=[]
    reg_tmp=regions_list[int(reg)].split(".")[0]
    reg_tmp=reg_tmp.split("_")[0]
    url="https://www.tuttitalia.it/"+reg_tmp+"/provincia-di-"+prov_tmp+"/"
    browser.get(url);
    try:
        browser.find_element(By.ID,"cookieChoiceDismiss").click()
    except:
        pass
    finally:
        lista = browser.find_elements(By.CLASS_NAME, "od")
        try:
            lista[3].click()
        except:
            url = "https://www.tuttitalia.it/" + reg_tmp + "/provincia-dell-" + prov_tmp + "/"
            browser.get(url);
            try:
                browser.find_element(By.ID, "cookieChoiceDismiss").click()
            except:
                pass
            finally:
                lista = browser.find_elements(By.CLASS_NAME, "od")
                lista[3].click()


        tutte_le_righe = browser.find_elements(By.TAG_NAME, "tr")
        time.sleep(2)
        for j in range(len(tutte_le_righe)):
            cap=re.search("\s[0-9]{5}\\b", tutte_le_righe[j].text)
            if (cap):
                s = tutte_le_righe[j].text.replace(cap.group(0),"")
                comune=s.strip().lower()
                cap=cap.group(0).strip()
                if(len(comune)<50):
                    try:
                        if(comune not in i['comuni']):
                            i['comuni'].append(comune)
                    except:
                        i['comuni']=[]
                        i['comuni'].append(comune)
                    try:
                        i['mapping'][comune] = cap
                    except:
                        i['mapping']={}
                        i['mapping'][comune] = cap
                    if (cap not in i['caps']):
                        i['caps'].append(cap)
with open("./italy_regions/"+regions_list[int(reg)], "w") as outfile:
    json.dump(region,outfile,indent=4,ensure_ascii=False)





