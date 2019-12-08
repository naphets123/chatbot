#create Manufacturer and model lists
import pandas as pd
import numpy as np 
import json

table = pd.read_csv("truck_table.csv")

Brand_list = [i.split(" ") for i in table.Manufacturer.unique()]

def list_flatten(brand_list):
    total_list = []
    for i in brand_list:
        if len(i)>1:
            for j in i:
                 total_list.append(j)
        else:
            total_list.append(i[0])
    return total_list
Brand_list = list_flatten(Brand_list)
Brand_list = [i for i in Brand_list if i not in ("Trucks","Truck", "Commercial", "Vehicles","Industries")]
#Prepare dictionary for models
Brand_models = dict((e,[]) for e in Brand_list)

for e in table.Model.unique():
    for j in Brand_list:
        if j in e:
            model = e.replace(j,'').strip()
            Brand_models[j].append(model)

#Prevent any duplicates
for k in Brand_models.keys():
    Brand_models[k] = list(dict.fromkeys(Brand_models[k]))

Brand_models.update({"Daimler":Brand_models["Mercedes-Benz"][:]})

#Prevent empty elements
Brand_models = {key:val for key, val in Brand_models.items() if val != []}
with open('trucks.json','w') as f:
    json.dump(Brand_models,f)

