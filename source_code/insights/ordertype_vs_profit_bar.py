import plotly.express as px

def order_type_profit(dataframe, order_type, profit):
    """"
    This function returns product with the mean of profit 
    dataframe = None
    quantity = None
    profit = None
    
    Parameters
    -----------
    dataframe : The dataframe of the data 
    order_type : str or int or Series or array-like. Either a name of a column in `dataframe`, 
    or a pandas Series or array_like object. it should be related to type of order column
    profit : str or int or Series or array-like. Either a name of a column in `dataframe`, 
    or a pandas Series or array_like object. it should be related to profit
    
    
    """
    order_type= dataframe[order_type]
    profit= dataframe[profit]
    subset= profit.groupby(order_type).sum().sort_values()
    fig = px.bar(x,title= 'TYPE OF ORDER VS PROFIT MADE' )
    fig.update_layout(xaxis_title='Order type',  yaxis_title= 'Profit of Orders')
    print (f' Total Profit of all Goods sold: {sum(subset)}')
    print (f' The product with the highest profit is: {subset.index.max()}, it generated {round((subset.max()/sum(subset))*100, 2)}% profit for the company')
    print (f' The product with the highest profit is: {subset.index.min()}, it generated {round((subset.min()/sum(subset))*100, 2)}%  profit for the company')
    return fig