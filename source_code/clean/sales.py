from pandas.api.types import is_numeric_dtype
from source_code.converter import list_to_string

def clean_sale_column(sale_data_column):
 
    sale_column = sale_data_column
    if is_numeric_dtype(sale_column):
        return (sale_column)
    cleaned_column = sale_column.astype("str")
    cleaned_column = cleaned_column.str.replace(',', '')
    cleaned_column = cleaned_column.str.extract("([\d.,]+)")
    cleaned_column= cleaned_column.astype(float)
    return (cleaned_column)

def cal_total_cost_price(df,mapper):
    formular = None
    try:
        df["total_cost_price"] = df[mapper["qty_sold"]].values * df[mapper["unit_cp"]].values
        formular = f"We got total_cost by multiplying {mapper['qty_sold']} with {mapper['unit_cp']}"
        return df,formular
    except KeyError:
        formular = None
        return df,formular
    
def cal_total_selling_price(df,mapper):
    
    possible_features = ["sp","discount_per","discount_amount"]
    formular = None
    for feature in possible_features:
        try:
            formular =  f"We got total_selling_price by multiplying {mapper['qty_sold']} with "
            if feature == "discount_per":
                discounted = None
                if df[mapper[feature]].max() > 1:
                    discounted = df[mapper["sp"]].values - (df[mapper["sp"]].values *  df[mapper[feature]].div(100) ) 
                    formular += f"{mapper['sp']} - ( {mapper['sp']} *  ({mapper[feature]} / 100)"
                else:
                    discounted = df[mapper["sp"]].values - (df[mapper["sp"]].values *  df[mapper[feature]].values ) 
                    formular += f"{mapper['sp']} - ( {mapper['sp']} *  ({mapper[feature]})"
                    
                df["total_selling_price"] = df[mapper["qty_sold"]].values * discounted
                return df,formular
            elif feature == "discount_amount":
                df["total_selling_price"] = df[mapper["qty_sold"]].values * (df[mapper["sp"]].values - df[mapper[feature]].values)
                formular += f"({mapper['sp']} - {mapper[feature]} )" 
                return df,formular
            else:
                df["total_selling_price"] = df[mapper["qty_sold"]].values * df[mapper["sp"]].values
                formular += f"{mapper['sp']}" 
                return df,formular
                
        except KeyError:
            formular = None
            continue
        
    return df,formular

def cal_gross_cost_price(df,mapper,multiple_features):
    formular = None
    features = []
    try:
       
        df['gross_cost_price'] = df['total_cost_price'].values + df[mapper["extra_cost"]]
        features.append(mapper['extra_cost'])
        try:
            for multiple_key in multiple_features["extra_cost"]:
             df['gross_cost_price'] = df['gross_cost_price'].values + df[mapper[multiple_key]]   
             features.append(mapper[multiple_key])      
        except KeyError:
            pass
    except KeyError:
        pass
    
    try:
        init = "gross_cost_price" if features else 'total_cost_price'
        df['gross_cost_price'] = df[init].values + (df[mapper["extra_cost_pu"]].values * df[mapper["qty_sold"]].values)
        features.append(f"({mapper['extra_cost_pu']} * {mapper['qty_sold']})")
        try:
            for multiple_key in multiple_features["extra_cost"]:
             df['gross_cost_price'] = df['gross_cost_price'].values + (df[mapper[multiple_key]] * df[mapper["qty_sold"]].values)   
             features.append({mapper[multiple_key]})  
             features.append(f"({mapper[multiple_key]} * {mapper['qty_sold']})")    
        except KeyError:
            pass
    except KeyError:
        pass
    
    if features: 
        formular = f"We got gross_cost_price by adding total_cost_price with "
        string,_ = list_to_string(features)
        formular += string
        
    return df,formular
    
def cal_delivery_profit(df,mapper):
    formular = None
    try:
        df["delivery_profit"] = df[mapper["del_charge"]].values - df[mapper["del_cost"]].values
        formular = f"We got delivery_profit by substracting {mapper['del_cost']} from {mapper['del_charge']}"
    except KeyError:
        pass
    return df,formular

def cal_profit(df,mapper,multiple_features,total_cp,total_sp):
    derivatives = []
    new_cols = []
    if not total_cp :
        df,total_cp_formular = cal_total_cost_price(df,mapper)
        if total_cp:
            derivatives.append(total_cp_formular)
            new_cols.append("total_cost_price")
            total_cp = True
    if not total_sp :
        df,total_sp_formular = cal_total_selling_price(df,mapper)
        if total_sp:
            derivatives.append(total_sp_formular)
            new_cols.append("total_selling_price")
            total_sp = True
    df,delivery_profit_formular = cal_delivery_profit(df,mapper)
    if delivery_profit_formular:
       derivatives.append(delivery_profit_formular)
       new_cols.append("delivery_profit")
    if total_cp:
        df,total_gcp_formular = cal_gross_cost_price(df,mapper,multiple_features)
        if total_gcp_formular:
            derivatives.append(total_gcp_formular)
            new_cols.append("gross_cost_price")
        if total_gcp_formular and total_sp and delivery_profit_formular:
            df["profit"] = df["total_selling_price"] - df["gross_cost_price"] + df["delivery_profit"]
            df['returns(%)'] = (( df["profit"].values/df["gross_cost_price"].values) * 100).round(2)
            formular = "We got profit by substracting (gross_cost_price + delivery_profit) from total_selling_price \
                then derived returns(%) by multipying (profit/gross_cost_price) by 100"
            derivatives.append(formular)
            new_cols += ["profit","returns(%)"]
        elif total_gcp_formular and total_sp:
            df["profit"] = df["total_selling_price"] - df["gross_cost_price"]
            df['returns(%)'] = ((df["profit"].values / df["gross_cost_price"].values ) * 100).round(2)
            formular = "We got profit by substracting gross_cost_price  from total_selling_price \
                then derived returns(%) by multipying (profit/gross_cost_price) by 100"
            derivatives.append(formular)
            new_cols += ["profit","returns(%)"]
        elif total_cp and total_sp and delivery_profit_formular:
            df["profit"] = df["total_selling_price"] - df["total_cost_price"] + df["delivery_profit"]
            df['returns(%)'] = (( df["profit"].values / df["total_cost_price"].values) * 100).round(2)
            formular = "We got profit by substracting (total_cost_price + delivery_profit) from total_selling_price \
                then derived returns(%) by multipying (profit/total_cost_price) by 100"
            derivatives.append(formular)
            new_cols += ["profit","returns(%)"]
        elif total_cp and total_sp:
            df["profit"] = df["total_selling_price"] - df["total_cost_price"]
            df['returns(%)'] = ((df["profit"].values / df["total_cost_price"].values ) * 100).round(2)
            formular = "We got profit by substracting total_cost_price from total_selling_price \
                then derived returns(%) by multipying (profit/total_cost_price) by 100"
            derivatives.append(formular)
            new_cols += ["profit","returns(%)"]
            
    return df,derivatives,new_cols     
   