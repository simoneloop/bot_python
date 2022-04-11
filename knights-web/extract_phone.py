import pandas as pd
import numpy as np
import xlsxwriter

file_name=input("ciao, inserisci il nome del file: ")
file_name=file_name.upper()
df=pd.read_excel(file_name+'.xlsx')
lista=np.array(df['Telefono'])
res=[]
for t in lista:
    t = str(t)
    t=t.replace(" ","")
    if (t!='nan' and t!="N/A" and t[0]=='3'):
        res.append(t+";")
for n in res:
    print(n)
print(len(res), " numeri di cellulare trovati")
res=np.array(res)
np.savetxt("cellulari-"+file_name+".txt",res,fmt='%s')