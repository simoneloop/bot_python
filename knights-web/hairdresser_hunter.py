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
from dog import hairdresser_support as imp

PATH_COMUNI='D:\RegioniComuni';
PATH_EXCEL='D:\RegioniExcels';
URL_GOOGLE='https://www.google.it';





if __name__ == '__main__':
    print("Quale regione vuoi che io cacci?")
    regioni=[]
    index=1
    for file in os.listdir(PATH_COMUNI):
        regione=file.split('.')[0]
        regioni.append(file)
        print(index,regione)
        index+=1;
    caccia = input();
    regione=regioni[int(caccia)-1].split(".")[0]
    file=open(os.path.join(PATH_COMUNI,regioni[int(caccia)-1]));
    path_regione=os.path.join(PATH_EXCEL,regione)
    exist_regione=os.path.isdir(path_regione)

    if(not exist_regione):
        os.mkdir(path_regione);
    else:
        print("la regione esiste", regione)
    uno=True
    dataframe=0;
    writer=0;
    nome_regione=0
    presi = 0
    while uno:
        provincia_already_done=False
        line=file.readline()
        if(line.split(" ")[0]=='PROVINCIA'):
            dataframe = pd.DataFrame(columns=['Nome', 'Indirizzo', 'Comune', 'Telefono','note'])
            # path_regione=os.path.join(PATH_EXCEL,regione);
            nome_provincia=line.split(" ")[2].strip()
            path_provincia=os.path.join(path_regione,nome_provincia+(".xlsx"))
            exist_provincia=os.path.isfile(path_provincia)

            if(not exist_provincia):
                writer=pd.ExcelWriter(path_provincia,engine="xlsxwriter")
                presi = 0
            else:
                print("la provincia "+nome_provincia+" l'ho già cacciata")
        elif(line=='\n' or len(line)==0):
            if(not exist_provincia):
                dataframe.to_excel(writer, sheet_name='parrucchieri in '+nome_provincia)
                print("############################################fine provincia",nome_provincia)
                writer.save();
            else:
                pass;
            if(len(line)==0):
                    uno = False;

        else:
            if (not exist_provincia):
                print("sto cercando "+line);
                line=line.strip().lower()
                done=False
                tried=0
                while not done:
                    try:
                        if(tried==3):
                            done=True
                        else:
                            tried+=1
                            hunt=imp.run(str(line),nome_provincia)
                            done=True;
                    except:
                        print("riprovo la caccia")
                dataframe=pd.concat([dataframe,hunt])
            else:
                pass;



            



