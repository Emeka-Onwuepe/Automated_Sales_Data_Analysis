SUB_CLASSES =  {'Stock Date':'stock_date','Sales Date':'sales_date',
               'Order ID':'order_id','Product ID':'p_id',
               'Quantity Sold':'qty_sold', "Payment Status":"payment_status",
               "Product Category":"p_cat",'Unit Cost Price':'unit_cp',
               "Extra Cost":"extra_cost","Extra Cost Per Unit":"extra_cost_pu",'Selling Price':'sp', 
               "Total Cost Price":"total_cp","Total Selling Price":"total_sp",
               "Discount Percent":"discount_per",
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

TIME_SEERIES_VAL = ['p_cat','sales_grouping','p_name']
PRODUCT_VAL = ['p_cat','p_name']

SUB_CLASSES_EXP =  {"Select the appropriate label":"Kindly leave any unnecessary column/feature unselected \
                         or select not found",
                    'Stock Date':'Represents stock date. Not advisable to be selected more than once.',
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
                    "Extra Cost":"Represents any other cost incured apart from \
                         the unit cost price eg tax. This can be selected multiple times. ",
                    "Extra Cost Per Unit":"Represents any other cost incured apart from \
                         the unit cost price that is recorded per unit. This will be multiplied with quantity sold \
                              during calculation. This can be selected multiple times.",
                    'Selling Price':'Represents selling price without discount, the actual selling price.\
                     Should be seleted once.', 
                    "Total Cost Price":"Represents the total cost price if available else the system will calculate it. \
                    Should be selected only once",
                    "Total Selling Price":"Represents the total selling price if available else the system will calculate it.\
                     Should be selected only once",
                     "Discounted Amount":"Represents the actual sales discounted amount from the product \
                         selling price.Not advisable to be selected more than once.",
                    "Discount Percent":"Represents the discounted percentage and not the actual discounted \
                         amount from the product selling price. Not advisable to be selected more than once.",
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
                'Delivery Cost':'Represents the delivery actual cost and not the amount a customer/client was charged or paid . \
                     This could be selected if the amount charged for delivery is different from the real cost of such delivery. \
                         Not advisable to be selected more than once.',
                'Delivery Charge':"Represents the actual amount charged or paid by the customer.Please note that we don't factor in \
                     delivery charge or cost while calculating profit/loss unless when they are both present in a dataset which indicates \
                          a possibility of having either gain or loss in the course of delivery. Not advisable to be selected more than once.",
                'Customer ID':'Represents the customers ID. Not advisable to be selected more than once.',
                'Customers\' Name':"Represents the customers' names. Not advisable to be selected more than once.",
                'Customer Address':"Represents customers' location/address.This can be selected multiple times. ",
                'Age':"Represents age feature. This can be selected multiple times depending on the use case",
                'Gender':'Represents gender feature.This can be selected multiple times dependiing on the use case",',
                "Customers' Grouping":"Represents anyother non-numeric customers' information with the exception of age, gender, \
                     customers' name and address.   ",
               'Not Found': "Select this if you didn't find an appropriate label for such feature or column. Kindly contact us when and \
                    if you think that such feature is very import. Note that we calculate profit/loss during the analysis, thus, we found it \
                         unnecessary to include such features like total amount, profit/loss etc, which could easily be derived."
               }