from functools import _make_key
from django.shortcuts import render
import json
import pandas as pd
import re
from data_sets.models import Dataset
from source_code.clean.general import DATA_TYPE_SETTER, clean_null, create_mapper, set_data_types
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

        mapper = create_mapper(data)
        df,dataset = read_dataset(Dataset,user_id,dataset_id,pd)
        df.columns = json.loads(dataset.columns)
        df = df[mapper.values()]
        
        df,mapper,multiple_features,error_mgs = set_data_types(df,mapper,DATA_TYPE_SETTER)
        nulls = df[df.isnull().any(axis=1)]
        df,null_report = clean_null(df,mapper,multiple_features)       

                  
        
    return render(request,"data_sets/dashboard.html",{"head":df.head().to_html(), 
                                                      "nulls": nulls.to_html(),
                                                        # "types": df.dtypes,
                                                        # "types": df.dtypes,
                                                        "error":error_mgs,'df':df})