import json

with open('simoneset.txt', 'r') as file:
    lines = file.readlines()

res=[]
r={}
for i in range(len(lines)):
  row=lines[i].split(":")
  
  if(len(row)>1):
    if(i%2==0):
        r['prompt']=row[1].replace('\n','')
    else:
        r['completion']=row[1].replace('\n','')
        res.append(r)
        r={}

with open("dataset.jsonl", "w") as fp:
    json.dump(res,fp) 
  