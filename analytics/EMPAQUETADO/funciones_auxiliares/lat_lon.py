def latitud_decimal(latitud_ini, lista):
            
    grados_lat = latitud_ini[:2]
    min_lat = int(latitud_ini[2:4])/60
    seg_lat = int(latitud_ini[4:6])/3600
    latitud_decim = int(grados_lat)+min_lat+seg_lat
    
    #guardamos el resultado en una lista

    lista.append(latitud_decim)



def longitud_decimal(longitud_ini, lista_lon):

    grados_lon = longitud_ini[:2]
    min_lon = int(longitud_ini[2:4])/60
    seg_lon = int(longitud_ini[4:6])/3600
    longitud_decim = -1*(int(grados_lon)+min_lon+seg_lon)

    lista_lon.append(longitud_decim)