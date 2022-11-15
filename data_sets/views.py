from django.shortcuts import render
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from django.core.files import File
import json
import pandas as pd
from pathlib import Path
from django.conf import settings
from os import path,listdir,makedirs
from zipfile import ZipFile
from data_sets.forms import UploadZipFileForm
from data_sets.models import Dataset
from source_code.clean.converter import convert_to_excel
from source_code.clean.general import DATA_TYPE_SETTER, clean_df, create_mapper, set_data_types
from source_code.clean.identifiers import name_issues,get_name_issues
from source_code.sub_classes import SUB_CLASSES
from source_code.read_file import read_dataset


files_location = path.join(".", 'datasets')

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
        feature = feature.replace("/","_").replace("\\","_")
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
        df,null_report,outliers_report = clean_df(df,mapper,multiple_features)
        name_errors = name_issues(df,mapper,multiple_features,get_name_issues)
        
       
        dataset_location = path.join(files_location,dataset_id)
        zip_name = f'{dataset_id}.zip'
        zip_location = path.join(files_location,zip_name)
        if not path.exists(files_location):
            makedirs(files_location)
        if not path.exists(dataset_location):
            makedirs(dataset_location)
            
        convert_to_excel(df,dataset_location,"clean_data")
        convert_to_excel(nulls,dataset_location,"null_values")
        for key,value in outliers_report.items():
            convert_to_excel(pd.DataFrame(value),dataset_location,f'{key}_outliers')
        
       
    
        with ZipFile(zip_location,'w') as zipfile:
            files= listdir(dataset_location)
            for file in files:
                zipfile.write(path.join(dataset_location,file))
        
        path_zip = Path(zip_location)    
        with path_zip.open(mode='rb') as f:
            dataset.zipfolder = File(f,name=path_zip.name)  
            dataset.save() 
        print(null_report)
        
    return render(request,"data_sets/dashboard.html",{"head":df.head().to_html(), 
                                                        "feature_ranges":outliers_report['feature_ranges'],
                                                        "name_errors":name_errors,
                                                        "error":error_mgs,
                                                        "nulls":nulls,
                                                        'null_report':null_report,
                                                        'df':df})