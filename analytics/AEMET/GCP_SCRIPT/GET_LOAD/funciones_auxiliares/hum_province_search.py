

def extracc_provincia_hum(google_maps_output):
    
    if isinstance(google_maps_output, list):

        print('...por favor introduzca el [0] antes de meter el input: json[0]...')
    json = google_maps_output

    try: 
        for keys in json.keys():

            if 'address_components' in keys:

                #print(json[keys])

                for subkey in range(len(json[keys])):

                    #print(json[keys][subkey])

                    if 'administrative_area_level_2' in json[keys][subkey]['types'] and  'political' in json[keys][subkey]['types']: 



                        provincia_hum = json[keys][subkey]['long_name']

                        return provincia_hum

    except: 

        print(' ... it is not possible to extract humidity data out of this point in this province ... ' )