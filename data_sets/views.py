from django.shortcuts import render
from data_sets.models import Dataset
import pandas as pd
from source_code.statics import SUB_CLASSES

# Create your views here.
def ClassifyView(request,user_id,dataset_id):
    df = None
    try:
        data= Dataset.objects.get(user_id__user_id = user_id,dataset_id = dataset_id)
        _,file_extension = str(data.dataset).split(".")
        # load data
        if file_extension == 'xlsx':
            df = pd.read_excel(data.dataset)
        else:
            # remember to check for possibles errors
            #/t seperator and other non coma seperatorsS
            df = pd.read_csv(data.dataset)
    except Dataset.DoesNotExist:
        pass
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
    return render(request,'data_sets/classify.html',{"column":new_col,"sub_classes":SUB_CLASSES})