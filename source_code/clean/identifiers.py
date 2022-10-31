import numpy as np
import pandas as pd
import re

def clean_identifiers(indentifier):
    indentifier = indentifier.fillna(np.nan)
    indentifier =  indentifier.astype('str')
    indentifier = indentifier.apply(lambda data:data.strip())
    indentifier = indentifier.replace("nan",np.nan)
    return indentifier

# The first function: for gender
def clean_genders(gen):
    '''This function returns the issues in the "gender" column of a dataframe while stating the rows where the issues occur. In addition, the function assigns female to gender values "f" and "fmale" while it assigns male to gender value "m". Missing values are not treated as issues. The function works by passing a dataframe and the gender column name into it. E.g. gender_issues(df,"gender") where df is a dataframe and "gender" is the name of the column.'''

    for i in range(len(gen)):
        try:
            data = gen[i].strip().lower()
            female = ['female', 'f', 'fmale']
            male = ['male', 'm']
            pd.set_option('mode.chained_assignment',None)   
            if re.search('[0-9@%$/())]',data):
                result.append('not a gender')
            elif data in female:
                gen[i] = 'female'
            elif data in male:
                gen[i] = 'male'
            elif data == 'prefer not to say':
                gen[i] = data
            else:
                gen[i] = 'unknown gender'
        except AttributeError:
            if pd.api.types.is_numeric_dtype(sale_column):
                gen[i] = 'unknown gender'
            else:
                 gen[i] = np.nan
    
    gen = gen.replace("nan",np.nan)
    return gen