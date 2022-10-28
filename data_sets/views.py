from django.shortcuts import render
import json
import pandas as pd
from data_sets.models import Dataset
from source_code.statics import SUB_CLASSES
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
                value = f"{value}_{count}"
                if value != "none":
                    mapper[value] = key
            except KeyError:
                if value != "none":
                    mapper[value] = key

        df,dataset = read_dataset(Dataset,user_id,dataset_id,pd)
        df.columns = json.loads(dataset.columns)
        df = df[mapper.values()]

    return render(request,"data_sets/dashboard.html",{"mapper":mapper,"df":df.head()})