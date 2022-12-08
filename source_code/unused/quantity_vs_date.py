#!/usr/bin/env python
# coding: utf-8

# In[ ]:
          

import plotly.express as px

def date_quantity(dataframe, date, quantity):
    """"
    This function returns product with the mean of profit 
    dataframe = None
    quantity = None
    profit = None
    
    Parameters
    -----------
    dataframe : The dataframe of the data 
    quantity : str or int or Series or array-like. Either a name of a column in `dataframe`, 
    or a pandas Series or array_like object. it should be related to quantity column
    date : str or int or Series or array-like. Either a name of a column in `dataframe`, 
    or a pandas Series or array_like object. it should be related to date column
    
    
    """
    date= dataframe[date]
    quantity= dataframe[quantity]
    subset= quantity.groupby(date).sum().sort_values()
    fig= px.line(subset, title= 'Quantity of orders in relation to time')
    fig.update_layout(xaxis_title='Date',  yaxis_title= 'Orders Quantity')
    print (f'Top five dates with high sale and quantity of goods sold includes:\n{subset.tail(5).to_frame()}')
    print (f'Top five dates with the low sale and quantity of goods sold includes: \n{subset.head(5).to_frame()}')
    return fig

