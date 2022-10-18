import plotly.express as px

def order_type_quantity(dataframe, quantity, order_type):
    """"
    This function returns product with the quantity of sales
    dataframe = None
    quantity = None
    order_type = None
    
    Parameters
    -----------
    dataframe : The dataframe of the data 
    quantity : str or int or Series or array-like. Either a name of a column in `dataframe`, 
    or a pandas Series or array_like object. it should be related to quantity column
    order_type : str or int or Series or array-like. Either a name of a column in `dataframe`, 
    or a pandas Series or array_like object. it should be related to type of order column
    
    
    """
    quantity= dataframe[quantity]
    order_type= dataframe[order_type]
    subset= quantity.groupby(order_type).sum().sort_values()
    fig = px.bar(x,title= 'TYPE OF ORDER QUANTITY' )
    fig.update_layout(xaxis_title='Order type',  yaxis_title= 'Quantity of Orders')
    print (f'Total quantity of Goods sold: {sum(subset)}')
    print (f'{subset.index.max()} was the mostly sold item with quantity of {subset.max()} which made it {round((subset.max()/sum(subset))*100, 2)}% amount of Goods sold' )
    print (f'{subset.index.min()} was the least sold item with quantity of {subset.min()} which made it {round((subset.min()/sum(subset))*100, 2)}% amount of Goods sold')
    return fig