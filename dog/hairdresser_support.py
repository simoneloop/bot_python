import requests
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import xlsxwriter
import pandas as pd
from selenium.webdriver.common.by import By
import re
URL_MAPS='https://www.google.it';


#def find_showall_inpage(browser):
# def get_data(browser):
#     telefono = None
#     indirizzo = None
#     comune = None
#     nome=None
#     chiuso=False
#     data= browser.find_elements_by_class_name("t3HED")[0]
#     testo=data.text
#     testi = testo.split("\n")
#     nome=testi[0]
#     for k in range(len(testi)):
#         testi[k]=testi[k].replace(" ","")
#     for t in testi:
#         if(re.search("Telefono:",t)):
#             tmp=re.search("[0-9]{10}",t)
#             if(tmp):
#                 telefono=tmp.group(0)
#             else:
#                 tmp=re.search("[0-9]{9}",t)
#             if(tmp):
#                 telefono=tmp.group(0)
#         if(re.search("Indirizzo:",t)):
#             tmp=re.split("Indirizzo:",t)
#             indirizzo=tmp[1]
#             if(re.search("[0-9]{5}", indirizzo)):
#                 s = re.split("[0-9]{5}", indirizzo)
#                 indirizzo = s[0].strip()
#                 s = s[1].strip()
#                 s = re.split("[A-Z]{2}", s)
#                 comune = s[0].strip()
#             else:
#                 lista=indirizzo.split(",")
#                 for l in lista:
#                     if(re.search("[A-Z]{2}", l)):
#                         lista.remove(l)
#                         indirizzo=','.join(lista)
#                         comune=re.split("[A-Z]{2}", l)[0]
#     if(nome):
#         if (re.match("Chiuso temporaneamente", nome)):
#             chiuso = True
#             nome = testi[2]
#         nome = nome.strip()
#         if(nome==" " or nome==""):nome=None
#     else:
#         nome=None
#     if(telefono):
#         telefono=telefono.strip()
#         if(telefono==" " or telefono==""):telefono=None
#     else:
#         telefono=None
#     if(indirizzo):
#         indirizzo=indirizzo.strip()
#         if(indirizzo==" "or indirizzo==""):indirizzo=None
#     else:
#         indirizzo=None
#     if(comune):
#         comune=comune.strip()
#         if(comune==" " or comune==""):comune=None
#     else:
#         comune=None
#     return nome,telefono,indirizzo,comune,chiuso

def get_data(browser):
    telefono = None
    indirizzo = None
    comune = None
    nome = None
    chiuso = False
    data = browser.find_elements_by_class_name("t3HED")[0]
    testo = data.text
    testi = testo.split("\n")
    nome = testi[0]
    testi_tel = []
    for k in range(len(testi)):
        testi_tel.append(testi[k].replace(" ", ""))
    for tt in testi_tel:
        if (re.search("Telefono", tt)):
            tmp = re.search("[0-9]{10}", tt)
            if (tmp):
                telefono = tmp.group(0)
            else:
                tmp = re.search("[0-9]{9}", tt)
            if (tmp):
                telefono = tmp.group(0)
    for t in testi:
        if (re.search("Indirizzo:", t)):
            tmp = re.split("Indirizzo:", t)
            indirizzo = tmp[1]
            if (re.search("[0-9]{5}", indirizzo)):
                s = re.split("[0-9]{5}", indirizzo)
                indirizzo = s[0].strip()
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
    if (nome):
        if (re.match("Chiuso temporaneamente", nome)):
            chiuso = True
            nome = testi[2]
        nome = nome.strip()
        if (nome == " " or nome == ""): nome = None
    else:
        nome = None
    if (telefono):
        telefono = telefono.strip()
        if (telefono == " " or telefono == ""): telefono = None
    else:
        telefono = None
    if (indirizzo):
        indirizzo = indirizzo.strip()
        if (indirizzo == " " or indirizzo == ""): indirizzo = None
    else:
        indirizzo = None
    if (comune):
        comune = comune.strip()
        if (comune == " " or comune == ""): comune = None
    else:
        comune = None
    if(nome):nome = nome.replace(",", " ")
    if(indirizzo):indirizzo = indirizzo.replace(",", " ")
    return nome, telefono, indirizzo, comune, chiuso


def run(com,provincia):
    browser = webdriver.Chrome(r'C:\Users\simone\Desktop\chromedriver.exe');
    browser.get(URL_MAPS);
    browser.find_element_by_id("L2AGLb").click()
    search=browser.find_element_by_name("q")
    done=False;
    dataframe = pd.DataFrame(columns=['Nome', 'Indirizzo', 'Comune', 'Telefono','note'])
    while not done:
        try:
            search.send_keys("parrucchieri vicino " + com + "," + provincia)
            search.submit()
            showAll=browser.find_elements_by_tag_name("g-more-link")[0]
            showAll.click()
            done=True
        except:
            browser.close()
            browser = webdriver.Chrome(r'C:\Users\simone\Desktop\chromedriver.exe');
            browser.get(URL_MAPS);
            browser.find_element_by_id("L2AGLb").click()
            search = browser.find_element_by_name("q")
            try:
                search.send_keys("parrucchieri vicino " + com + "," + provincia + " maps")
                search.submit()
                showAll = browser.find_elements_by_tag_name("g-more-link")[0]
                showAll.click()
                done = True
            except:
                print("errore, salto il comune di "+com)
                browser.close()
                return dataframe
    time.sleep(1)
    lista=browser.find_element_by_xpath('//*[@id="rl_ist0"]/div/div[1]/div[4]');
    done=False
    elementi=None
    tried=10
    while not done:
        if(tried==0):
            done=True
        if(lista):
            elementi=lista.find_elements_by_class_name("cXedhc")
            if(len(elementi)>0):
                done=True;
        else:
            tried-=1
    print("numero elementi: ",len(elementi))
    # res_research=browser.find_element_by_id("search")
    # elementi=res_research.find_elements_by_xpath("./div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div/div[1]/div[4]")
    # elementi=browser.find_elements_by_class_name("rlfl__tls")
    # for e in elementi:
    #     print(e.text)
    index=0
    presi = 0

    for e in elementi:
        is_hairdresser=False
        details=e.text.split("\n")
        for d in details:
            if(re.search("Parrucchiere",d, re.IGNORECASE)):
                is_hairdresser=True
            elif(re.search("Centro di formazione",d, re.IGNORECASE)):
                is_hairdresser=True
            elif (re.search("Barbiere", d, re.IGNORECASE)):
                is_hairdresser = True
            elif (re.search("Hair", d, re.IGNORECASE)):
                is_hairdresser = True
            elif (re.search("estetic", d, re.IGNORECASE)):
                is_hairdresser = True

        browser.execute_script("document.querySelector('.gXmnc').scrollTo(0, "+str(index)+");")
        if(is_hairdresser):
            try:
                e.click()
            except:
                print("non riesco a cliccare")
            time.sleep(1)
            nome,telefono,indirizzo,comune,chiuso=get_data(browser)
            if (indirizzo == None):
                indirizzo = "N/A"
            if (telefono == None):
                telefono = "N/A"
            if (comune == None):
                comune = "N/A"
            taken=False
            result=None
            if(comune):
                result = re.match(com.lower(), comune.strip().lower())
            if(result and nome):

                if((dataframe["Nome"]==nome).any() and (dataframe["Comune"]==comune).any()):
                    pass
                else:
                    note=""
                    if(chiuso):
                        note="Chiuso temporaneamente"
                    dataframe.loc[presi] = [nome, indirizzo, comune, telefono,note]
                    presi += 1;
                    taken=True
            print("Nome: " + nome)
            print("Telefono: " + telefono)
            print("Indirizzo: " + indirizzo)
            print("Comune: " + comune)
            print("Chiuso temp:", chiuso)
            print("Preso:",taken)
            print("\n")
        index += 130
    print(presi)
    browser.close();
    return dataframe;
pd.set_option('display.max_columns', None)
print(run("albi","catanzaro"))
