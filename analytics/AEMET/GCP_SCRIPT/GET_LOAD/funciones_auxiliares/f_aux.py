

def busqueda_codigopostal(json):

    json = json[0]

    if 'address_components' in json.keys():
    
        for key in json.keys():

            print(json[key], end = '\n')
            
        
            
                
            if isinstance(json[key], list):

                for item in range(len(json[key])):
                    
                    try:
                    
                        if 'types' in json[key][item].keys() or isinstance(json[key][item]['types'], list):

                            if len(json[key][item]['long_name']) == 5:

                                #print(type(json[key][item]['long_name']))

                                try:
                                    #print(int(json[key][item]['long_name']))

                                    codigo_postal = int(json[key][item]['long_name'])

                                    return codigo_postal

                                except:

                                    print('... searching ...')
                                    
                    except: 
                        
                        print("... there is no more information to search for now... ")
                            

                    #print(json[key][item])
                        
                        
                    #print('ES LISTA')
                    
                
            
            
            
            
        
        
    #print('El código postal de la ubicación es: ', codigo_postal)

