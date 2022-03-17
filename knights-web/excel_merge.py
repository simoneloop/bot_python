import pandas as pd
import numpy as np
import xlsxwriter
import re
import math
# def format_telephone(x):
#     x=x.split('.')
#     x=x[0]
#     if(x[0]!='3' and x[0]!='0' and x!='nan'):
#         prefix='0'+x[:3]
#         rest=x[3:]
#         prefix+=" "
#         return prefix+rest;
#     else:
#         prefix=x[:3]
#         rest=x[3:]
#         prefix+=" "
#         return prefix+rest
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
if __name__ == '__main__':
    path_merge_1=input("inserisci path file estetica\n")
    path_merge_2=input("inserisci path file bot\n")
    path_dest=input("inserisci path dest\n")
    df_e=pd.read_excel(path_merge_1)
    df_b=pd.read_excel(path_merge_2)
    df_res=pd.DataFrame(columns=['Nome', 'Indirizzo', 'Comune', 'Telefono','note','interazioni','risposta'])
    # df_e=df_e.drop(columns=['REGIONE','PROVINCIA','FACEBOOK','INSTAGRAM','NEXT'])
    intersezioni=0
    index=0
    index_rimossi_e=[]
    index_rimossi_b=[]
    for i in range(len(df_e)):

        nome_e = str(df_e.loc[i]['Nome']).strip()
        comune_e=str(df_e.loc[i]['Comune']).strip()
        for j in range(len(df_b)):
            nome_b=str(df_b.loc[j]['Nome']).strip()
            comune_b=str(df_b.loc[j]['Comune']).strip()
            telStrip=str(df_b.loc[j]['Telefono']).replace(" ","")

            df_b.loc[j]['Telefono']=str(telStrip)
            if(nome_e.lower()==nome_b.lower()):
                if(comune_e.lower()==comune_b.lower()):
                    tmp=pd.DataFrame([[nome_b,df_e.loc[i]['Indirizzo'],df_e.loc[i]['Comune'],str(df_e.loc[i]['Telefono']).replace(" ",""),"",df_e.loc[i]['interazioni'],df_e.loc[i]['risposta']]],columns=['Nome', 'Indirizzo', 'Comune', 'Telefono','note','interazioni','risposta'])
                    df_res=df_res.append(tmp)
                    intersezioni+=1
                    index_rimossi_e.append(i)
                    index_rimossi_b.append(j)
    df_e=df_e.drop(index_rimossi_e)
    df_b=df_b.drop(index_rimossi_b)
    print("in comune",intersezioni)
    print("in più nel primo: ",len(df_e))
    print("in più nel secondo: ", len(df_b))
    df_res=pd.concat([df_res,df_e])
    df_res=pd.concat([df_res,df_b])
    df_res['Telefono']=df_res['Telefono'].fillna('N/A')
    df_res['Telefono']=df_res['Telefono'].apply(lambda x:format_telephone(str(x)))
    cond_nan=np.where(df_res['Telefono']=='nan')
    cond_NA = np.where(df_res['Telefono'] == 'N/A')
    i_nan=pd.DataFrame()
    i_NA=pd.DataFrame()
    i_nan=(df_res.iloc[cond_nan])
    i_NA = (df_res.iloc[cond_NA])
    df_res=df_res.drop_duplicates(subset=['Telefono'])
    df_res=pd.concat([df_res,i_nan])
    df_res = pd.concat([df_res, i_NA])
    df_res = df_res.drop_duplicates(subset=['Nome'])
    df_res['Indirizzo'] = df_res['Indirizzo'].fillna('N/A')
    print("lunghezza tot",len(df_res))
    writer = pd.ExcelWriter(path_dest+"merge"+path_merge_1.split("\\")[-1]+path_merge_2.split("\\")[-1], engine="xlsxwriter")
    df_res.to_excel(writer, sheet_name='Merge')
    writer.save();