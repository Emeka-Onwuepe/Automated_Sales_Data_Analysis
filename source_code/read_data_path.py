from settings import (INPUT_FOLDER, ALLOWED_FILE_TYPES,
                      get_data_absolute_path)

dataset = None

try:
    [dataset] = INPUT_FOLDER 
except ValueError:
        print('got zero or more than one datasets, check input folder')
        quit()
        
_,file_extension = dataset.split(".")
        
if file_extension not in ALLOWED_FILE_TYPES:
    print('only xlsx and csv files are supported at the moment')
    quit()
file_path = get_data_absolute_path(dataset) 

