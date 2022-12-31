from numpy import nan,select

def delivery (status_col):
    status_col =  status_col.astype('str')
    status_col = status_col.apply(lambda data:data.strip().lower())
    conditions_list = [(status_col == '1')|(status_col == 'delivered')|(status_col == 'true')|
                       (status_col == 'serviced') | (status_col == 'yes'),
                       (status_col == '0') |(status_col == 'not delivered') |
                       (status_col == 'false') | (status_col == 'not serviced')|(status_col == 'no')]
    values = ["delivered","undelivered"]
    return select(conditions_list,values,"unidentified")