
def province_search(json_):

    print('...cooking...')

    json = json_[0]

    #print(json.keys())

    for keys in json.keys():

        #print(key)

        for subkey in json[keys]:

            #print(json[keys])
            
            if isinstance(subkey, dict):
                
                if 'locality'  in subkey['types'] and 'political' in subkey['types']:
                    
                    provincia = subkey['long_name']
                    
                    return provincia