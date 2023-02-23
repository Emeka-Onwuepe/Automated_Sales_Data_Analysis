from os import path
from matplotlib import use
use("Agg")
import matplotlib.pylab as plt
from numpy import array_split


def plot_time_series(data,feature,count,pngs_location,period = "d"):
    
    labels = None
    xticks = None
    xlabel = "Days" if period == "d" else "Months"
    
    
    if period == "d":
        labels = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        xticks = [0,1,2,3,4,5,6]
        title = f'Daily average quantity sold ({feature}) '
        ylabel = f'Average Count'
    elif period == 'm':
        labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul',"Aug","Sep","Oct","Nov","Dec"]
        xticks = [0,1,2,3,4,5,6,7,8,9,10,11]
        title = f'monthly total quantity sold ({feature}) '
        ylabel = f'Quantity'
       
    # base_color = color_palette()[0]
    # plt.figure(figsize = [16,5])
    
    fig,ax = plt.subplots(dpi=300,figsize = [12, 5])
    plt.subplots_adjust(bottom=0.30)
    # data.plot(marker="P",alpha=0.5,ax=ax);
    data.plot.bar(ax=ax)
    plt.xticks(xticks,labels=labels);
    # fig.canvas.draw()
    
    # print(ax.yaxis.get_offset_text().get_text())
    
    plt.title(title.title(),fontsize = 14, weight = "bold");
    # Add x label and format i
    plt.xlabel(xlabel,fontsize = 10, weight = "bold");
    # Add y label and format it
    plt.ylabel(ylabel,
                fontsize = 10, weight = "bold");
    plt.grid();
    
    label = f'{feature}_{xlabel}' if count < 1 else f"{feature}_{xlabel}_{count}"
    file_location = path.join(pngs_location,f'{label}.png')
    
    plt.savefig(file_location)
    return fig

def average_sales(df,sales_date,feature,mapper,period):
    maximium = 6
    data_list = []
    info_df = None
    data = None
    if period == "d":
        data = df.groupby([df[sales_date].dt.dayofweek,feature])[mapper['qty_sold']].median().unstack()
    elif period == "m":
        data = df.groupby([df[sales_date].dt.month,feature])[mapper['qty_sold']].sum().unstack()
    data.fillna(0,inplace = True)
    # info_df = time_series_insights(data,period,feature)
    if data.shape[1] > maximium:
        length = data.shape[1]
        split_into = length // maximium
        if (length % maximium) > 0:
            split_into += 1
        start = 0
        end = maximium
        for i in range(split_into):
            if i == (split_into - 1):
                data_list.append(data.iloc[:,start:])
            else:
                data_list.append(data.iloc[:,start:end])
                start,end = end,end+maximium
        del start,end
    else:
        data_list.append(data)

    return data_list,data
