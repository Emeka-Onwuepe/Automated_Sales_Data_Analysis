
from pandas import set_option
from pandas.api.types import is_numeric_dtype
from numpy import nan
from re import search

def clean_identifiers(indentifier):
    indentifier = indentifier.fillna(nan)
    indentifier =  indentifier.astype('str')
    indentifier = indentifier.apply(lambda data:data.strip())
    indentifier = indentifier.replace("nan",nan)
    return indentifier

# The first function: for gender
def clean_genders(gen):
    '''This function returns the issues in the "gender" column of a dataframe while stating the rows where the issues occur. In addition, the function assigns female to gender values "f" and "fmale" while it assigns male to gender value "m". Missing values are not treated as issues. The function works by passing a dataframe and the gender column name into it. E.g. gender_issues(df,"gender") where df is a dataframe and "gender" is the name of the column.'''

    for i in gen:
        try:
            data = gen[i].strip().lower()
            female = ['female', 'f', 'fmale']
            male = ['male', 'm']
            set_option('mode.chained_assignment',None)   
            if search('[0-9@%$/())]',data):
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
            if is_numeric_dtype(sale_column):
                gen[i] = 'unknown gender'
            else:
                 gen[i] = nan
    
    gen = gen.replace("nan",nan)
    return gen

# def name_issues(names):
#     if search('[0-9@%$/())-]',elem)