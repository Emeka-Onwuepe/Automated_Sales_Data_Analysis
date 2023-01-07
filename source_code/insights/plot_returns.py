import matplotlib
matplotlib.use("Agg")
import matplotlib.pylab as plt
from os import path


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
                start, end,result):
                try:
                    if split_into == 1:
                        result.append({"data":data[start:end],"feature":feature,"count":count})
                        count+=1
                        
                        result.append({"data":data[end:],"feature":feature,"count":count})
                        return result
                    
                 
                    result.append({"data":data[start:end],"feature":feature,"count":count})
                    start,end = end,end+max
                    split_into-=1
                    count+=1
                    return split_plot(split_into,data,max,
                                  feature,count,start,end,result)
                except IndexError:
                    return result
               

def average_returns(df,feature):
    maximium = 16
    count = 0
    
    data = df.groupby(feature)["returns(%)"].mean().sort_values()
    data.fillna(0,inplace = True)
          
    if len(data) > maximium:
        length = data.shape[1]
        split_into = length // maximium
        count = 1
        return split_plot(split_into,data,maximium,feature,
                           count,0, maximium,[])
    elif len(data) <= maximium:
        
        return [{"data":data,"feature":feature,"count":count}]
            
