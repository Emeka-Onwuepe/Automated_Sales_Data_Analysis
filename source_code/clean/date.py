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
        