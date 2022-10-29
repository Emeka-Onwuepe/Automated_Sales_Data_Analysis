#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import seaborn as sns
import matplotlib.pyplot as plt

def correlation(dataframe, first_column, second_column):
    """"
    This function returns product with the quantity of sales
    dataframe = None
    first_column = None
    second_column = None
    
    Parameters
    -----------
    dataframe : The dataframe of the data 
    quantity : int or Series or array-like. Either a name of a column in `dataframe`, 
    or a pandas Series or array_like object. it should be an integer column
    order_type : int or Series or array-like. Either a name of a column in `dataframe`, 
    or a pandas Series or array_like object. it should be an integer column
    
    
    """
    first_columns= dataframe[first_column]
    second_columns= dataframe[second_column]

    if first_columns.dtypes == object or second_columns.dtypes == object :
        
        print (f'This plot can only work for numeric columns; your {first_column} column is {first_columns.dtypes} data type and {second_column} column is {second_columns.dtypes} data type')
        
    else:
        corr= first_columns.corr(second_columns)
        sns.heatmap(dataframe[[first_column, second_column]].corr())
        plt.title(f'Correlation relationship between {first_column} and {second_column}')
        print (f'correlation of {first_column} and {second_column} is: {round(corr,3)}')
        if corr >= 0.5:
                print (f'These columns have strong positive correlation with each other, that is as {first_column} increasin {second_column} is also increasing')
                
        elif corr < 0.5 and corr > 0.1:
            print (f'These columns have weak positive correlation with each other, that is as {first_column} increasing, {second_column} is also increasing')
            
        elif corr <= -0.5:
            print (f'These columns have strong negative correlation with each other, that is as {first_column} increasing, {second_column} is decreasing')
            
        elif corr > -0.5 and corr < -0.1:
            print (f'These columns have strong negative correlation with each other, that is as {first_column} increasing, {second_column} is decreasing')
        
        elif corr == 0:
            print (f'These columns have no correlation with each other')
    

