import numpy as np
import pandas as pd
import re

def delivery(status):
    '''This function returns the "delivery" column issues of a dataframe while stating the rows where the issues occur. It works by taking in a dataframe and the delivery column name. E.g. delivery(df,"delivery_status").'''
    delivered = ['1','delivered','true','serviced','yes']
    not_delivered = ['0','not delivered','false','not serviced','no']
    status = status.astype(str)
    status = status.apply(lambda data:data.strip())
    pd.set_option('mode.chained_assignment',None) 
    for i in range(len(status)):
        if status[i].lower() in delivered:
            status[i] = "delivered"
        elif status[i].lower() in not_delivered:
            status[i] = "undelivered"
        elif status[i] == 'nan':
            status[i] = np.nan
        else:
            status[i] = "unidentified"
  
    return status
