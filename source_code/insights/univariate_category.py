# import necessary modules
import matplotlib.pyplot as plt
import seaborn as sns


# define function that plot a chart for a single category feature
def Univariate_plot_category(df, col):
    # check if the col is category data type and plot a bar chart if yes and report error if no
    try:
        if df[col].nunique()<=8:
            plt.figure(figsize=(8,5))
            chart = sns.countplot(data=df, x=col, color=sns.color_palette('dark')[0]);
            plt.title('Distribution of Values in '+ col, fontsize=16)
            plt.xticks(rotation=15)
            plt.xlabel(xlabel=col, fontsize=14)
            plt.ylabel(ylabel='Count', fontsize=14)
            chart
            print('The chart below gives the distribution of values in the ',col)
        else:
            print('This is not a category column')
    except KeyError:
        print('The column cannot be found in the dataframe. Kindly, ensure that the case match.')