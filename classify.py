from settings import SUB_CLASSES

def classify(cols):
    classified  = {}
    not_matched = []
    non_classified = []
    filtered = []
    col_name,identifier = None,None
    
    for feature in cols:
        # convert to lowercase 
        try:
            feature = feature.strip().lower()
        except AttributeError:
            feature = str(feature)
    
        try:
           col_name,identifier = feature.split(':')
           identifier = identifier.strip()
           if identifier in SUB_CLASSES.keys():
                identifier = identifier.replace("-","_") 
                classified[identifier] = col_name
                filtered.append(col_name) 
           else:
               not_matched.append(feature)
               filtered.append(feature) 
        except ValueError:
            non_classified.append(feature)
            filtered.append(feature)
    return [classified,filtered,non_classified,not_matched]