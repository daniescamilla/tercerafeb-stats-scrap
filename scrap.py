import requests
from bs4 import BeautifulSoup
import pandas as pd

# Paso 1: Obtener el contenido HTML (cambia la URL con la página que contiene la tabla)
url = str(input('Introduce la URL de la página: '))
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Paso 2: Extraer los nombres de los equipos (asumo que hay dos equipos y se utilizan varios <h1> o similar)
team_names = [h1.get_text().strip() for h1 in soup.find_all('h1', class_='titulo-modulo')]

# Paso 3: Encontrar las tablas correspondientes
tables = soup.find_all('table')

# Función para extraer encabezados y filas de una tabla
def extract_table_data(table):
    # Extraer encabezados del segundo <tr>
    second_tr = table.find_all('tr')[1]  # Selecciona el segundo <tr>
    headers = [th.get_text().strip() for th in second_tr.find_all('th')]

    # Extraer las filas de la tabla
    rows = []
    for tr in table.find_all('tr'):
        cells = tr.find_all('td')
        if cells:  # Asegurarse de que no sea una fila vacía
            row = [cell.get_text().strip() for cell in cells]
            rows.append(row)

    return headers, rows

# Lista para almacenar los DataFrames de ambas tablas
dataframes = []

# Paso 4: Procesar cada tabla y añadir el nombre del equipo antes de cada tabla
for i, table in enumerate(tables):
    # Extraer los encabezados y las filas de la tabla
    headers, rows = extract_table_data(table)

    # Añadir el nombre del equipo a cada fila
    team_column = [team_names[i]] * len(rows)  # Crear una lista con el nombre del equipo repetido para cada fila

    # Añadir la columna del equipo a las filas y actualizar los encabezados
    for row in rows:
        row.insert(0, team_column[0])  # Añadir el nombre del equipo al inicio de cada fila
    headers.insert(0, 'Equipo')  # Añadir "Equipo" como el primer encabezado

    # Crear un DataFrame para la tabla actual
    df = pd.DataFrame(rows, columns=headers)
    
    # Añadir el DataFrame a la lista
    dataframes.append(df)

# Paso 5: Concatenar ambos DataFrames
df_final = pd.concat(dataframes, ignore_index=True)

# Paso 6: Mostrar el DataFrame completo
print(df_final)

# Paso 7: Guardar el DataFrame en un archivo CSV
df_final.to_csv('datos_partido.csv', index=False)
