import pandas as pd
import folium
from folium.plugins import MarkerCluster

# Paso 1: Cargar el DataFrame (a partir de tu CSV o DataFrame existente)
df = pd.read_csv('Data_csv/Players_20242025_Cities_Countries.csv')
print(df)
# Paso 2: Crear un mapa centrado en el mundo
m = folium.Map(location=[0, 0], zoom_start=2)

# Paso 3: Crear un diccionario de capas por país
country_groups = df.groupby('country')

# Paso 4: Iterar sobre cada país y agregar una capa por país
for country, group in country_groups:
    # Crear un FeatureGroup para cada país
    feature_group = folium.FeatureGroup(name=country)

    # Agregar un MarkerCluster para mejorar el rendimiento si hay muchos puntos
    marker_cluster = MarkerCluster().add_to(feature_group)

    # Iterar sobre cada jugador del país actual
    for index, row in group.iterrows():
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=f"{row['firstName']} {row['lastName']} - {row['city']}, {row['country']}",
            icon=folium.Icon(color="blue", icon="info-sign")
        ).add_to(marker_cluster)

    # Añadir la capa del país al mapa
    feature_group.add_to(m)

# Paso 5: Añadir control de capas para habilitar/deshabilitar países
folium.LayerControl().add_to(m)

# Paso 6: Guardar el mapa en un archivo HTML
m.save('Players_20242025_WorldMaps.html')
