from pandas import to_datetime

def clean_date(column):
    if column.dtypes == 'datetime64[ns]':
        return column
    else:
        if column.dtypes == "float":
            column = column.astype("int")

        column = column.astype("str")
        column = column.apply(lambda data:data.strip())
        date_transformed = to_datetime(column,infer_datetime_format=True)
        return date_transformed
        
def handle_multiple_sales_date(df,multiple_key,new_mapper,multiple_features):
    year_only = []
    print("new mapper",new_mapper)
    print("multiple_features",multiple_features)
    multiple_key.append("sales_date")
    print("multiple_features",multiple_features)
    months,day = None,None
    for mapper_key in multiple_key:
        try:
            months = df[new_mapper[mapper_key]].dt.month.nunique() 
            day = df[new_mapper[mapper_key]].dt.day.nunique() 
        except KeyError:
            pass
        if months and day:
            if months < 2 and day < 2:
                print("seen just year")
                df.drop(new_mapper[mapper_key],axis=1)
                year_only.append(new_mapper[mapper_key])
                del new_mapper[mapper_key]
                idx = multiple_features['sales_date'].index(mapper_key)
                if idx > -1:
                    multiple_features['sales_date'].pop(idx)
            elif months > 1 and day  > 1:
                print("seen more than one unique")
                
                idx = multiple_features['sales_date'].index(mapper_key)
                if idx > -1:
                    multiple_features['sales_date'].pop(idx)
                new_mapper["sales_date"] = new_mapper[mapper_key]
                del new_mapper[mapper_key]
            
    return year_only,df,new_mapper,multiple_features         