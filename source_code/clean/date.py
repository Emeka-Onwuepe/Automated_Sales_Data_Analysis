import pandas as pd

def clean_date(column):
    if column.dtypes == 'datetime64[ns]':
        return column
    else:
        if column.dtypes == "float":
            column = column.astype("int")

        column = column.astype("str")
        column = column.apply(lambda data:data.strip())
        date_transformed = pd.to_datetime(column,infer_datetime_format=True)
        return date_transformed
        
    
# def clean_date_outliers(dataframe, date_column):
#     """
#     This function remove outliers from date column, it converts date column to datetime
#     dataframe = None
#     date_column= None
    
#     Parameters
#     -----------
#     dataframe : The dataframe of the data 
#     date_column : int or Series, object like column. Either a name of a column in `dataframe`, 
#     or a pandas Series or array_like object. it should be a date column
#     """
    
#     date = clean_date(dataframe, date_column)
#     quant1, quant2= date.quantile([0.01,0.99])
#     new_date= date[date.between(quant1, quant2)]
#     print (f'Dates that are older than {quant1} has been removed from your date set as we believe they are outliers')
#     print (f'Dates that are later than {quant2}  has been removed from your date set as we believe they are outliers')
#     return (new_date)

# def missing_data(dataframe, date_column):
#     """
#     This function returns missing rows in date column
#     dataframe = None
#     date_column= None
    
#     Parameters
#     -----------
#     dataframe : The dataframe of the data 
#     date_column : int or Series, object like column. Either a name of a column in `dataframe`, 
#     or a pandas Series or array_like object. it should be a date column
#     """
    
#     date = dataframe[date_column]
#     missing_column= date.isna().sum()
#     if missing_column == 0:
#         print (f'There is no missing date rows in this dataset')
#     else:
#         print (f'There are {missing_column} number of missing date rows in this dataset')
#         data_set= dataframe[date.isna()]
#         return (data_set)