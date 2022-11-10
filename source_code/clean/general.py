from pandas.errors import OutOfBoundsDatetime
from pandas.api.types import is_numeric_dtype
from re import search
from source_code.sub_classes import CRITICAL
from .date import clean_date
from .sales import clean_sale_column
from .confirmations import delivery
from .identifiers import clean_identifiers,clean_genders


DATA_TYPE_SETTER = {'stock_date':clean_date,'sales_date':clean_date,
               'order_id':clean_identifiers,'p_id':clean_identifiers,'unit_cp':clean_sale_column,
               "discount_per":clean_sale_column,"discount_amount":clean_sale_column,
               'qty_sold':clean_sale_column, "payment_status":clean_identifiers,
               "p_cat":clean_identifiers,"pro_cost":clean_sale_column,
               'sp':clean_sale_column, 'sp_dis':clean_sale_column,
               "sales_grouping":clean_identifiers,'p_name':clean_identifiers,
               'ship_p_code':clean_identifiers,'del_date':clean_date,
               'delivered':delivery,'del_location':clean_identifiers,
                'del_cost':clean_sale_column,'del_charge':clean_sale_column,
                'c_id':clean_identifiers,'c_name':clean_identifiers,
                "c_grouping":clean_identifiers,
                'c_city':clean_identifiers,'c_region':clean_identifiers,
                'gender':clean_genders,
               }

def create_mapper(data):
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

    return mapper

def set_data_types(df,mapper,set_data_data):
    multiple_features = {}
    error_mgs = {"out_of_bound":[]}
    new_mapper = mapper.copy()
    for mapper_key in mapper.keys():
        sub_class = None
        if search('&#&\d',mapper_key):
            sub_class,__ = mapper_key.split('&#&')
        
            try:
                multiple_features[sub_class]
                multiple_features[sub_class].append(mapper_key)
            except KeyError:
                multiple_features[sub_class] = [mapper_key]
           
        try:
                
            data_key = sub_class if sub_class else mapper_key
            df[mapper[mapper_key]] = set_data_data[data_key](df[mapper[mapper_key]])
        except OutOfBoundsDatetime:
            error_mgs["out_of_bound"].append(mapper[mapper_key])
            df.drop(mapper[mapper_key],axis=1,inplace=True)
            del new_mapper[mapper_key]
            if search('&#&\d',mapper_key):
                sub_class,__ = mapper_key.split('&#&')
                idx = multiple_features[sub_class].index(mapper_key)
                multiple_features[sub_class].pop(idx)
    return df,new_mapper,multiple_features,error_mgs
    

def clean_null(df,mapper,multiple_features,critical=CRITICAL):
    
    null_report = {"dropped":[],"unknown":[],"zeros":[],"ffill":[]}

    for mapper_key in mapper.keys():
        # check if the key is multiple
        if search('&#&\d',mapper_key):
            sub_class,__ = mapper_key.split('&#&')
            # check if a critical feature
            if sub_class in critical:
                for multiple_key in multiple_features[sub_class]:
                    # check for null values
                    if df[mapper[multiple_key]].isnull().sum() > 0:
                        # drop null values
                        null_report["dropped"].append(mapper[multiple_key])
                        df = df[df[mapper[multiple_key]].notna()] 
            else:
                for multiple_key in multiple_features[sub_class]:
                    # check for null values
                    if df[mapper[multiple_key]].isnull().sum() > 0:
                        # check if an object
                        if df[mapper[multiple_key]].dtype == "object":
                            null_report["unknown"].append(mapper[multiple_key])
                            df[mapper[multiple_key]] = df[mapper[multiple_key]].fillna("unknown") 
                        elif df[mapper[multiple_key]].dtype == "datetime64[ns]":
                            null_report["ffill"].append(mapper[multiple_key])
                            df[mapper[multiple_key]] = df[mapper[multiple_key]].fillna(method = "ffill")
                        elif is_numeric_dtype(df[mapper[multiple_key]]):
                            null_report["zeros"].append(mapper[multiple_key])
                            df[mapper[multiple_key]] = df[mapper[multiple_key]].fillna(0)

        else:
            # check if a critical feature
            if mapper_key in critical:
                # check for null values
                if df[mapper[mapper_key]].isnull().sum() > 0:
                    null_report["dropped"].append(mapper[mapper_key])
                    df = df[df[mapper[mapper_key]].notna()]
            else:
                # check for null values
                if df[mapper[mapper_key]].isnull().sum() > 0:
                    # check if an object
                    if df[mapper[mapper_key]].dtype == "object":
                        null_report["unknown"].append(mapper[mapper_key])
                        df[mapper[mapper_key]] = df[mapper[mapper_key]].fillna("unknown") 
                    elif df[mapper[mapper_key]].dtype == "datetime64[ns]":
                        null_report["ffill"].append(mapper[mapper_key])
                        df[mapper[mapper_key]] = df[mapper[mapper_key]].fillna(method = "ffill")
                    elif is_numeric_dtype(df[mapper[mapper_key]]):
                        null_report["zeros"].append(mapper[mapper_key])
                        df[mapper[mapper_key]] = df[mapper[mapper_key]].fillna(0)

            
    return df,null_report
   

# # Importing
# import sklearn
# from sklearn.datasets import load_boston
# import pandas as pd
# import numpy as np

# # Load the dataset
# bos_hou = load_boston()

# # Create the dataframe
# column_name = bos_hou.feature_names
# df_boston = pd.DataFrame(bos_hou.data)
# df_boston.columns = column_name
# df_boston.head()

# ''' Detection '''
# # IQR
# Q1 = np.percentile(df_boston['DIS'], 25,
# 				interpolation = 'midpoint')

# Q3 = np.percentile(df_boston['DIS'], 75,
# 				interpolation = 'midpoint')
# IQR = Q3 - Q1

# print("Old Shape: ", df_boston.shape)

# # Upper bound
# upper = np.where(df_boston['DIS'] >= (Q3+1.5*IQR))
# # Lower bound
# lower = np.where(df_boston['DIS'] <= (Q1-1.5*IQR))

# ''' Removing the Outliers '''
# df_boston.drop(upper[0], inplace = True)
# df_boston.drop(lower[0], inplace = True)

# print("New Shape: ", df_boston.shape)
