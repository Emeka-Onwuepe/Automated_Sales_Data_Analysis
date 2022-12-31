from pandas.api.types import is_numeric_dtype
from numpy import nan, select
from re import search

def clean_identifiers(indentifier):
    indentifier = indentifier.fillna(nan)
    indentifier =  indentifier.astype('str')
    indentifier = indentifier.apply(lambda data:data.strip().lower())
    indentifier = indentifier.replace("nan",nan)
    return indentifier

def clean_genders (gender_col):
    gender_col =  gender_col.astype('str')
    gender_col = gender_col.apply(lambda data:data.strip().lower())
    conditions_list = [(gender_col == 'female') | (gender_col == 'f')|
                       (gender_col == 'fmale'), (gender_col == 'male') |
                       (gender_col == 'm'), gender_col == 'prefer not to say']
    values = ["female","male","prefer not to say"]
    return select(conditions_list,values,"unknown gender")

def get_name_issues(names):
    irregular_name = []
    for name in names:
        if search('[0-9@%$/())-]',name):
            irregular_name.append(name)
    
    return irregular_name

def name_issues(df,mapper,multiple_features,get_name_issues):
    name_errors = {}
    try:
        irregular_name = get_name_issues(df[mapper["c_name"]])
        if irregular_name:
            name_errors[mapper["c_name"]] =  irregular_name
        for multiple_key in multiple_features["c_name"]:
            irregular_name = get_name_issues(df[mapper[multiple_key]])
            if irregular_name:
                name_errors[mapper[multiple_key]] = irregular_name 
    except KeyError:
        pass
    return name_errors

def clean_age(age):
     
    sale_column = age
    if is_numeric_dtype(sale_column):
        return sale_column.astype("int")
    cleaned_column = sale_column.astype("str")
    cleaned_column = cleaned_column.str.replace(',', '')
    cleaned_column = cleaned_column.str.extract("([\d]+)")
    cleaned_column= cleaned_column.astype("int")
    return (cleaned_column)