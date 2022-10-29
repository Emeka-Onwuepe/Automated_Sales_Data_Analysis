import pandas as pd

def clean_sale_column(dataframe, sale_data_column):
    """
    This function clean all messiness and tidy price data column.
    This function takes in a dataframe column and return the cleaned version of the dataframe.
    dataframe = None
    sale_data_column= None
    
    Parameters
    -----------
    dataframe : The dataframe of the data 
    sale_data_column : int or Series, object like column. Either a name of a column in `dataframe`, 
    or a pandas Series or array_like object. it should be a sale column
    """
    sale_column= dataframe[sale_data_column]
    if pd.api.types.is_numeric_dtype(sale_column):
        return (sale_column)

    first_clean= sale_column.str.replace(',', '')
    cleaned_column= first_clean.str.extract("([\d.,]+)")
    cleaned_column= cleaned_column.astype(float)
    return (cleaned_column)


def missing_sale_data(dataframe, sale_column):
    """
    This function returns missing rows in sale column
    dataframe = None
    date_column= None
    
    Parameters
    -----------
    dataframe : The dataframe of the data 
    sale_column : int or Series, object like column. Either a name of a column in `dataframe`, 
    or a pandas Series or array_like object. it should be a sale column
    """
    
    data = dataframe[sale_column]
    missing_column= data.isna().sum()
    if missing_column == 0:
        print (f'There is no missing date rows in this dataset')
    else:
        print (f'There are {missing_column} number of missing date rows in this dataset')
        data_set= dataframe[data.isna()]
        return (data_set)