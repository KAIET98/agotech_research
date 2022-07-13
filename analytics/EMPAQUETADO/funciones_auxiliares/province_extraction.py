

def search_province(objeto):

    elementos_gmaps = objeto.keys()

    
    if 'address_components' in elementos_gmaps: 

        print(' ... it is possible to extract the province information ...')

        #print(objeto['address_components'])

        #print(type(objeto['address_components']))

        for subelementolista in objeto['address_components']: 

            
            #print(subelementolista, end = '\n')

        # print(subelementolista.keys())

            for subelementlistkeys in subelementolista.keys(): 

            # print(subelementolista[subelementlistkeys])

                
                if subelementlistkeys == 'types':

                    #print(subelementolista[subelementlistkeys])

                    if subelementolista[subelementlistkeys][0] == 'administrative_area_level_2': 
                        
                        print(' ... province obtained ...')

                        provincia = subelementolista['long_name']

                        print(' the province is: {}'.format(provincia))


                        return provincia 

