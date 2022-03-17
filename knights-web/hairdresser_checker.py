import pandas as pd
import xlsxwriter
import os
from selenium import webdriver
import time
import re

PATH_EXCEL=r'D:\RegioniExcels\hairdressers';
URL_GOOGLE='https://maps.google.com/maps';
pd.set_option('display.max_columns', None)
if __name__ == '__main__':
    print("quale regione vuoi che io controlli?")
    index=1
    regioni=[]
    for regione in os.listdir(PATH_EXCEL):
        print(index,regione)
        regioni.append(regione)
        index+=1
    check=input()
    regione=regioni[int(check)-1]
    PATH_PROVINCIE=PATH_EXCEL+"\\"+regione
    print("quale provincia vuoi che io controlli?")
    provincie=[]
    index=1
    for provincia in os.listdir(PATH_PROVINCIE):
        print(index,provincia)
        provincie.append(provincia)
        index+=1
    check=input()
    provincia=provincie[int(check)-1]
    PATH_FILE=PATH_PROVINCIE+"\\"+provincia
    df=pd.read_excel(PATH_FILE)
    indice=input("da che indice vuoi che io cominci?")

    df=df[["Nome","Indirizzo","Comune","Telefono","note","interazioni","risposta"]]
    browser = webdriver.Chrome(r'C:\Users\simone\Desktop\chromedriver.exe');
    browser.get(URL_GOOGLE);
    buttons = browser.find_elements_by_tag_name("button")

    for el in buttons:
        if (el.text == "Accetto"):
            el.click()
            break
    cambiati=0
    nomi=[]
    fatti=0
    for i in range(int(indice),len(df)):
        if(len(str(df.loc[i]["Telefono"]).replace(" ",""))==9 or len(str(df.loc[i]["Telefono"]).replace(" ",""))==10):
            nome=df.loc[i]["Nome"]
            indirizzo=df.loc[i]["Indirizzo"]
            comune=df.loc[i]["Comune"]
            telefono=str(df.loc[i]["Telefono"]).replace(" ","")
            note=df.loc[i]["note"]
            interazioni=df.loc[i]["interazioni"]
            risposta=df.loc[i]["risposta"]

            search = browser.find_element_by_name("q")
            done = False;
            search.clear()
            search.send_keys(str(nome)+" "+str(indirizzo)+" "+str(comune))

            searchBox=browser.find_elements_by_class_name("xoLGzf-BIqFsb-haAclf")[0]
            lente=searchBox.find_elements_by_tag_name("button")[0]
            lente.click()
            # for q in lente:
            #     if(q.text=="Cerca"):
            #         q.click();
            done=False
            tried=3
            while (not done or tried==0):
                body=browser.find_element_by_id("pane")
                if(body):
                    done=True
                else:
                    search = browser.find_element_by_name("q")
                    search.clear()
                    search.send_keys(str(nome) + " " + str(indirizzo) + " " + str(comune))
                    searchBox = browser.find_elements_by_class_name("xoLGzf-BIqFsb-haAclf")[0]
                    lente = searchBox.find_elements_by_tag_name("button")[0]
                    lente.click()
                    tried-=1
            if(tried==0):
                pass
            else:
                result = None
                testi=None
                done=False
                while not done:
                    testi = body.text
                    testi = testi.split("\n")
                    if(len(testi)>1):
                        for j in range(len(testi)):
                            testi[j] = testi[j].replace(" ", "")

                        for t in testi:
                            result=re.search("[0-9]{10}",t)
                            if(result):
                                if (telefono != result.group(0)):
                                    cambiati += 1
                                    nomi.append(nome)
                                    print(i,str(telefono), result.group(0), "cambiato: ", nome, comune)
                                else:
                                    print(i,str(telefono), result.group(0))
                            else:
                                result=re.search("[0-9]{9}",t)
                                if (result):
                                    if(str(telefono)!=result.group(0)):
                                        cambiati+=1
                                        nomi.append(nome)
                                        print(i,str(telefono), result.group(0),"cambiato: ", nome, comune)
                                    else:
                                        print(i,str(telefono), result.group(0))
                                        # df.loc[i]["Telefono"]=result.group(0)
                        done=True
                        fatti+=1
                    else:
                        result = None
                        testi = None