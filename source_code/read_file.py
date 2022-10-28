
def read_dataset(model,user_id,dataset_id,pd):
    df = None
    dataset = None

    try:

        dataset= model.objects.get(user_id__user_id = user_id, dataset_id= dataset_id)
        _,file_extension = str(dataset.dataset).split(".")
        # load data
        if file_extension == 'xlsx':
            df = pd.read_excel(dataset.dataset)
        else:
            # remember to check for possibles errors
            #/t seperator and other non coma seperatorsS
            df = pd.read_csv(dataset.dataset)
    except model.DoesNotExist:
        pass

    return df,dataset