import requests
from bs4 import BeautifulSoup
import pandas as pd
#https://baloncestoenvivo.feb.es/partido/2417642
# Paso 1: Obtener el contenido HTML (cambia la URL con la página que contiene la tabla)
url = "https://baloncestoenvivo.feb.es/partido/2417642"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Paso 2: Encontrar la tabla correspondiente (ajustar el selector si es necesario)
table = soup.find('table')

# Paso 3: Extraer los encabezados de la tabla
headers = []
for th in table.find_all('th'):
    headers.append(th.get_text().strip())

# Paso 4: Extraer las filas de la tabla, asegurándose que cada fila tenga el mismo número de columnas que los headers
rows = []
for tr in table.find_all('tr'):
    cells = tr.find_all('td')
    if cells:  # Asegurarse de que no sea una fila vacía
        row = [cell.get_text().strip() for cell in cells]
        # Si la fila tiene menos celdas, completamos con valores vacíos
        while len(row) < len(headers):
            row.append('')
        rows.append(row)

# Paso 5: Crear el DataFrame con pandas
if len(headers) == len(rows[0]):
    df = pd.DataFrame(rows, columns=headers)
else:
    df = pd.DataFrame(rows, columns=headers[:len(rows[0])])  # Ajustar la longitud de headers si es mayor

# Paso 6: Mostrar el DataFrame completo
print(df)