print("******************")
print("BUSINESS ANALYTICS")
print("******************")

print("***********************************")
print("CONSULTAS INTERACTIVAS - EJERCICIOS")
print("***********************************")

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os 

# Documentación de Pandas https://pandas.pydata.org/pandas-docs/stable/reference/index.html

pd.options.display.min_rows = 6 # por defecto nos muestra 6 registros

# Este análisis consisten en analizar la calidad de datos de un dataset que contiene los accidentes de tráfico en Madrid durante 2020.
# Está en Excel, se llama 2020_Accidentalidad.xlsx.

directorio_actual = os.path.dirname(os.path.abspath(__file__))
ruta_csv = os.path.join(directorio_actual, "2020_Accidentalidad.csv")

# Importa el archivo en el objeto df y visualizalo por pantalla.

df = pd.read_csv(ruta_csv, sep=';', parse_dates=['FECHA'])

print(df.head(2))
df.info()

# Eliminar registros duplicados
df.drop_duplicates(inplace=True)

# Renombrar las columnas
cabecera = ['expediente', 'fecha', 'hora', 'calle', 'numero', 'distrito', 'tipo_accidente', 'tiempo',
            'vehiculo', 'persona', 'edad', 'sexo', 'lesividad', 'unamed1', 'unamed2']

df.columns = cabecera[:len(df.columns)]

df = pd.read_csv(ruta_csv, delimiter=";", 
    header=0, 
    names=cabecera, 
    parse_dates=["fecha"])

df = df.drop("unamed1", axis = 1)
df = df.drop("unamed2", axis = 1)

# Corregir los tipos de datos de las columnas
tipos = {
    'distrito': 'category',
    'tipo_accidente': 'category',
    'tiempo': 'category',
    'vehiculo': 'category',
    'persona': 'category',
    'edad': 'category',
    'sexo': 'category'
}

df = df.astype(tipos)

# Eliminar nulos en 'numero' y 'distrito'
df = df.dropna(subset=['numero', 'distrito'])

# Crear una categoría "Desconocido" para nulos en 'sexo' y 'estado_metereológico'

df["sexo"] = df.sexo.cat.add_categories('Desconocido')
df["tiempo"] = df.tiempo.cat.add_categories('Desconocido')

for column in ['sexo', 'tiempo']:
    df[column].fillna('Desconocido', inplace=True)

# Sustituir nulos en 'lesividad' con cero
df['lesividad'].fillna(0, inplace=True)

# Visualizar el DataFrame resultante
print(df.head())
print(df.info())

# EJERCICIO 1: ¿Cuántos accidentes han ocurrido en total? 12632

# The number of accidents can be determined by counting the unique values of the 'expediente' column.

total_accidentes = df['expediente'].nunique()
print(total_accidentes)

# EJERCICIO 2: ¿Cuántos accidentes han ocurrido en cada distrito?

# Count the number of unique accidents in each district

accidentes_por_distrito = df.drop_duplicates(subset=['expediente']).groupby('distrito').size()
print(accidentes_por_distrito.sort_values(ascending=False))

"""SALAMANCA: 965 accidentes
PUENTE DE VALLECAS: 950 accidentes
CHAMARTÍN: 799 accidentes
CIUDAD LINEAL: 782 accidentes
MONCLOA-ARAVACA: 757 accidentes
CARABANCHEL: 749 accidentes
FUENCARRAL-EL PARDO: 725 accidentes
SAN BLAS-CANILLEJAS: 676 accidentes
CENTRO: 655 accidentes
TETUÁN: 628 accidentes
CHAMBERÍ: 625 accidentes
HORTALEZA: 621 accidentes
LATINA: 579 accidentes
RETIRO: 556 accidentes
ARGANZUELA: 533 accidentes
USERA: 470 accidentes
VILLAVERDE: 372 accidentes
MORATALAZ: 368 accidentes
VILLA DE VALLECAS: 366 accidentes
BARAJAS: 236 accidentes
VICÁLVARO: 220 accidentes"""

# EJERCICIO 3: Saca los 3 distritos en los que hayan ocurrido más accidentes.

# Extract the top 3 districts with the most accidents

top_3_distritos = accidentes_por_distrito.sort_values(ascending=False).head(3)
print(top_3_distritos)

# EJERCICIO 4: Identifica los 3 accidentes más graves(mayor lesividad).

# Extract the top 3 accidents with the highest severity (lesividad)

top_3_accidentes_graves = df.sort_values(by='lesividad', ascending=False).head(3)
print(top_3_accidentes_graves[['expediente', 'fecha', 'hora', 'distrito', 'tipo_accidente', 'lesividad']])

# EJERCICIO 5: Selecciona las variables distrito y tipo_accidente usando filter.

# Select 'distrito' and 'tipo_accidente' columns using the filter method

selected_data = df.filter(items=['distrito', 'tipo_accidente'])
print(selected_data.head())

# EJERCICIO 6: Selecciona todas las variables que sean el 'tipo' de algo.

# Select columns that have names starting with 'tipo_', and also include 'persona' and 'vehiculo'

selected_columns = df.filter(items=['tipo_accidente', 'persona', 'vehiculo'])
print(selected_columns.head())

# EJERCICIO 7: Saca todos los accidentes que hayan ocurrido en RETIRO o en USERA.

# Filter the dataset for accidents that occurred in 'RETIRO' or 'USERA'

accidentes_retiro_usera = df[df['distrito'].isin(['RETIRO', 'USERA'])]
print(accidentes_retiro_usera.head())

# EJERCICIO 8: ¿Cuantos accidentes han ocurrido en cada uno de esos dos distritos?

# Count the number of unique accidents in 'RETIRO' and 'USERA'
accidentes_retiro_usera_count = accidentes_retiro_usera.drop_duplicates(subset=['expediente']).groupby('distrito').size()
print(accidentes_retiro_usera_count)

# EJERCICIO 9: Ahora saca todos los accidentes excepto los que hayan ocurrido en RETIRO o en USERA.

# Filter the dataset for accidents that did NOT occur in 'RETIRO' or 'USERA'

accidentes_excepto_retiro_usera = df[~df['distrito'].isin(['RETIRO', 'USERA'])]
print(accidentes_excepto_retiro_usera.head())

# EJERCICIO 10: Saca todos los accidentes que hayan ocurrido la CASTELLANA.

# Filter the dataset for accidents that occurred on 'CASTELLANA'

accidentes_castellana = df[df['calle'].str.contains('CASTELLANA', case=False, na=False)]
print(accidentes_castellana.head())

# EJERCICIO 11: Identifica todas las formas diferentes en las que de alguna manera está implicada la CASTELLANA (sea como calle, avenida, paseo, cruce con otras calles, etc.

# Identify all unique ways 'CASTELLANA' is mentioned in the 'calle' column

formas_castellana = accidentes_castellana['calle'].unique()
print(formas_castellana)

# EJERCICIO 12: Saca todos los accidentes que hayan tenido una lesivilidad entre 5 y 10.

# Filter the dataset for accidents with lesividad between 5 and 10

accidentes_lesividad = df[(df['lesividad'] >= 5) & (df['lesividad'] <= 10)]
print(accidentes_lesividad.head())

# EJERCICIO 13: Identifica todas las combinaciones que ha habido entre el tipo de vehículo y el tipo de accidente (estilo select distinct)

# Identify all unique combinations of 'vehiculo' and 'tipo_accidente'

combinaciones_vehiculo_accidente = df[['vehiculo', 'tipo_accidente']].drop_duplicates().reset_index(drop=True)
print(combinaciones_vehiculo_accidente)

# EJERCICIO 14: Lo mismo pero ahora saca (como un dataframe) cuantos accidentes ha habido de cada combinación, ordenados de más a menos.

# Count the number of accidents for each combination of 'vehiculo' and 'tipo_accidente'
combinaciones_count = df.groupby(['vehiculo', 'tipo_accidente']).size().reset_index(name='numero_accidentes')

# Sort the results in descending order of the number of accidents
combinaciones_count_sorted = combinaciones_count.sort_values(by='numero_accidentes', ascending=False)

# Display the result using print
print_result = combinaciones_count_sorted.to_string(index=False)
print(print_result)

# EJERCICIO 15: Lo mismo pero ahora sácalo como una tabla cruzada.

# Create a cross tabulation (pivot table) of the number of accidents for each combination of 'vehiculo' and 'tipo_accidente'
crosstab_result = pd.crosstab(df['vehiculo'], df['tipo_accidente'], margins=True, margins_name="Total")

# Displaying the result using the print function
print(crosstab_result)

# La tabla cruzada muestra la cantidad de accidentes para cada combinación de tipo de vehículo ("vehiculo") y tipo de accidente ("tipo_accidente"). 
# Las filas representan los diferentes tipos de vehículos, las columnas representan los diferentes tipos de accidentes, y los valores en la tabla representan el número de accidentes para cada combinación.
# Además, se proporcionan totales para cada fila y columna.

# EJERCICIO 16: Lo mismo pero ahora las celdillas no sean frecuencias si no la lesividad media.
# Y que en las celdillas donde no haya datos en vez de un nulo aparezca un -999

# Create a cross tabulation (pivot table) of the mean lesividad for each combination of 'vehiculo' and 'tipo_accidente'
crosstab_lesividad_mean = df.pivot_table(values='lesividad', index='vehiculo', columns='tipo_accidente', aggfunc='mean', fill_value=-999)

# Displaying the result using the print function
print(crosstab_lesividad_mean)

# EJERCICIO 17: Para cada combinación entre el tipo de vehículo y el tipo de accidente saca el mínimo, la media y el máximo de lesividad.

# Calculate the min, mean, and max lesividad for each combination of 'vehiculo' and 'tipo_accidente'
lesividad_stats = df.groupby(['vehiculo', 'tipo_accidente'])['lesividad'].agg(['min', 'mean', 'max']).reset_index()

# Display the result using the print function
print(lesividad_stats)

# EJERCICIO 18: Saca el número de accidentes y la lesividad media por cada tipo de vehículo. Llámandose 'conteo' y 'media' respectivamente. Y ordenado de mayor a menor primero por conteo y después por media

# Calculate the number of accidents (count) and mean lesividad for each 'vehiculo'
accidents_by_vehiculo = df.groupby('vehiculo')['lesividad'].agg(conteo='count', media='mean')

# Sort the result by 'conteo' and 'media' in descending order
sorted_accidents_by_vehiculo = accidents_by_vehiculo.sort_values(by=['conteo', 'media'], ascending=[False, False])

# Display the result using the print function
print(sorted_accidents_by_vehiculo)

# Por ejemplo, el tipo de vehículo "Turismo" tuvo el mayor número de accidentes (18,258) con una lesividad media de aproximadamente 5.71.

# EJERCICIO 20: Intenta responder a la pregunta de ¿qué tipo de moto es más peligrosa? (pero sobre una base mínima de 300 accidentes). Para ello:

# - Filtra solo registros que contengan la palabra 'moto' en tipo_vehiculo (usa na = False para que no falle, y cuidado con las mayúsculas)

# Filter records containing the word 'moto' in 'vehiculo'
motos_df = df[df['vehiculo'].str.contains('moto', case=False, na=False)]

# - Selecciona sólo los tipos de moto en los que haya habido más de 300 accidentes(para tener suficiente muestra)

# Select only the types of motorcycles with more than 300 accidents
motos_counts = motos_df['vehiculo'].value_counts()
motos_selected = motos_counts[motos_counts > 300].index

# - Calcula la lesividad media

# Calculate the mean lesividad for these selected types
lesividad_motos = motos_df[motos_df['vehiculo'].isin(motos_selected)].groupby('vehiculo')['lesividad'].mean()

# - Ordena en descendente

# Sort in descending order
lesividad_motos_sorted = lesividad_motos.sort_values(ascending=False)

# Display the result using the print function
print(lesividad_motos_sorted)

# Ciclomotor: Lesividad media de aproximadamente 5.26
# Motocicleta > 125cc: Lesividad media de aproximadamente 5.15
# Motocicleta hasta 125cc: Lesividad media de aproximadamente 4.94

# Estos valores indican que, en este conjunto de datos, los ciclomotores tienen la lesividad media más alta, seguidos por las motocicletas de más de 125cc y luego las motocicletas de hasta 125cc.

# EJERCICIO 21: Crea un "cubo" con las siguientes variables

# ['tipo_accidente','estado_metereologico','tipo_vehiculo','tipo_persona','rango_de_edad','sexo','lesividad']
# y que tenga como métricas el número de accidentes la suma de lesividad y la media de lesividad por accidente.

# PISTA: puedes seguir los siguientes pasos:

# - pasa todas las variables citadas a transaccional, excepto lesividad

# Convert all mentioned variables to transactional format, except 'lesividad'
transaccional_df = df.melt(id_vars=['lesividad'], value_vars=['tipo_accidente', 'tiempo', 'vehiculo', 'persona', 'edad', 'sexo'])

# - haz un groupby por variable y value y calcula el conteo y la suma de lesividad

# Group by variable and value, then calculate count and sum of 'lesividad'
cubo = transaccional_df.groupby(['variable', 'value']).agg(conteo=('value', 'size'), suma_lesividad=('lesividad', 'sum'))

# - crea una nueva variable que sea la media como resultado de dividir la suma anterior por el conteo

# Create a new column for the mean of 'lesividad' per accident
cubo['media_lesividad'] = cubo['suma_lesividad'] / cubo['conteo']

# - guárdalo en un objeto llamado cubo

cubo.reset_index(inplace=True)

print(cubo)

# Por ejemplo, para la edad "DE 0 A 5 AÑOS", el número total de registros es de 238, con una lesividad total de 1586 y una lesividad media de aproximadamente 6.66.

# Vemos en el cubo que cuando el estado_metereologico es LLuvia intensa la lesividad media es de 6.76 y ha habido 294 accidentes.
# Comprueba con una consulta sobre los datos iniciales de df que es así.

lluvia_intensa_df_corrected = df[df['tiempo'] == 'LLuvia intensa']

# Calculate the mean lesividad and number of accidents for 'LLuvia intensa'

lluvia_intensa_stats_corrected = lluvia_intensa_df_corrected['lesividad'].agg(['count', 'mean'])
print(lluvia_intensa_stats_corrected)

# EJERCICIO 22: Extrae sobre el cubo las 10 condiciones que provocan accidentes con la mayor lesividad.

# Extract the top 10 conditions from the cubo that lead to the highest mean lesividad
top_lesividad_conditions = cubo.sort_values(by='media_lesividad', ascending=False).head(10)

# Display the result using the print function
print(top_lesividad_conditions)

"""Tiempo: Nevando - Lesividad media: 10.50
Tipo de Accidente: Atropello a persona - Lesividad media: 8.68
Edad: DE 6 A 9 AÑOS - Lesividad media: 7.18
Vehículo: Camión de bomberos - Lesividad media: 7.00
Vehículo: Maquinaria agrícola - Lesividad media: 7.00
Edad: DE 10 A 14 AÑOS - Lesividad media: 6.71
Persona: Pasajero - Lesividad media: 6.68
Edad: DE 0 A 5 AÑOS - Lesividad media: 6.66
Tiempo: LLuvia intensa - Lesividad media: 6.66
Tipo de Accidente: Colisión fronto-lateral - Lesividad media: 6.57"""

# Para una mayor legibilidad elimina el índice de cubo.

# Remove the index from the cubo dataframe for better legibility
cubo.set_index(['variable', 'value'], inplace=True)
cubo.reset_index(inplace=True)

# Display the modified cubo using the print function
print(cubo)

# TÉCNICA PRO:

# Una vez creado un cubo nos puede servir para hacer incluso predicciones sin tener que desarrollar un modelo predictivo, y sin que el escenario concreto a evaluar haya sucedido nunca en el histórico
# De hecho esto es una técnica muy utilizada por ejemplo en el mundo de riesgo con lo que se llaman los "risk scorecards".
# Por ejemplo vamos a usar el cubo para calcular el nivel de lesividad esperado en un accidente que se produzca cuando está nevando, siendo la persona un niño de 10 a 14 años conduciendo un ciclomotor.

# Haz una consulta sobre df para comprobar que no tenemos historia de ningún accidente con esas características.

# Check the original dataframe to see if there's any record with the mentioned characteristics

accidente_nevando_niño_ciclomotor = df[(df['tiempo'] == 'Nevando') & 
                                      (df['edad'] == 'DE 10 A 14 AÑOS') & 
                                      (df['vehiculo'] == 'Ciclomotor')]

print(accidente_nevando_niño_ciclomotor)

# EJERCICIO 23: Ahora usa el cubo como un scorecard para calcular la lesividad estimada para este accidente.

# PISTA: puedes hacer el siguiente proceso:

# PASO1: filtra los registros en los que las condiciones del escenario están en la columna value

selected_conditions = ['Nevando', 'DE 10 A 14 AÑOS', 'Ciclomotor']
filtered_cubo = cubo[cubo['value'].isin(selected_conditions)]

# PASO2: calcula la media de la lesividad

estimated_lesividad = filtered_cubo['media_lesividad'].mean()
print(estimated_lesividad)

# Ahora vamos a utilizar el método query en los siguientes ejercicios

print(df)

# EJERCICIO 24: Haz una consulta para extraer sólo los accidentes de ciclomotores en Usera.

# Use the query method to extract accidents involving ciclomotors in Usera
ciclomotores_usera = df.query("vehiculo == 'Ciclomotor' and distrito == 'USERA'")
print(ciclomotores_usera)

# EJERCICIO 25: Haz una consulta para extraer sólo los accidentes de ciclomotores en Usera con lesividad menor que 5.

# Use the query method to extract accidents involving ciclomotors in Usera with lesividad less than 5
ciclomotores_usera_lesividad_menor_5 = df.query("vehiculo == 'Ciclomotor' and distrito == 'USERA' and lesividad < 5")
print(ciclomotores_usera_lesividad_menor_5)

# EJERCICIO 26: Haz una consulta para extraer los registros con lesividad entre 5 y 8.

# Use the query method to extract records with lesividad between 5 and 8
lesividad_5_to_8 = df.query("5 <= lesividad <= 8")
print(lesividad_5_to_8)

# EJERCICIO 27: Haz una consulta para extraer los accidentes de 'MONCLOA-ARAVACA' o 'FUENCARRAL-EL PARDO'

# Use the query method to extract accidents in 'MONCLOA-ARAVACA' or 'FUENCARRAL-EL PARDO'
accidentes_selected_distritos = df.query("distrito == 'MONCLOA-ARAVACA' or distrito == 'FUENCARRAL-EL PARDO'")
print(accidentes_selected_distritos)

# EJERCICIO 28: Haz una consulta para extraer los accidentes que NO sean de 'MONCLOA-ARAVACA' o 'FUENCARRAL-EL PARDO'

# Use the query method to extract accidents NOT in 'MONCLOA-ARAVACA' or 'FUENCARRAL-EL PARDO'
accidentes_other_distritos = df.query("distrito != 'MONCLOA-ARAVACA' and distrito != 'FUENCARRAL-EL PARDO'")
print(accidentes_other_distritos)

# EJERCICIO 29: Crea una variable llamada lesividad_media y crea una consulta para seleccionar solo los accidentes cuya lesividad sea inferior a la lesividad media.

lesividad_media = df['lesividad'].mean()

# Use the query method to extract accidents with lesividad below the mean lesividad, using the value directly
accidentes_below_mean_lesividad = df.query(f"lesividad < {lesividad_media}")
print(accidentes_below_mean_lesividad)

# EJERCICIO 30: Sobre la consulta anterior haz que muestre solo las variables tipo_accidente y lesividad.

# Extract only 'tipo_accidente' and 'lesividad' columns from the previous result using the query method
selected_columns_accidentes = accidentes_below_mean_lesividad[['tipo_accidente', 'lesividad']]
print(selected_columns_accidentes)












