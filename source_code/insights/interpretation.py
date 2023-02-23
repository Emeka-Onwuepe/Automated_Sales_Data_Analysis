from source_code.converter import list_to_string

def time_series_insights(data,period,feature):
    insight = ""
    if period == "d":
        labels = ['Mondays', 'Tuesdays', 'Wednesdays', 'Thursdays', 'Fridays', 'Saturdays', 'Sundays']
        index = [0,1,2,3,4,5,6]
        title = f'Daily average quantity sold ({feature})'
        required_num = 7
    elif period == 'm':
        labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul',"Aug","Sep","Oct","Nov","Dec"]
        index = [0,1,2,3,4,5,6,7,8,9,10,11]
        title = f'Monthly average quantity sold ({feature})'
        required_num = 12
        
    #check if period is more 3
    num_periods = data.shape[0]
    if num_periods > 3:
        #check if there is sales in all periods
        if required_num > num_periods:
            non_sales = set(index) - set(data.index)
            non_sales_months = [labels[index] for index in non_sales]
            string,is_plural = list_to_string(non_sales_months)
            insight = f"Sales were not recorded in any of {feature} items on the {'months' if is_plural else 'month'} of {string}"
        else:
            insight = f"Sales were recorded on all the {'months'if period=='m' else 'days'}" 
        #check for min sales
        minimum_sales = data.loc[data.sum(axis=1) == data.sum(axis=1).min()]
        string,is_plural = list_to_string([labels[index] for index in minimum_sales.index])
        insight += f" while the minimum sales were recorded on {string}."
        #check for max sales
        max_sales = data.loc[data.sum(axis=1) == data.sum(axis=1).max()]
        string,is_plural = list_to_string([labels[index] for index in max_sales.index])
        max_sum = max_sales.sum().to_frame().rename(columns={0:"sum"})
        string2,is_plural2 = list_to_string((max_sum[max_sum['sum'] == max_sum["sum"].max()].index))
        insight += f" The maximum sales were recorded on {string}, "
        insight += f"the highest {'contributors were' if is_plural2 else 'contributor is'} {string2}."
    elif num_periods > 1 :
        insight = f"{tittle} has just {num_periods} periods and we believe you can easily interpret it."
    elif num_periods == 1 :
        insight = f"{tittle} has just {num_periods} period and we believe you can easily interpret it."
    return insight  



def returns_insights(data):
    data = data.to_frame()
    insight = ""
    above_30 = data[(data["returns(%)"] > 30) & (data["returns(%)"] < 50)].index
    above_50 = data[(data["returns(%)"] > 50) & (data["returns(%)"] < 100)].index
    above_100 = data[data["returns(%)"] > 100].index
    if above_30.size:
        string,is_plural = list_to_string(above_30)
        insight = f"Investment on {string} returned more than 30% profit "
    if above_50.size and not above_30.size:
        string,is_plural = list_to_string(above_50)
        insight = f"Investment on {string} returned more than 50% profit."
    if above_50.size:
        string,is_plural = list_to_string(above_50)
        insight += f"while investment on {string} returned more than 50% profit."
    if above_100.size:
        string,is_plural = list_to_string(above_100)
        insight += f"Investment on {string} {'were' if is_plural else 'was'} very profitable, it returned more than 100% profit."
    return insight