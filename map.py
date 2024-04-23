import folium
import os
import pandas as pd

df_loca = pd.read_csv('listeStations_Metro-OM_PackRadome.csv', sep=';')

def get_lon_lat():
    dico_lon_lat = {}
    
    for files_name in os.listdir('pred'):
        name = files_name.replace('df_','').replace('.csv','')

        if 'station' in name:
            name = name.replace('station','')
        if '_' in name:
            name = name.replace('_',' ')#remettre les espace dans les nom de vielle

        # Vérifiez si le nom de la station existe dans le DataFrame
        if name in df_loca['Nom_usuel'].values:
            lon = df_loca.loc[df_loca['Nom_usuel'] == name, 'Longitude'].values[0]
            lat = df_loca.loc[df_loca['Nom_usuel'] == name, 'Latitude'].values[0]

            dico_lon_lat[name] = (lon, lat)

    return dico_lon_lat


def map(dico_lon_lat):
    # Create a map centered at the mean latitude and longitude
    m = folium.Map(location=[df_loca['Latitude'].mean(), df_loca['Longitude'].mean()], zoom_start=12)

    # Add a marker for each station
    for name, (lon, lat) in dico_lon_lat.items():
        folium.Marker(
            location=[lat, lon],
            popup=name,
        ).add_to(m)

    return m

# Get the longitude and latitude of each station
dico_lon_lat = get_lon_lat()

# Create the map
m = map(dico_lon_lat)

# Display the map
m



