from pandas.api.types import is_numeric_dtype

def clean_sale_column(sale_data_column):
 
    sale_column = sale_data_column
    if is_numeric_dtype(sale_column):
        return (sale_column)
    cleaned_column = sale_column.astype("str")
    cleaned_column = cleaned_column.str.replace(',', '')
    cleaned_column = cleaned_column.str.extract("([\d.,]+)")
    cleaned_column= cleaned_column.astype(float)
    return (cleaned_column)

