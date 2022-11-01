from django.shortcuts import render
import json
import pandas as pd
import re
from data_sets.models import Dataset
from source_code.clean.general import DATA_CLEANING
from source_code.sub_classes import SUB_CLASSES
from source_code.read_file import read_dataset

# Create your views here.
def ClassifyView(request,user_id,dataset_id):
    df,dataset = read_dataset(Dataset,user_id,dataset_id,pd)
    column = df.columns
    new_col = []
    for feature in column:
        # convert to lowercase 
        try:
            feature = feature.strip().lower()
        except AttributeError:
            feature = str(feature)
        feature = feature.replace("-","_").replace(" ","_")
        new_col.append(feature)
    dataset.columns = json.dumps(new_col)
    dataset.save()
    return render(request,'data_sets/classify.html',{"column":new_col,"sub_classes":SUB_CLASSES,
                                                    "user_id":user_id,"dataset_id":dataset_id})

def AnalysisView(request,user_id,dataset_id):
    if request.method == "POST":
        data = dict(request.POST)
        del data['csrfmiddlewaretoken']
        mapper = {}
        count = 0
        for key,value in data.items():
            count+=1
            value = value[0]
            try:
                mapper[value]
                value = f"{value}&#&{count}"
                if value != "none":
                    mapper[value] = key
            except KeyError:
                if value != "none":
                    mapper[value] = key

        df,dataset = read_dataset(Dataset,user_id,dataset_id,pd)
        df.columns = json.loads(dataset.columns)
        df = df[mapper.values()]
        
        multiple_features = {}
        error_mgs = {"out_of_bound":[]}
        for mapper_key in mapper.keys():
            sub_class = None
            if re.search('&#&\d',mapper_key):
                sub_class,num = mapper_key.split('&#&')
        
                try:
                    multiple_features[sub_class]
                    multiple_features[sub_class].append(mapper_key)
                except KeyError:
                    multiple_features[sub_class] = [sub_class,mapper_key]
           
            try:
                
                data_key = sub_class if sub_class else mapper_key
                df[mapper[mapper_key]] = DATA_CLEANING[data_key](df[mapper[mapper_key]])
            except pd.errors.OutOfBoundsDatetime:
                error_mgs["out_of_bound"].append(mapper[mapper_key])
                df.drop(mapper[mapper_key],axis=1,inplace=True)
                 
        
    return render(request,"data_sets/dashboard.html",{"df":df.head().to_html(), 
                  "error":error_mgs})
