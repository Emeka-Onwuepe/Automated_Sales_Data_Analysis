import numpy as np
import pandas as pd
import re

def date_columns(df):
    """This function checks all the columns in a dataframe and returns the name of the date column(s) whose entries take the form dd-mm-yy"""
    for column_name in df.columns:
        if df[column_name][0] in re.findall(r'\d{1,2}/\d{1,2}/\d{2,4}',df[column_name][0]):
            return column_name
    
