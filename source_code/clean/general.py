
from pandas.errors import OutOfBoundsDatetime
from pandas.api.types import is_numeric_dtype
from pandas import DataFrame
from numpy import percentile
from re import search
from source_code.sub_classes import CRITICAL
from .date import clean_date, handle_multiple_sales_date
from .sales import clean_sale_column
from .confirmations import delivery
from .identifiers import clean_age, clean_identifiers,clean_genders


DATA_TYPE_SETTER = {'stock_date':clean_date,'sales_date':clean_date,
               'order_id':clean_identifiers,'p_id':clean_identifiers,'unit_cp':clean_sale_column,
               "discount_per":clean_sale_column,"discount_amount":clean_sale_column,
               'qty_sold':clean_sale_column, "payment_status":clean_identifiers,
               "p_cat":clean_identifiers,"extra_cost":clean_sale_column,
               "extra_cost_pu":clean_sale_column,'sp':clean_sale_column,
               "total_cp":clean_sale_column,"total_sp":clean_sale_column, 
               "sales_grouping":clean_identifiers,'p_name':clean_identifiers,
               'ship_p_code':clean_identifiers,'del_date':clean_date,
               'delivered':delivery,'del_location':clean_identifiers,
                'del_cost':clean_sale_column,'del_charge':clean_sale_column,
                'c_id':clean_identifiers,'c_name':clean_identifiers,
                "c_grouping":clean_identifiers,
                'c_address':clean_identifiers,
                'age':clean_age,'gender':clean_genders,
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
                

    # check for multiple sales date
    try:
        year_only,df,new_mapper,multiple_features = handle_multiple_sales_date(df,
                                                         multiple_features["sales_date"],new_mapper,
                                                         multiple_features)
        error_mgs["year_only"] = year_only
    except KeyError:
        pass
    
 
    return df,new_mapper,multiple_features,error_mgs


def handle_outliers(df,col,col_name,outliers_report):
    Q1 = percentile(col, 25,
                    interpolation = 'midpoint')
    Q3 = percentile(col, 75,
                    interpolation = 'midpoint')
    IQR = Q3 - Q1
    upper = (Q3+1.5*IQR)
    lower = (Q1-1.5*IQR)
    outliers_report["feature_ranges"][col_name] = [lower,upper]
    outliers = df.query("@col > @upper | @col < @lower")

    if outliers.shape[0]:
        outliers_report[col_name] = outliers

    return df,outliers_report

    

def clean_df(df,mapper,multiple_features,handle_outliers=handle_outliers,critical=CRITICAL):
    
    null_report = {"dropped":[],"unknown":[],"mean":[],"ffill":[]}
    outliers_report = {"feature_ranges":{"range":["Min","Max"]}}

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
                    # check for outliers
                    df,outliers_report = handle_outliers(df,df[mapper[multiple_key]],
                                                         mapper[multiple_key],outliers_report)
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
                            null_report["mean"].append(mapper[multiple_key])
                            df[mapper[multiple_key]] = df[mapper[multiple_key]].fillna(int(df[mapper[multiple_key]].mean()))
                    # check for outliers
                    if is_numeric_dtype(df[mapper[multiple_key]]) or df[mapper[multiple_key]].dtype == "datetime64[ns]":
                        df,outliers_report = handle_outliers(df,df[mapper[multiple_key]],
                                                      mapper[multiple_key],outliers_report)

        else:
            # check if a critical feature
            if mapper_key in critical:
                # check for null values
                if df[mapper[mapper_key]].isnull().sum() > 0:
                    null_report["dropped"].append(mapper[mapper_key])
                    df = df[df[mapper[mapper_key]].notna()]
                # check for outliers
                df,outliers_report = handle_outliers(df,df[mapper[mapper_key]],
                                                     mapper[mapper_key],outliers_report)
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
                        null_report["mean"].append(mapper[mapper_key])
                        df[mapper[mapper_key]] = df[mapper[mapper_key]].fillna(int(df[mapper[mapper_key]].mean()))
                # check for outliers
                if is_numeric_dtype(df[mapper[mapper_key]]) or df[mapper[mapper_key]].dtype == "datetime64[ns]":
                    df,outliers_report = handle_outliers(df,df[mapper[mapper_key]],
                                                         mapper[mapper_key],outliers_report)

           
    return df,null_report,outliers_report


def get_null_table(df):
    nulls = df[df.isnull().any(axis=1)]
    null_types = nulls.dtypes
    null_table = DataFrame({ "Features": null_types.index,
                                   "Data Types": null_types,
                                    "Null Values": nulls.isnull().sum()
                                })
    return null_table,nulls
        
   
def rename_cols(df,mapper):
    rename_msg = []
    total_cp = False
    total_sp = False
    try:
        df.rename(columns = {mapper["total_cp"]:"total_cost_price"},inplace=True,error="ignore")
        rename_msg.append(f"We renamed {mapper['total_cp']} to total_cost_price ")
        mapper["total_cp"] = "total_cost_price"
        total_cp = True
    except KeyError:
        pass
    try:
        df.rename(columns = {mapper["total_sp"]:"total_selling_price"},inplace=True,error="ignore")
        rename_msg.append(f"We renamed {mapper['total_sp']} to total_selling_price ")
        mapper["total_sp"] = "total_selling_price"
        total_sp = True
    except KeyError:
        pass
    return df,rename_msg,total_cp,total_sp