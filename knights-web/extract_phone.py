import pandas as pd
import numpy as np
path_file=input("inserisci path")
df=pd.read_excel(path_file)
lista=np.array(df['Telefono'])
res=[]
for t in lista:
    t = str(t)
    t=t.replace(" ","")
    if (t!='nan' and t!="N/A" and t[0]=='3'):
        res.append(t)
for n in res:
    print(n)
print(len(res), " numeri di cellulare trovati")