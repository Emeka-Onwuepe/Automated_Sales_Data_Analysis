# from seaborn import color_palette
import matplotlib.pylab as plt
from os import path

from source_code.sub_classes import TIME_SEERIES_VAL

# data_sum = df_clean.groupby(df_clean.start_time.dt.dayofweek)['distance_km','duration_hr'].sum()
# data_count = df_clean.groupby(df_clean.start_time.dt.dayofweek)['distance_km'].count()

def plot_time_series(data,feature,count,pngs_location,period = "d"):
    
    labels = None
    xticks = None
    info_df = None
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
        ylabel = f'Total Count'
       
    # base_color = color_palette()[0]
    # plt.figure(figsize = [16,5])
    
    fig,ax = plt.subplots(dpi=300,figsize = [12, 5])
    plt.subplots_adjust(bottom=0.30)
    data.plot(marker="P",ax=ax);
    plt.xticks(xticks,labels=labels);
    # print("yticks")
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
    print(label)
    return fig,info_df

def split_plot(split_into,data,max,feature ,count,
                start, end,pngs_location,period,result,
                plot_time_series = plot_time_series):
                try:
                    if split_into == 1:
                        result.append(plot_time_series(data.iloc[:,start:end],feature,count,pngs_location,period))
                        count+=1
                        result.append(plot_time_series(data.iloc[:,end:],feature,count,pngs_location,period))
                        return result
                    
                 
                    result.append(plot_time_series(data.iloc[:,start:end],feature,count,pngs_location,period))
                    start,end = end,end+max
                    split_into-=1
                    count+=1
                    return split_plot(split_into,data,max,
                                  feature,count,start,end,
                                  pngs_location,period,result)
                except IndexError:
                    return result
               

def average_sales(df,sales_date,feature,mapper,pngs_location,period ="d"):
    maximium = 6
    count = 0
    if period == 'd':
    
        data_median = df.groupby([df[sales_date].dt.dayofweek,feature])[mapper['qty_sold']].median().unstack()

        data_median.fillna(0,inplace = True)
        
        
        if data_median.shape[1] > maximium:
            length = data_median.shape[1]
            split_into = length // maximium
            count = 1
            return split_plot(split_into,data_median,maximium,feature,
                           count,0, maximium,pngs_location,period,[])
        elif data_median.shape[1] <= maximium:
            return [plot_time_series(data_median,feature,count,
                                    pngs_location,period)]
            
    else:
        period = "m"
        count = 0
        data_sum = df.groupby([df[sales_date].dt.month,feature])[mapper['qty_sold']].sum().unstack()
        data_sum.fillna(0,inplace = True)
      
        if data_sum.shape[1] > maximium:
            count = 1
            length = data_sum.shape[1]
            split_into = length // maximium
            return split_plot(split_into,data_sum,maximium,
                              feature,count,0, maximium,
                              pngs_location,period,[])
        elif data_sum.shape[1] <= maximium:
            return [plot_time_series(data_sum,feature, count,
                                    pngs_location,period)]



def plot_time_series_graphs(df,mapper,pngs_location,multiple_features,
                            story,fig2image,period,Paragraph,heading2):
    label_period = "Daily"
    if period == "d":
        label_period = "Daily"
    elif period == "m":
        label_period = "Monthly"
    
    story.append(Paragraph(f'{label_period} Sales Graphs',heading2))
    for feature in TIME_SEERIES_VAL:
        graph_list = None
        try:
             graph_list = average_sales(df,mapper['sales_date'],mapper[feature],mapper,pngs_location,period)
        except KeyError:
            continue 
        
        if graph_list:
            for graph in graph_list:
                fig,info_df = graph
                story.append(fig2image(fig))
    # multiple keys
    for feature in TIME_SEERIES_VAL:
        graph_list = None
        try:
            for feature2 in multiple_features[feature]:
                try:
                    graph_list = average_sales(df,mapper['sales_date'],mapper[feature2],mapper,pngs_location,period)
                except KeyError:
                    continue 
        except KeyError:
            continue
        
            
        if graph_list:
            for graph in graph_list:
                fig,info_df = graph
                story.append(fig2image(fig))
                         