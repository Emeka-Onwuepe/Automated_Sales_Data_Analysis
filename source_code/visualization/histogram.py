import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline
def hist_func(df,col):
    ''' An histogram function to to find to distribution of numeric
         data in a colunm. '''
    if 10 <= df[col].max() <= 10000:
        bins = np.arange(df[col].min(),df[col].max()+30,30)
        plt.hist(data=df,x=col,bins=bins)
        plt.xlabel('{}'.format(col))
        plt.title('Plotting the graph of frequency against {}'.format(col))
        plt.show();
    elif df[col].max() < 10:
        def sqrt_trans(x,inverse=False):
            ''' creating a function to find quare-root and to reverse it back. '''
            if not inverse:
                return np.sqrt(x)
            else:
                return x**2
        bins = np.arange(0,sqrt_trans(df[col].max())+0.1,0.1)
        plt.hist(df[col].apply(sqrt_trans),bins=bins)
        plt.xlabel('{}'.format(col))
        plt.title('Plotting the graph of frequency against the sqare-root of {}'.format(col))
        #identify the tick locations
        tick_locs = np.arange(0,sqrt_trans(df[col].max())+10,10)
        #apply tick
        plt.xticks(tick_locs,sqrt_trans(tick_locs,inverse=True).astype(int))
        plt.show();
    elif df[col].max() > 10000:
        plt.figure(figsize=[8,8])
        bins =10**np.arange(0,np.log10(df[col].max())+0.07,0.07)
        plt.hist(data=df,x=col,bins=bins)
        plt.xscale('log')
        plt.xlabel('log of {}'.format(col))
        plt.title('Plotting frequency agains the log transform of {}'.format(col))
        plt.show();

