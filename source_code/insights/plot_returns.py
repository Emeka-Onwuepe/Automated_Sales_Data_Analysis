import matplotlib
matplotlib.use("Agg")
import matplotlib.pylab as plt
from os import path

from source_code.sub_classes import PRODUCT_VAL
from matplotlib.pylab import close

def plot_average_returns(data,feature,count,pngs_location):
    
    info_df = None
    ylabel = "Percentage"
    xlabel = feature
    title = f"{feature} Average Returns(%) "
    
    fig,ax = plt.subplots(dpi=300,figsize = [12, 5])
    plt.subplots_adjust(bottom=0.30)
    data.plot.bar(rot=0,width=0.8,edgecolor="black",ax=ax)
   
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
    plt.xticks(rotation=15);
    
    label = f'{feature}_returns' if count < 1 else f"{feature}_returns_{count}"
    file_location = path.join(pngs_location,f'{label}.png')
    
    plt.savefig(file_location)
    # print(label)
    return fig,info_df

def split_plot(split_into,data,max,feature ,count,
                start, end,pngs_location,result,
                plot_average_returns = plot_average_returns):
                try:
                    if split_into == 1:
                        result.append(plot_average_returns(data[start:end],feature,count,pngs_location))
                        count+=1
                        result.append(plot_average_returns(data[end:],feature,count,pngs_location))
                        return result
                    
                 
                    result.append(plot_average_returns(data[start:end],feature,count,pngs_location))
                    start,end = end,end+max
                    split_into-=1
                    count+=1
                    return split_plot(split_into,data,max,
                                  feature,count,start,end,
                                  pngs_location,result)
                except IndexError:
                    return result
               

def average_returns(df,feature,pngs_location):
    maximium = 16
    count = 0
    
    data = df.groupby(feature)["returns(%)"].mean().sort_values()
    data.fillna(0,inplace = True)
          
    if len(data) > maximium:
        length = data.shape[1]
        split_into = length // maximium
        count = 1
        return split_plot(split_into,data,maximium,feature,
                           count,0, maximium,pngs_location,[])
    elif len(data) <= maximium:
        return [plot_average_returns(data,feature,count,
                                    pngs_location)]
            




def plot_average_returns_graphs(df,mapper,pngs_location,multiple_features,
                            story,fig2image,Paragraph,heading2,p_style):

    story.append(Paragraph('Average Sales Returns Graphs',heading2))
    content = "This shows the average percentage of profits to investement on products. For Example 10% averages shows that \
        the product on average has yeilded 10% of the cost price or gross cost price as profit "
    story.append(Paragraph(content,p_style))
    
    for feature in PRODUCT_VAL:
        graph_list = None
        try:
            graph_list = average_returns(df,mapper[feature],pngs_location)
        except KeyError:
            continue 
        
        if graph_list:
            for graph in graph_list:
                fig,info_df = graph
                story.append(fig2image(fig))
                close("all")
                del fig,info_df
    # multiple keys
    for feature in PRODUCT_VAL:
        graph_list = None
        try:
            for feature2 in multiple_features[feature]:
                try:
                    graph_list = average_returns(df,mapper[feature2],pngs_location)
                except KeyError:
                    continue 
        except KeyError:
            continue
        
            
        if graph_list:
            for graph in graph_list:
                fig,info_df = graph
                story.append(fig2image(fig))
                close("all")
                del fig,info_df
                         