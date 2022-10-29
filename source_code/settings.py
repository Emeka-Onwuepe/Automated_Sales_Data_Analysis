import os

file_base = "./input"
INPUT_FOLDER = os.listdir(file_base)

def get_data_absolute_path(dataset, file_base=file_base):
    return os.path.join(file_base,dataset)  

ALLOWED_FILE_TYPES = ['xlsx','csv']

CLASSES = ['date','identifiers','confirmations','locations','sales','quantity']

SUB_CLASSES =  {'stock-date':'date','purchase-date':'date','del-date':'date',
               'order-id':'identifiers','p-name':'identifiers','p-id':'identifiers',
               'c-id':'identifiers','c-name':'identifiers','ship-p-code':'identifiers',
               'gender':'identifiers','delivered':'confirmations','del-location':'locations',
               'c-city':'locations', 'c-region':'locations','unit-cp':'sales','sp':'sales',
               'del-cost':'sales','del-price':'sales','qty-sold':'quantity'
               }

DATA_TYPES =  {'stock-date':'date','purchase-date':'date','del-date':'date',
               'order-id':'str','p-name':'str','p-id':'str','c-id':'str',
               'c-name':'str','ship-p-code':'str','gender':'str',
               'delivered':'boolean','del-location':'str','c-city':'str',
               'c-region':'str','unit-cp':'float','sp':'float',
               'del-cost':'float','del-price':'float','qty-sold':'float'
               }