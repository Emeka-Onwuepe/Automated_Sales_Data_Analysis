#writing a function to convert locations to string
def convert_location(col,df):
    if isinstance(col,str):
        df[col] = df[col]
    else:
        df[col] = df[col].astype(str)

#using the function to convert the locations keys to strings
def verify_location():
    for column in mapper.key():
        if column == 'del_location':
            convert(mapper['del_location'])
            continue
        elif column == 'c_city':
            convert(mapper['c_city'])
            continue
        elif column == 'c_region':
            convert(mapper['c_region'])
            continue
