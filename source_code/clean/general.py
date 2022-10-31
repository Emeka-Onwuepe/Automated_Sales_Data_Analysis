from .date import clean_date


DATA_CLEANING = {'stock_date':clean_date,'sales_date':clean_date,
               'Order ID':'order_id','Product ID':'p_id','Unit Cost Price':'unit-cp',
               "Discount Percent":"discount_per","Discounted Amount":"discount_amount",
               'Quantity Sold':'qty-sold', "Payment Status":"payment_status",
               "Product Category":"p_cat","Processing Cost":"pro_cost",
               'Selling Price':'sp', 'Selling Price (discounted)':'sp_dis',
               "Sales' Grouping": "sales_grouping", 'Product Name':'p_name',
               'Shippinng Postal Code':'ship_p_code','del_date':clean_date,
               'Delivery Status':'delivered','Delivery Location':'del_location',
                'Delivery Cost':'del-cost','Delivery Charge':'del-charge',
                'Customer ID':'c_id','Customers\' Name':'c_name',
                "Customers' Grouping":"c_grouping",
                'Customer City':'c-city', 'Customer Region':'c-region',
                'Gender':'gender',
               }