from .date import clean_date
from .sales import clean_sale_column
from .confirmations import delivery
from .identifiers import clean_identifiers,clean_genders

DATA_CLEANING = {'stock_date':clean_date,'sales_date':clean_date,
               'order_id':clean_identifiers,'p_id':clean_identifiers,'unit-cp':clean_sale_column,
               "discount_per":clean_sale_column,"discount_amount":clean_sale_column,
               'qty-sold':clean_sale_column, "payment_status":clean_identifiers,
               "p_cat":clean_identifiers,"pro_cost":clean_sale_column,
               'sp':clean_sale_column, 'sp_dis':clean_sale_column,
               "sales_grouping":clean_identifiers,'p_name':clean_identifiers,
               'ship_p_code':clean_identifiers,'del_date':clean_date,
               'delivered':delivery,'del_location':clean_identifiers,
                'del-cost':clean_sale_column,'del-charge':clean_sale_column,
                'c_id':clean_identifiers,'c_name':clean_identifiers,
                "c_grouping":clean_identifiers,
                'c-city':clean_identifiers,'c-region':clean_identifiers,
                'gender':clean_genders,
               }