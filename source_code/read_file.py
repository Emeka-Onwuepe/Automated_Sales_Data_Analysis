def read_dataset(model,user_id,dataset_id,pd):
    df = None
    dataset = None
    file_data = None
    
    try:

        dataset= model.objects.get(user_id__user_id = user_id, dataset_id= dataset_id)
        file_data = dataset.dataset
        _,file_extension = str(file_data).split(".")
        # load data
        if file_extension == 'xlsx':
            df = pd.read_excel(file_data)
        else:
            # remember to check for possibles errors
            #/t seperator and other non coma seperatorsS
            df = pd.read_csv(file_data)
    except model.DoesNotExist:
        pass
    
    file_data.close()
    return df,dataset