import os
from map import get_lon_lat, map  
import pandas as pd
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

def main():
    # Map 
    dico_lon_lat = get_lon_lat() 
    m = map(dico_lon_lat)  
    st.write(m)  # Affichez la carte dans Streamlit
    
    lst_station = []

    for filename in os.listdir('pred'):
        # Supprimer le préfixe 'df_' et l'extension '.csv'
        station_name = filename.replace('df_', '').replace('.csv', '')  # Supprimez l'extension '.csv' ici
        lst_station.append(station_name)

    lst_station.append('Toutes les stations')

    station = st.selectbox('Station', lst_station)

    if station == 'Toutes les stations':
        df = pd.concat([load_data(s) for s in lst_station[:-1]])  # Exclure 'Toutes les stations' de la liste
    else:
        df = load_data(station)

    st.write(df.head())

    # Ajoute un bouton pour dl le df
    if st.button('Télécharger le DataFrame'):
        st.markdown(to_csv_download_link(df, f'{station}.csv'), unsafe_allow_html=True)

if __name__ == "__main__":
    main()
