from django.shortcuts import render,reverse
from django.http import HttpResponseRedirect
from django.core.files import File
import json
import pandas as pd
from pathlib import Path
from os import path,makedirs,remove
from shutil import rmtree,make_archive
from datetime import timedelta
from django.utils import timezone
from data_sets.models import Dataset
from source_code.converter import  convert_to_excel
from source_code.clean.general import (DATA_TYPE_SETTER, clean_df, create_mapper, 
                                       get_null_table, set_data_types,handle_outliers)
from source_code.clean.identifiers import name_issues,get_name_issues
from source_code.report import create_report_pdf
from source_code.sub_classes import SUB_CLASSES, SUB_CLASSES_EXP
from source_code.read_file import read_dataset
from source_code.cleaning_report import create_cleaning_pdf
from source_code.clean.sales import cal_profit


files_location = path.join(".", 'datasets')

# Create your views here.
def ClassifyView(request,dataset_id):
    
    user_id = None
    try:
        user_id = request.session["user_id"]
    except KeyError:
       return HttpResponseRedirect(reverse('frontview:homeView'))
  
    
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
                                                    "dataset_id":dataset_id,'table_data':SUB_CLASSES_EXP})

def AnalysisView(request,dataset_id):
    
    user_id = None
    try:
        user_id = request.session["user_id"]
    except KeyError:
       return HttpResponseRedirect(reverse('frontview:homeView'))
    
    
    if request.method == "POST":
        data = dict(request.POST)
        del data['csrfmiddlewaretoken']

        mapper = create_mapper(data)
        df,dataset = read_dataset(Dataset,user_id,dataset_id,pd)
        df.columns = json.loads(dataset.columns)
        # select needed columns
        df = df[mapper.values()]
        shape = df.shape
        df,mapper,multiple_features,error_mgs = set_data_types(df,mapper,DATA_TYPE_SETTER)
        
        null_table,affected_nulls = get_null_table(df)
        df,null_report,outliers_report = clean_df(df,mapper,multiple_features)
        df,derivatives,new_cols = cal_profit(df,mapper,multiple_features)
        for col in new_cols:
            df,outliers_report = handle_outliers(df,df[col],col,outliers_report)
        name_errors = name_issues(df,mapper,multiple_features,get_name_issues)
        
        num_ranges = pd.DataFrame(outliers_report["feature_ranges"],index=["Lower Bound","Upper Bound"])
        
        null_table_cleaned,_ = get_null_table(df)
        
        dataset_location = path.join(files_location,dataset_id)
        excels_location =  path.join(dataset_location,'excels')
        pngs_location =  path.join(dataset_location,'pngs')
        zip_name = f'{dataset_id}.zip'
        zip_location = path.join(files_location,zip_name)
        zip_folder = path.join(files_location,dataset_id)
        if not path.exists(files_location):
            makedirs(files_location)
        if not path.exists(dataset_location):
            makedirs(dataset_location)
            makedirs(excels_location)
            makedirs(pngs_location)

            
        create_cleaning_pdf(df,error_mgs,null_report,num_ranges,null_table,
                            null_table_cleaned,name_errors,dataset_location,
                            derivatives,shape
                            )
        
        create_report_pdf(df,dataset.report_title,dataset_location,
                          pngs_location,excels_location,mapper,multiple_features)       
        
        convert_to_excel(df,dataset_location,"clean_data")
        convert_to_excel(affected_nulls,excels_location,"null_values")
        for key,value in outliers_report.items():
            convert_to_excel(pd.DataFrame(value),excels_location,f'{key}_outliers')
         
        summary_sat = df.describe().reset_index()
        summary_sat.rename({"index":"statistics"},axis=1,inplace=True)
        
        convert_to_excel(summary_sat,excels_location,'statistical_summary')
        
        
        make_archive(zip_folder,'zip',dataset_location)
        
        path_zip = Path(zip_location)    
        with path_zip.open(mode='rb') as f:
            dataset.zipfolder = File(f,name=path_zip.name)  
            dataset.save() 
            
        if path.exists(files_location):
            rmtree(path.join(dataset_location))
            remove(zip_location)
                 
    return HttpResponseRedirect(reverse('process:dashboardView'))


    
def dashboardView(request):
    
    user_id = None
    try:
        user_id = request.session["user_id"]
    except KeyError:
        if request.method != "POST":
            return HttpResponseRedirect(reverse('frontview:homeView'))
    
    if request.method == "POST" or user_id:
        time_out = timezone.now() - timedelta(hours=3)
        old_data = Dataset.objects.filter( created__lte = time_out)
        old_data.delete()
          
        datasets = Dataset.objects.filter(user_id__user_id = user_id)
        return render(request,'data_sets/dashboard.html',{"dataset":datasets})
        
def deleteView(request,dataset_id):
    
    try:
        dataset = Dataset.objects.get(id=dataset_id)
        dataset.delete()
    except Dataset.DoesNotExist:
        pass
    
    return HttpResponseRedirect(reverse('process:dashboardView'))
    
      