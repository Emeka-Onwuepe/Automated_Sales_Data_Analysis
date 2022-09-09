from read_data_path import file_path,file_extension
import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# import seaborn as sns
# from general_cleaning import clean_cols
from classify import classify

# load data
if file_extension == 'xlsx':
    df = pd.read_excel(file_path)
else:
    # remember to check for possibles errors
    #/t seperator and other non coma seperatorsS
    df = pd.read_csv(file_path)
# classify the dataset
data = classify(df.columns)
mapper,columns,non_classified,not_matched = data

# rename columns
df.columns = columns
print(df[mapper["c_name"]][:10])

print("ran successfully")