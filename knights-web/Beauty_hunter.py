import requests
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import xlsxwriter
import pandas as pd
import re

PATH_COMUNI = 'D:\RegioniComuni';
PATH_EXCEL = r'D:\RegioniExcels\beauticians';
URL_GOOGLE = 'https://www.google.it';


def start():
    browser = webdriver.Chrome(r'C:\Users\simone\Desktop\chromedriver.exe');
    browser.get(URL_GOOGLE);
    browser.find_element_by_id("L2AGLb").click()
    return browser


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
        tt=tt.strip()
        tt=tt.replace(" ","")
        if (re.search("Telefono", tt)):
            tmp=re.search("[0-9]{11}",tt)
            if(tmp):
                telefono=tmp.group(0)
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
        telefono=formatTel(telefono)
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





def formatTel(telefono):
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




def run(browser, com, provincia, isStarted):
    search = browser.find_element_by_name("q")
    done = False;
    dataframe = pd.DataFrame(columns=['Nome', 'Indirizzo', 'Comune', 'Telefono', 'note'])
    while not done:
        try:
            search.clear()
            search.send_keys("estetisti vicino " + com + "," + provincia)
            search.submit()
            if (isStarted):
                showAll = browser.find_elements_by_tag_name("g-more-link")[0]
                showAll.click()
            done = True
        except:
            search.clear()
            try:
                search.send_keys("estetisti vicino " + com + "," + provincia + " maps")
                search.submit()
                if (isStarted):
                    showAll = browser.find_elements_by_tag_name("g-more-link")[0]
                    showAll.click()
                done = True
            except:
                print("errore, salto il comune di " + com)
                return dataframe
    # time.sleep(1)
    lista = browser.find_element_by_xpath('//*[@id="rl_ist0"]/div/div[1]/div[4]');
    done = False
    elementi = None
    tried = 10
    while not done:
        if (tried == 0):
            done = True
        if (lista):
            elementi = lista.find_elements_by_class_name("cXedhc")
            if (len(elementi) > 0):
                done = True;
        else:
            tried -= 1
    print("numero elementi: ", len(elementi))
    index = 0
    presi = 0

    for e in elementi:
        is_hairdresser = False
        details = e.text.split("\n")
        for d in details:
            if (re.search("Centro estetico", d, re.IGNORECASE)):
                is_hairdresser = True
            elif (re.search("estetico", d, re.IGNORECASE)):
                is_hairdresser = True
            elif (re.search("accademia", d, re.IGNORECASE)):
                is_hairdresser = True
            elif (re.search("center", d, re.IGNORECASE)):
                is_hairdresser = True
            elif (re.search("beauty", d, re.IGNORECASE)):
                is_hairdresser = True

        browser.execute_script("document.querySelector('.gXmnc').scrollTo(0, " + str(index) + ");")
        if (is_hairdresser):
            try:
                e.click()
            except:
                print("non riesco a cliccare")
            time.sleep(1)
            nome, telefono, indirizzo, comune, chiuso = get_data(browser)
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

        index += 130
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
    file = open(os.path.join(PATH_COMUNI, regioni[int(caccia) - 1]));
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
                dataframe.to_excel(writer, sheet_name='estetisti in ' + nome_provincia)
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
                    hunt=pd.DataFrame(columns=['Nome', 'Indirizzo', 'Comune', 'Telefono', 'note'])
                    try:
                        if (tried == 3):
                            done = True
                        else:
                            tried += 1
                            hunt = run(browser, str(line), nome_provincia, isStarted)
                            dataframe = pd.concat([dataframe, hunt])
                            done = True;
                    except:
                        print("riprovo la caccia")
                    finally:
                        isStarted = False

            else:
                pass;




