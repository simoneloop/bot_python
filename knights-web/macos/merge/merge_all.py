import os

import pandas as pd
import numpy as np
import xlsxwriter


def format_telephone(telefono):
    telefono=str(telefono)
    telefono=telefono.strip()
    telefono=telefono.replace(" ","")
    if (telefono[0] == '0'):
        prefix = telefono[:4]
        rest = telefono[4:]
        telefono = str(prefix)+' '+str(rest)
    elif (telefono[0] == '3'):
        prefix = telefono[:3]
        rest = telefono[3:]
        telefono = str(prefix) + ' ' + str(rest)
    return telefono

def merge(lista_nuovi,esistente=None):
    path_dest=lista_nuovi[0].split('.')[0].split('-')[0]+'-merged.xlsx'
    dataframe=pd.DataFrame()
    for e in lista_nuovi:
        df_tmp=pd.read_excel(e)
        dataframe=pd.concat([dataframe,df_tmp], ignore_index=True)
    dataframe=dataframe.drop_duplicates(subset=['Nome','Telefono'])
    dataframe['interazioni'] = " "
    dataframe['risposta'] = " "

    if(esistente!=None):
        path_merge_1 = esistente
        df_e = pd.read_excel(path_merge_1)
        df_b = pd.DataFrame(dataframe)
        df_b=df_b.reset_index()

        df_res = pd.DataFrame(columns=['Nome', 'Indirizzo', 'Comune', 'Telefono', 'note', 'interazioni', 'risposta'])
        # df_e=df_e.drop(columns=['REGIONE','PROVINCIA','FACEBOOK','INSTAGRAM','NEXT'])
        intersezioni = 0
        index = 0
        index_rimossi_e = []
        index_rimossi_b = []
        for i in range(len(df_e)):
            nome_e = str(df_e.loc[i]['Nome']).strip()
            comune_e = str(df_e.loc[i]['Comune']).strip()
            for j in range(len(df_b)):
                nome_b = str(df_b.loc[j]['Nome']).strip()
                comune_b = str(df_b.loc[j]['Comune']).strip()
                telStrip = str(df_b.loc[j]['Telefono']).replace(" ", "")
                telStripE= str(df_e.loc[i]['Telefono']).replace(" ", "")
                df_b.loc[j]['Telefono'] = str(telStrip)
                if ((nome_e.lower() == nome_b.lower() and(comune_e.lower() == comune_b.lower())) or telStripE==telStrip):
                    tmp = pd.DataFrame([[nome_e, df_e.loc[i]['Indirizzo'], df_e.loc[i]['Comune'],
                                         str(df_e.loc[i]['Telefono']).replace(" ", ""), "", df_e.loc[i]['interazioni'],
                                         df_e.loc[i]['risposta']]],
                                       columns=['Nome', 'Indirizzo', 'Comune', 'Telefono', 'note', 'interazioni',
                                                'risposta'])
                    df_res = pd.concat([df_res,tmp])
                    intersezioni += 1
                    index_rimossi_e.append(i)
                    index_rimossi_b.append(j)
        df_e = df_e.drop(index_rimossi_e)
        df_b = df_b.drop(index_rimossi_b)
        print("in comune", intersezioni)
        print("in più nel primo: ", len(df_e))
        print("in più nel secondo: ", len(df_b))
        df_res = pd.concat([df_res, df_e])
        df_res = pd.concat([df_res, df_b])
        df_res['Telefono'] = df_res['Telefono'].fillna('N/A')
        df_res['Telefono'] = df_res['Telefono'].apply(lambda x: format_telephone(str(x)))
        cond_nan = np.where(df_res['Telefono'] == 'nan')
        cond_NA = np.where(df_res['Telefono'] == 'N/A')
        i_nan = pd.DataFrame()
        i_NA = pd.DataFrame()
        i_nan = (df_res.iloc[cond_nan])
        i_NA = (df_res.iloc[cond_NA])
        df_res = df_res.drop_duplicates(subset=['Telefono'])
        df_res = pd.concat([df_res, i_nan])
        df_res = pd.concat([df_res, i_NA])
        df_res = df_res.drop_duplicates(subset=['Nome'])
        df_res['Indirizzo'] = df_res['Indirizzo'].fillna('N/A')
        df_res=df_res.drop(['index'], axis=1)
        print("lunghezza tot", len(df_res))
        writer = pd.ExcelWriter("res/"+path_dest, engine="xlsxwriter")
        df_res.to_excel(writer, sheet_name='Merge')
        writer.save();
    else:
        dataframe=dataframe.drop_duplicates(subset=['Nome','Telefono'])
        dataframe=dataframe.fillna('N/A')
        writer = pd.ExcelWriter("res/"+path_dest, engine="xlsxwriter")
        dataframe.to_excel(writer, sheet_name='Merge')
        writer.save();

def find_estetica(name):
    words=name.split('_')
    if 'e' in words:
        return name;
    else:
        for i in range(len(os.listdir())):
            words=os.listdir()[i].split('.')[0].split('_')
            if 'e' in words:
                words.remove('e')
                nameTmp='_'.join(words)
                if(nameTmp==name):
                    return nameTmp+'_e.xlsx'

if __name__ == '__main__':
    done=[]
    lista=[]
    for i in range (len(os.listdir())):
        estetica=None
        name=os.listdir()[i].split('.')[0].split('-')[0]
        estetica=find_estetica(name)
        ext=None
        try:
            ext=os.listdir()[i].split('.')[1]
        except:
            ext=None
        finally:
            if(ext):
                indone=name.split('.')[0].split("_")[0]
                if (ext == 'xlsx' and (indone not in done) and name!=estetica):
                    lista.append(os.listdir()[i])
                    for j in range(i+1,len(os.listdir())):
                        nameTMP = os.listdir()[j].split('.')[0]
                        if(name.split('-')[0]==nameTMP.split('-')[0]):
                            lista.append(os.listdir()[j])
                    print(lista,estetica)
                    done.append(name)
                    merge(lista,estetica)
                    print("lista",lista," estetica",estetica)
                    print("done",done)
                    lista=[]

            else:
                print("not a file",os.listdir()[i])




