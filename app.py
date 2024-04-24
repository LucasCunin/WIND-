import os
import pandas as pd
import streamlit_folium as sf
import folium
import streamlit as st
import base64

def load_data(station):
    file_path = os.path.join('pred', f'df_{station}.csv') 
    df = pd.read_csv(file_path)
    return df

def to_csv_download_link(df, filename):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">Télécharger le DataFrame CSV</a>'
    return href

def create_map(dico):
    m = folium.Map(location=[43.296482, 5.36978], zoom_start=9)

    for point, coordinates in dico.items():
        if pd.isna(coordinates[0]).any() or pd.isna(coordinates[1]).any():
            print(f"Pas de données de localisation pour {point}.")
        else:
            folium.Marker(
                location=[coordinates[0].iloc[0], coordinates[1].iloc[0]],  # Prenez la première valeur de chaque série
                popup=point,
            ).add_to(m)

    return m



def main():
    lst_station = []
    dico_station = {}

    for filename in os.listdir('pred'):
        station_name = filename.replace('df_', '').replace('.csv', '')
        lst_station.append(station_name)

    lst_station.sort()
    lst_station.append('Toutes les stations')

    station = st.selectbox('Station', lst_station)

    if station == 'Toutes les stations':
        if st.button('Télécharger les données au format CSV'):
            with open('data_frame.zip', 'rb') as f:
                bytes = f.read()
                b64 = base64.b64encode(bytes).decode()
                href = f'<a href="data:file/zip;base64,{b64}" download="data_frame.zip">Télécharger le fichier zip</a>'
                st.markdown(href, unsafe_allow_html=True) 

        for station in lst_station[:-1]:
            df = load_data(station)
            dico_station[station] = [df['lat'], df['lon']]
            
    else:
        df = load_data(station)
        st.write(df.head())
        if st.button('Télécharger le DataFrame'):
            st.markdown(to_csv_download_link(df, f'{station}.csv'), unsafe_allow_html=True)

        dico_station[station] = [df['lat'], df['lon']]

    m = create_map(dico_station)
    sf.folium_static(m)

if __name__ == "__main__":
    main()
