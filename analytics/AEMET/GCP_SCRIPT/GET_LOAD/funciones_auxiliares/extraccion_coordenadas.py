
def extraccion_coordenadas(json):

    json = json[0]

    for item in json: 

    #print(item, end = '\n')

    

    #--- obtenemos su punto de lat, lon

        if 'geometry' == item: 

            print(' ... obtaining geolocalisation data ...')

            print(json[item], end = '\n')

            if 'location' in json[item].keys():

                print('... obtaining exact coordenates ... ')

                raw_coordenates = list(json[item]['location'].values())

                #print(list(json[item]['location'].values()))


                latitude = raw_coordenates[0]
                longitude = raw_coordenates[1]

                coordenates_location = (latitude, longitude)

                return coordenates_location

                #print('Coordinates : ', coordenates_location)

        else: 

            print(' ... it has not been possible to extract locations exact coordenates ... ')

