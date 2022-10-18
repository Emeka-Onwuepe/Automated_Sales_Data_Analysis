import numpy as np
import pandas as pd
import re

# The first function: for gender
def gender_issues(df,gen):
    '''This function returns the issues in the "gender" column of a dataframe while stating the rows where the issues occur. In addition, the function assigns female to gender values "f" and "fmale" while it assigns male to gender value "m". Missing values are not treated as issues. The function works by passing a dataframe and the gender column name into it. E.g. gender_issues(df,"gender") where df is a dataframe and "gender" is the name of the column.'''
    data = None
    index = []
    result = []
    for i in range(len(df[gen])):
        try:
            data = df[gen][i].strip().lower()
            female = ['female', 'f', 'fmale']
            male = ['male', 'm']
            pd.set_option('mode.chained_assignment',None)   
            if re.search('[0-9@%$/())]',data):
                index.append(i)
                result.append('not a gender')
            elif data in female:
                df[gen][i] = 'female'
            elif data in male:
                df[gen][i] = 'male'
            elif data == 'prefer not to say':
                df[gen][i] = data
            else:
                index.append(i)
                result.append('unknown gender')
        except AttributeError:
            if np.isnan(df[gen][i]) == False:
                index.append(i)
                result.append('not a gender')
    issues = pd.DataFrame({'row':index, 'issue':result})
    if len(issues) == 0:
        return None
    else:
        return issues.set_index('row')

# The second function: for names
def name_issues(df,names):
    '''This function returns the "name" column issues of a dataframe while stating the rows where the issues occur. The function works by passing a dataframe and the name column into it. E.g. name_issues(df,"product_names").'''
    row = []
    result = []
    elem = None
    #please note that this is
    #not an efficient code
    #due to running time
    for i in range(len(df[names])):
        try:
            elem = df[names][i].strip()
            if re.search('[0-9@%$/())-]',elem):
                row.append(i)
                result.append('unexpected')
        except AttributeError:
            if np.isnan(df[names][i]) == False:
                row.append(i)
                result.append('numeric')
                
    issues = pd.DataFrame({'row':row, 'issue':result})
    if len(issues) == 0:
        return None
    else:
        return issues.set_index('row')

# The third function: for ids
def clean_ids(df, ids):
    '''This function converts an "ID" column to string while retaining null values as null values. It works by taking in a dataframe and the column name of the id. E.g. clean_ids(df,"user_id").'''
    df[ids] =  df[ids].astype('str')
    for i in range(len(df[ids])):
        if df[ids][i] in ['nan','None']:
            df[ids][i] = np.nan
    return None