from source_code.sub_classes import CRITICAL
from .date import clean_date
from .sales import clean_sale_column
from .confirmations import delivery
from .identifiers import clean_identifiers,clean_genders


DATA_CLEANING = {'stock_date':clean_date,'sales_date':clean_date,
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

def clean_data(df,mapper,multiple_features, critical=CRITICAL):
    null_columns =  df.isnull().sum().index
    mapper_values = mapper.values()
    keys = list(mapper.keys())
    
    null_keys = []
    for index,value in enumerate(mapper_values):
        if value in null_columns:
            null_keys.append(keys[index])
    
    # drop critical null values
    for key in critical:
        if key in null_keys:
            df = df[df[mapper[key]].notna()]
            try:
                for multiple_key in multiple_features[key]:
                    df = df[df[mapper[multiple_key]].notna()]  
            except KeyError:
                pass

    return df
            
    