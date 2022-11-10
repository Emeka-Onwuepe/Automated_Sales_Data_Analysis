import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def Pie(df, x, y, title):
    """
    This function plot a pie chart.

    Parameters
    ---------------
    df: this is the dataframe or a table-like arrays.
    x: is the numerical values used in plotting the chart. A 1D array-like i.e.the wedge sizes.
    y: is the labels for each of the sectors in the pie chart
    title: as the name implies, is the title of the chart.
    """
    
    plt.figure(figsize=(12,8))
    chart = plt.pie(data=df, x=x, labels=y, counterclock=True, startangle=90, wedgeprops={'width':0.6}, colors=sns.color_palette('dark'))
    plt.title(title);
    chart

def Bar(df, x, y, xlab, ylab, title):
    """
    This function plot a bar chart.

    Parameters
    ---------------
    df: this is the dataframe or a table-like arrays.
    x: float or array-like. The x coordinates of the bars.
    y: float or array-like. The height(s) of the bars.
    xlab: this is the label for the x-axis of the chart
    ylab: this is the label for the y-axis of the chart
    """
    
    plt.figure(figsize=(12,8))
    chart = plt.bar(data=df, x=x, height=y, color=sns.color_palette('dark')[0])
    plt.title(title)
    plt.xlabel(xlab)
    plt.ylabel(ylab)
    chart

def gainLoss(df, ucp, qty_sold, sp):
    """
    This function determines whether a sale yield profit or loss.
    
    Parameters
    ---------------
    df: this is the dataframe or a table-like arrays.
    ucp: a panda series referring to the unit cost price.
    qty_sold: a panda series referring to the quantity of goods sold.
    sp: a panda series referring to the selling price.
    """
    
    try:
        if (df[sp].dtype in('int64', 'int32', 'float')) & (df[sp].dtype in('int64', 'int32', 'float')) & (df[sp].dtype in('int64', 'int32', 'float')):
            df['profit_loss'] = df[sp] - df[ucp]*df[qty_sold]
            df['gain_lost'] = df['profit_loss'].apply(lambda x: 'loss' if x<0 else ('gain' if x>0  else 'neutral'))
        else:
            print('At least one of the columns specified is not a numeric data type')
    except KeyError:
        print('One of the columns specified is not spelt correctly. Kindly, check the spelling and the case of the column(s) name.')        
        

def topCustomers(df, cust, sp, top):
    """
    This function compute customers with highest purchase based on the rank (top) specified.
    
    Parameters
    ---------------
    df: this is the dataframe or a table-like arrays.
    cust: a panda series referring to the customer's names.
    sp: a panda series referring to the selling price.
    top: an int specifying the rank order of customers.
    """
    
    if (df[sp].dtype not in('float', 'int64', 'int32', 'object')):
        print(sp, 'is not a numeric data')
    else:
        title = '\n\nTop '+ str(top) +' Purchasing Customers'
        new = df.groupby(cust)[sp].sum().sort_values(ascending=False)[0:top]
        print(new)
        Pie(new, new.values, new.index, str.upper(title))
        print('\n\nThis chart shows that ', new.index[0], 'is the highest purchasing customer.')

def Sales_by_day(df, pdate, sp):
    """
    This function evaluates sales by day of the week.
    
    Parameters
    ---------------
    df: this is the dataframe or a table-like arrays.
    pdate: a panda series referring to the purchase date which is expected to be a datetime data type.
    sp: a panda series referring to the selling price.
    """
    from datetime import datetime as dt
    try:
        if df[pdate].isna().count()==0:
            df['p_dow'] = df[pdate].apply(lambda x: dt.strftime(x, '%A'))
            sbd = df.groupby('p_dow')[sp].sum().sort_values(by=sp, ascending=False)
            Bar(sbd, sbd.index, sbd.values, str.upper('Days of the Week'), str.upper('Total Sales'), str.upper('Total Sales by Days of the Week'))
            print('This chart shows that ', sbd.index[0], ' has the highest sales among the days of the week,', ' while ', sbd.index[6], ' has the lowest sales.')
            
        else:
            df[pdate].fillna('1908-01-01', inplace=True)
            df['p_dow'] = df[pdate].apply(lambda x: dt.strftime(x, '%A'))
            sd = df[df[pdate]!='1908-01-01']
            sbd = sd.groupby('p_dow')[sp].sum().sort_values(ascending=False)
            Bar(sbd, sbd.index, sbd.values, str.upper('Days of the Week'), str.upper('Total Sales'), str.upper('Total Sales by Days of the Week'))
            print('This chart shows that ', sbd.index[0], ' has the highest sales among the days of the week,', ' while ', sbd.index[6], ' has the lowest sales.')
        
    except KeyError:
        print('Column(s) cannot be found')
        

def totalGainLoss(df, sp, ucp, qty_sold):
    
    """
    This function determines the total profit or total loss.
    
    Parameters
    ---------------
    df: this is the dataframe or a table-like arrays.
    ucp: a panda series referring to the unit cost price.
    qty_sold: a panda series referring to the quantity of goods sold.
    sp: a panda series referring to the selling price.
    """
    
    df['tcp'] = df[ucp]*df[qty_sold]
    tgl = df[sp].sum() - df['tcp'].sum()
    if tgl>0:
        print('The total profit made on sales is: #', tgl)
    else:
        print('The total loss in sales is: #', tgl)
        
def Sales_by_year(df, pdate, sp):
    
    """
    This function evaluates sales by year.
    
    Parameters
    ---------------
    df: this is the dataframe or a table-like arrays.
    pdate: a panda series referring to the purchase date which is expected to be a datetime data type.
    sp: a panda series referring to the selling price.
    """
    
    from datetime import datetime as dt
    try:
        if df[pdate].isna().count()==0:
            df['p_year'] = df[pdate].apply(lambda x: dt.strftime(x, '%Y'))
            sby = df.groupby('p_year')[sp].sum().sort_values(by=sp, ascending=False)
            plt.figure(figsize=(15,8))
            sns.pointplot(data=sby, x=sby.index, y=sby.values, linestyles='-', ci=0, dodge=True);
            plt.xlabel('YEAR')
            plt.ylabel('TOTAL SALES')
            plt.xticks(rotation=45)
            plt.title('TOTAL SALES BY YEAR');
            print('This chart shows that ', sby.index[0], ' has the highest sales across the year.')            
        else:
            df[pdate].fillna('1908-01-01', inplace=True)
            df['p_year'] = df[pdate].apply(lambda x: dt.strftime(x, '%Y'))
            sy = df[df[pdate]!='1908-01-01']
            sby = df.groupby('p_year')[sp].sum().sort_values(ascending=False)
            year = sby.index
            plt.figure(figsize=(15,8))
            sns.pointplot(data=sby, x=sby.index, y=sby.values, linestyles='-', ci=0, dodge=True);
            plt.xlabel('YEAR')
            plt.ylabel('TOTAL SALES')
            plt.xticks(rotation=45)
            plt.title('TOTAL SALES BY YEAR');
            print('This chart shows that ', sby.index[0], ' has the highest sales across the year.')
            return sby
        
    except KeyError:
        print('Column(s) cannot be found')
        