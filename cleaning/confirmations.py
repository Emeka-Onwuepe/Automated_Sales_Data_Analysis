import numpy as np
import pandas as pd
import re

def delivery(df,status):
    '''This function returns the "delivery" column issues of a dataframe while stating the rows where the issues occur. It works by taking in a dataframe and the delivery column name. E.g. delivery(df,"delivery_status").'''
    delivered = ['1','delivered','true','serviced','yes']
    not_delivered = ['0','not delivered','false','not serviced','no']
    row = []
    issue = []
    df[status] = df[status].astype(str)
    pd.set_option('mode.chained_assignment',None) 
    for i in range(len(df[status])):
        if df[status][i].lower() in delivered:
            df[status][i] = True
        elif df[status][i].lower() in not_delivered:
            df[status][i] = False
        elif df[status][i] == 'nan':
            df[status][i] = np.nan
        else:
            row.append(i)
            issue.append('unidentified delivery status')
    unidentified = pd.DataFrame({'row':row,'issue':issue})
    return unidentified.set_index('row')
