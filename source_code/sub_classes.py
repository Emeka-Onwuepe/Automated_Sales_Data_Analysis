SUB_CLASSES =  {'Stock Date':'stock_date','Sales Date':'sales_date',
               'Order ID':'order_id','Product ID':'p_id',
               'Quantity Sold':'qty_sold', "Payment Status":"payment_status",
               "Product Category":"p_cat",'Unit Cost Price':'unit_cp',
               "Processing Cost":"pro_cost",'Selling Price':'sp', 
               'Selling Price (discounted)':'sp_dis',"Discount Percent":"discount_per",
               "Discounted Amount":"discount_amount",
               "Sales' Grouping": "sales_grouping", 'Product Name':'p_name',
               'Shippinng Postal Code':'ship_p_code','Delivery Date':'del_date',
               'Delivery Status':'delivered','Delivery Address':'del_location',
                'Delivery Cost':'del_cost','Delivery Charge':'del_charge',
                'Customer ID':'c_id','Customers\' Name':'c_name',
                "Customers' Grouping":"c_grouping",
                'Customer_address':'c_address',
                'Age':"age",'Gender':'gender',
               }

CRITICAL = ["unit_cp","sp","discount_per","discount_amount","qty_sold",
            "pro_cost","sp_dis"]
# CAT_UNIVARIATS = ['gender',"p_cat","sales_grouping",'payment_status','delivered',
#                   "del_location","c_grouping",'c_region']

TIME_SEERIES_VAL = ['p_cat','sales_grouping','p_name','c_grouping']

SUB_CLASSES_EXP =  {'Stock Date':'Represents stock date. Not advisable to be selected more than once.',
                    'Sales Date':'Represents sales date. Not advisable to be selected more than once.',
                    'Order ID':'Represrnts sales Order Id. Not advisable to be selected more than once.',
                    'Product ID':'Reprents the unique IDs associated to a particular product.Not advisable to \
                         be selected more than once.',
                    
                    "Payment Status":"Represents the service/product payment status.Not advisable to be selected \
                         more than once. ",
                    "Product Category":"Represents various product classifications like size,brand,type,color etc.\
                         This can be selected multiple times. ",
                    'Unit Cost Price':'Represents the product/service cost price per unit.Not advisable to be \
                         selected more than once.',
                    "Processing Cost":"Represents a processing cost if any, or any other cost incured apart from \
                         the unit cost price. Not advisable to be selected more than once. ",
                    'Selling Price':'Represents selling price without discount.', 
                    'Selling Price (discounted)':'Represents discounted selling price.',
                     "Discounted Amount":"Represents the actual sales discounted amount from the product \
                         selling price.Not advisable to be selected more than once.",
                    "Discount Percent":"Represents the discounted percentage and not the actual discounted \
                         amount from the product selling price.Not advisable to be selected more than once.",
                    'Quantity Sold':'This is the unit/quantity of product sold or offered. Not advisable to be \
                         selected more than once.', 
                    "Sales' Grouping": "Represents different sales groupings like sales channels, sales \
                         personnels etc. This can be selected multiple times.", 
                    'Product Name':'Represents the product names.Not advisable to be selected more than once.',
               'Shippinng Postal Code':'Represents the shipping code. Not advisable to be selected more than once.',
               'Delivery Date':'Represents the date the product/service was delivered to customer/client.Not advisable to be \
                         selected more than once.',
               'Delivery Status':'Represents the delivery status. Not advisable to be selected more than once.',
               'Delivery Address':'Represents the the delivery location or address. Not advisable to be \
                         selected more than once.',
                'Delivery Cost':'Represents the delivery cost and not the amount charged. This could be selected \
                     if the amount charged for delivery is different from the real cost of such delivery and this option \
                          represents the real cost. Not advisable to be selected more than once.',
                'Delivery Charge':'Represents the actual amount charged or paid by the customer.Not advisable to be \
                         selected more than once.',
                'Customer ID':'Represents the customers ID. Not advisable to be selected more than once.',
                'Customers\' Name':"Represents the customers' names. Not advisable to be selected more than once.",
                'Customer Address':"Represents customers' location/address.This can be selected multiple times. ",
                'Age':"Represents age feature. This can be selected multiple times depending on the use case",
                'Gender':'Represents gender feature.This can be selected multiple times dependiing on the use case",',
                "Customers' Grouping":"Represents anyother non-numeric customers' information with the exception of age, gender, \
                     customers' name and address.   ",
               }