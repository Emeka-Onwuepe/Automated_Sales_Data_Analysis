from os import path
import pandas as pd

def convert_to_excel(data,dataset_location,file_name):
    df_file = path.join(dataset_location,f"{file_name}.xlsx")
    writer = pd.ExcelWriter(df_file,engine="xlsxwriter")
    data.to_excel(writer,index=False)
    writer.save()