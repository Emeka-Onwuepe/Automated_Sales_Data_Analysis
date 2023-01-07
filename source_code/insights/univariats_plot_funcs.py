import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pylab as plt
import seaborn as sns
from os import path

def get_percentage(series):
    '''Takes in a series/list and returns the percentage
        of each element to the summation of the list/series elements'''
    
    return round((series/np.sum(series)) * 100,2)


def plot_graph(df,graph_type, title ,xlabel, ylabel, ylim,pngs_location):
    '''Takes in a datafrme and plots either bar or pie chart

        Paramenters
        df: Dataframe
        graph_type: str
        title: str
        xlabel: str
        ylabel: str
        pngs_location: path
        ylim: boolean
    
    '''    
   
    fig,ax = plt.subplots(dpi=300,figsize = [12, 5])
    plt.subplots_adjust(bottom=0.30)
    
    if graph_type == "bar":
        df.plot.bar(rot=0,width=0.8,edgecolor="black",color=sns.color_palette()[:10],ax=ax)
    elif graph_type == 'pie':
        df.plot.pie(subplots=True,ax=ax)
    else:
        rows,_ = df.shape
        if  rows < 5 and rows > 1:
            graph_type = "pie"
            df.plot.pie(subplots=True,autopct=lambda pct:"{:.2f}%".format(pct),wedgeprops=dict(width=0.5), startangle=-40,ax=ax)
        elif rows >= 5 :
            df.plot.bar(rot=0,width=0.8,edgecolor="black",color=sns.color_palette()[:10],ax=ax)
        else:
            return None,None
            
        
        
    if ylim and graph_type != "pie" :
        plt.ylim(0,100)
        labels = df.iloc[:,0]
        for i in range(len(labels)):
            plt.text(i, labels[i] + 1, f'{labels[i]}%', ha = 'center')
        
    # Add title and format it
    plt.title(title.title(),
               fontsize = 14, weight = "bold")
    # Add x label and format it
    plt.xlabel(xlabel.title(),fontsize = 10, weight = "bold")
    # Add y label and format it
    plt.ylabel(ylabel.title(),
               fontsize = 10, weight = "bold")
    plt.xticks(rotation=15);
    
    file_location = path.join(pngs_location,f'{xlabel}.png')
    plt.savefig(file_location)
   
    return fig

def feature_uniques_percentage(df,feature_name,graph=None,ylim= True,
                               cal_percentage = get_percentage):
    '''Takes in string feature_name and other optional arguments 
        and plots either bar or pie chart of the feature unique
        values percentages

        Paramenters
        df: dataframe
        feature_name: str
        graph: str -- optional -- default: None
        ylim: boolean -- optional -- default: True
        cal_percentage: function -- optional -- default: global scope get_percentage function
         
    '''
    #  get the counts of the feature unique values
    feature_df = df[feature_name].value_counts().to_frame()
    
   
    feature_df["count"] = feature_df[feature_name]
    feature_df[feature_name] = cal_percentage(feature_df[feature_name])
    
    info_df = feature_df.apply(lambda row:   f" {row.name} had {row['count']} counts which represents " + 
                       f'{row[feature_name]}%.', axis=1)
    
    feature_df.drop("count",inplace=True,axis=1)    

    title = f"unique values percentages of {feature_name} feature " 
    #   call the graph function
    return {"df":feature_df,"graph_type":graph,"title":title,"xlabel":feature_name,
             "ylabel":'Percentage',"ylim":ylim},info_df
    
    # return graph_fun(feature_df,graph,title,feature_name,'Percentage',ylim,pngs_location,info_df=info_df)
    

