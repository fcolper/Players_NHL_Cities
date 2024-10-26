import pandas as pd
import time
from geopy.geocoders import Nominatim
from opencage.geocoder import OpenCageGeocode
import pandas as pd
import time

# Cargar los datos
df = pd.read_csv('Data_csv/Players_20242025_Cities_Countries.csv')

country_dict = {
    'CAN': 'Canada',
    'USA': 'United States',
    'SWE': 'Sweden',
    'RUS': 'Russia',
    'FIN': 'Finland',
    'CZE': 'Czech Republic',
    'SVK': 'Slovakia',
    'SUI': 'Switzerland',
    'GER': 'Germany',
    'LAT': 'Latvia',
    'BLR': 'Belarus',
    'DEN': 'Denmark',
    'UKR': 'Ukraine',
    'NOR': 'Norway',
    'AUT': 'Austria',
    'GBR': 'United Kingdom',
    'KAZ': 'Kazakhstan',
    'FRA': 'France',
    'POL': 'Poland',
    'LTU': 'Lithuania',
    '{}': None,  # Reemplaza si sabes a qué país corresponde o trata los datos faltantes
    'BEL': 'Belgium',
    'ITA': 'Italy',
    'SLO': 'Slovenia',
    'JPN': 'Japan',
    'CRO': 'Croatia',
    'BAH': 'Bahamas',
    'KOR': 'South Korea',
    'NGR': 'Nigeria',
    'BRA': 'Brazil',
    'RSA': 'South Africa',
    'BRU': 'Brunei',
    'IDN': 'Indonesia',
    'EST': 'Estonia',
    'TAN': 'Tanzania',
    'NED': 'Netherlands',
    'AUS': 'Australia',
    'UZB': 'Uzbekistan',
    'BUL': 'Bulgaria'
}

# Reemplaza con tu clave API de OpenCage
key = 'd699b07e72bf4cfebf9ff376a57ee69c'
geocoder = OpenCageGeocode(key)

# Función para obtener latitud y longitud con OpenCage, considerando tanto ciudad como país
def get_lat_lon_opencage(row):
    country_full = country_dict.get(row['country'], row['country'])  # Convertir abreviación a nombre completo
    query = f"{row['city']}, {country_full}"  # Asegurarte de incluir tanto ciudad como país completo
    results = geocoder.geocode(query)
    if results and len(results):
        return pd.Series([results[0]['geometry']['lat'], results[0]['geometry']['lng']])
    else:
        return pd.Series([None, None])

# Aplicar la función a cada fila
df[['latitude', 'longitude']] = df.apply(get_lat_lon_opencage, axis=1)

# Agregar un pequeño delay entre consultas para evitar sobrecarga en el servicio
time.sleep(1)

df=df.drop_duplicates(subset=['id'])
df=df.drop(columns=['Unnamed: 0_x','Unnamed: 0_y'])
df.sort_values(by=['id'], inplace=True)

df.to_csv(f'Data_csv/Players_20242025_Cities_Countries.csv', index=False)