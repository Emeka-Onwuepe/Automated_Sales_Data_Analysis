SUB_CLASSES =  {'Stock Date':'stock_date','Sales Date':'sales_date',
               'Order ID':'order_id','Product ID':'p_id','Unit Cost Price':'unit_cp',
               "Discount Percent":"discount_per","Discounted Amount":"discount_amount",
               'Quantity Sold':'qty_sold', "Payment Status":"payment_status",
               "Product Category":"p_cat","Processing Cost":"pro_cost",
               'Selling Price':'sp', 'Selling Price (discounted)':'sp_dis',
               "Sales' Grouping": "sales_grouping", 'Product Name':'p_name',
               'Shippinng Postal Code':'ship_p_code','Delivery Date':'del_date',
               'Delivery Status':'delivered','Delivery Location':'del_location',
                'Delivery Cost':'del_cost','Delivery Charge':'del_charge',
                'Customer ID':'c_id','Customers\' Name':'c_name',
                "Customers' Grouping":"c_grouping",
                'Customer City':'c_city', 'Customer Region':'c_region',
                'Gender':'gender',
               }

CRITICAL = ["unit_cp","sp","discount_per","discount_amount","qty_sold",
            "pro_cost","sp_dis"]