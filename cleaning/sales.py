import pandas as pd

def clean_sale_column(sale_data_column):

    """this function clean all messiness and tidy price data column
    this function takes in a dataframe column and return the cleaned version of the dataframe.
    sale_data_column= the column you want to clean"""

    if pd.api.types.is_numeric_dtype(sale_data_column):
        return (sale_data_column)

    first_clean= sale_data_column.str.replace(',', '')
    cleaned_column= first_clean.str.extract("([\d.,]+)")
    cleaned_column= cleaned_column.astype(float)
    return (cleaned_column)

def missing_sale_column(dataframe, sale_data_column):

    """This function returns the index number and rows that have missing values in the column called in a dataframe.
    It takes in a dataframe and dataframe column that you want to check for missing data
    """

    missing_column= sale_data_column.isna()
    data_set= dataframe[missing_column]
    return data_set