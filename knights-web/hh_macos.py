#! /usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import xlsxwriter
import pandas as pd
import re
import asyncio
from selenium.webdriver.chrome.options import Options

# PATH_COMUNI = 'D:\RegioniComuni';
# PATH_EXCEL = r'D:\RegioniExcels\hairdressers';
URL_GOOGLE = 'https://www.google.it';

PATH_COMUNI = "/Users/simonelopez/Documents/RegioniComuni"
PATH_EXCEL = "/Users/simonelopez/Documents/RegioniExcel"

def formatTel(telefono):
    telefono = str(telefono)
    if (telefono[0] == '0'):
        prefix = telefono[:4]
        rest = telefono[4:]
        telefono = str(prefix) + ' ' + str(rest)
    elif (telefono[0] == '3'):
        prefix = telefono[:3]
        rest = telefono[3:]
        telefono = str(prefix) + ' ' + str(rest)
    return telefono


def start():
    options = Options()
    options.headless = True
    browser = webdriver.Chrome("/Users/simonelopez/Documents/chromedriver/chromedriver");
    browser.get(URL_GOOGLE);
    browser.find_element(By.ID, "L2AGLb").click()
    return browser


def match_key(details):
    is_matching=False
    for d in details:
        if (re.search("Parrucchiere", d, re.IGNORECASE)):
            is_matching = True
        elif (re.search("Centro di formazione", d, re.IGNORECASE)):
            is_matching = True
        elif (re.search("Barbiere", d, re.IGNORECASE)):
            is_matching = True
        elif (re.search("Hair", d, re.IGNORECASE)):
            is_matching = True
        elif (re.search("estetic", d, re.IGNORECASE)):
            is_matching = True
    return is_matching

def get_data(data):
    telefono = None
    indirizzo = None
    comune = None
    nome = None
    chiuso = False
    #data = browser.find_elements(By.CLASS_NAME, "t3HED")[0]
    testo = data.text
    testi = testo.split("\n")
    nome = testi[0]
    testi_tel = []
    for k in range(len(testi)):
        testi_tel.append(testi[k].replace(" ", ""))
    for tt in testi_tel:
        tt = tt.strip()
        tt = tt.replace(" ", "")
        if (re.search("Telefono", tt)):
            tmp = re.search("[0-9]{11}", tt)
            if (tmp):
                telefono = tmp.group(0)
            else:
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
        telefono = formatTel(telefono)
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
    if (nome): nome = nome.replace(",", " ")
    if (indirizzo): indirizzo = indirizzo.replace(",", " ")
    return nome, telefono, indirizzo, comune, chiuso


def run(browser, com, provincia, isStarted):
    done = False;
    search = browser.find_element(By.NAME, "q")
    dataframe = pd.DataFrame(columns=['Nome', 'Indirizzo', 'Comune', 'Telefono', 'note'])
    while not done:

        try:
            search.clear()
            search.send_keys("parrucchieri vicino " + com + "," + provincia)
            search.submit()
            if (isStarted):
                print(browser.execute_script("return document.documentElement.outerHTML"))
                showAll = browser.find_elements(By.TAG_NAME, "g-more-link")[0]
                showAll.click()
            done = True
        except:
            search.clear()
            try:
                search.send_keys("parrucchieri vicino " + com + "," + provincia + " maps")
                search.submit()
                if (isStarted):
                    showAll = browser.find_elements(By.TAG_NAME, "g-more-link")[0]
                    showAll.click()
                done = True
            except:
                print("errore, salto il comune di " + com)
                return dataframe
    current_url = browser.current_url
    # time.sleep(1)
    doneclicked=False
    while not doneclicked:
        try:
            lista = browser.find_element(By.XPATH, '//*[@id="rl_ist0"]/div/div[1]/div[4]');
            elementi = None
            if (lista):
                elementi = lista.find_elements(By.CLASS_NAME, "cXedhc")
                if (len(elementi) > 0):
                    print("numero elementi: ", len(elementi))
                    index=50
                    presi=0
                    lastData=None
                    for e in elementi:
                        details=e.text.split("\n")
                        isToTake=match_key(details)
                        if(isToTake):
                            e.click()
                            time.sleep(2)
                            done=False
                            while not done:
                                data = browser.find_elements(By.CLASS_NAME, "t3HED")[0]
                                if(data and data!=lastData):
                                    lastData=data
                                    nome, telefono, indirizzo, comune, chiuso = get_data(data)
                                    done=True
                                else:
                                    time.sleep(2)
                            if (indirizzo == None):
                                indirizzo = "N/A"
                            if (telefono == None):
                                telefono = "N/A"
                            if (comune == None):
                                comune = "N/A"
                            taken = False
                            result = None
                            if (comune):
                                result = re.match(com.lower(), comune.strip().lower())
                            if (result and nome):

                                if ((dataframe["Nome"] == nome).any() and (dataframe["Comune"] == comune).any()):
                                    pass
                                else:
                                    note = ""
                                    if (chiuso):
                                        note = "Chiuso temporaneamente"
                                    dataframe.loc[presi] = [nome, indirizzo, comune, telefono, note]
                                    presi += 1;
                                    taken = True
                            print("Nome: " + nome)
                            print("Telefono: " + telefono)
                            print("Indirizzo: " + indirizzo)
                            print("Comune: " + comune)
                            print("Chiuso temp:", chiuso)
                            print("Preso:", taken)
                            print("\n")
                            index=index+150
                            doneclicked=True
                            browser.execute_script("document.querySelector('.rl_full-list').scrollTo(0, " + str(index) + ");")
        except:
            print("ricarico pagina")
            #browser.get(current_url)
    print(presi)
    return dataframe;


if __name__ == '__main__':
    print("Quale regione vuoi che io cacci?")
    regioni = []
    index = 1
    for file in os.listdir(PATH_COMUNI):
        regione = file.split('.')[0]
        regioni.append(file)
        print(index, regione)
        index += 1;
    caccia = input();
    regione = regioni[int(caccia) - 1].split(".")[0]
    file = open(os.path.join(PATH_COMUNI, regioni[int(caccia) - 1]), encoding="ISO-8859-1");
    path_regione = os.path.join(PATH_EXCEL, regione)
    exist_regione = os.path.isdir(path_regione)

    if (not exist_regione):
        os.mkdir(path_regione);
    else:
        print("la regione esiste", regione)
    uno = True
    dataframe = 0;
    writer = 0;
    nome_regione = 0
    presi = 0
    browser = start()
    isStarted = True
    while uno:
        provincia_already_done = False
        line = file.readline()
        if (line.split(" ")[0] == 'PROVINCIA'):
            dataframe = pd.DataFrame(columns=['Nome', 'Indirizzo', 'Comune', 'Telefono', 'note'])
            # path_regione=os.path.join(PATH_EXCEL,regione);
            nome_provincia = line.split(" ")[2].strip()
            path_provincia = os.path.join(path_regione, nome_provincia + (".xlsx"))
            exist_provincia = os.path.isfile(path_provincia)

            if (not exist_provincia):
                writer = pd.ExcelWriter(path_provincia, engine="xlsxwriter")
                presi = 0
            else:
                print("la provincia " + nome_provincia + " l'ho già cacciata")
        elif (line == '\n' or len(line) == 0):
            if (not exist_provincia):
                dataframe.to_excel(writer, sheet_name='parrucchieri in ' + nome_provincia.split("-")[0])
                print("############################################fine provincia", nome_provincia)
                writer.save();
            else:
                pass;
            if (len(line) == 0):
                uno = False;

        else:
            if (not exist_provincia):
                print("sto cercando " + line);
                line = line.strip().lower()
                done = False
                tried = 0
                while not done:
                    hunt = pd.DataFrame(columns=['Nome', 'Indirizzo', 'Comune', 'Telefono', 'note'])
                    try:
                        if (False):
                            done = True
                        else:
                            tried += 1
                            hunt = run(browser, str(line), nome_provincia, isStarted)
                            hunt2 = run(browser, str(line), nome_provincia, isStarted)
                            dataframe = pd.concat([dataframe, hunt,hunt2])
                            dataframe= dataframe.drop_duplicates(subset=['Telefono'])
                            done = True;
                    except:
                        print("riprovo la caccia")
                    finally:
                        isStarted = False

            else:
                pass;
