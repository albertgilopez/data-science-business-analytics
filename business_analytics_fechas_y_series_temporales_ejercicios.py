print("******************")
print("BUSINESS ANALYTICS")
print("******************")

print("***************************************")
print("FECHAS Y SERIES TEMPORALES - EJERCICIOS")
print("***************************************")

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os 

# %matplotlib inline. Es para decirle cómo tiene que sacar los gráficos.
# En este caso significa que los saque como gráficos estáticos integrados en el propio notebook (de tal forma que se guarde y distribuya más fácilmente).

pd.options.display.min_rows = 6

# Ruta al archivo CSV
path = 'Historico_IBEX35_Diario.csv' # Ajusta esta ruta según la ubicación de tu archivo

# Leyendo el archivo CSV sin ninguna limpieza para entender la estructura
raw_df = pd.read_csv(path, na_values='-', thousands='.', decimal=',')

# Renombrando las columnas especificadas para que coincidan con el código original
df = raw_df.rename(columns={'Vol.': 'vol', '% var.': 'var'})

# Limpiando la columna 'vol'
df['vol'] = df['vol'].str.replace(',', '.').str.replace('M', '').astype('float')

# Limpiando la columna 'var'
df['var'] = df['var'].str.replace(',', '.').str.replace('%', '').astype('float')

# Mostrando las primeras filas del DataFrame limpio
print(df.head())

# EJERCICIO 1: Comprueba si el tipo de la variable fecha ya es un datetime64.

fecha_data_type = df['Fecha'].dtype
print(fecha_data_type)

# EJERCICIO 2: Convierte fecha a datetime y muestra df. ¿Ves algo raro en la fecha?

# Converting the 'Fecha' column to datetime

# Parece que hay un problema con la conversión de la columna 'Fecha' a datetime. 
# El error "day is out of range for month" sugiere que el formato que hemos especificado no coincide con la estructura real de las fechas en la columna.

# La columna 'Fecha' tiene un formato de fecha en el que los primeros cuatro dígitos representan el año, seguidos de dos dígitos para el mes y dos dígitos para el día.
# Podemos ajustar el formato para reflejar esta estructura y volver a intentar la conversión.

# Examining unique values in the 'Fecha' column to identify any unusual patterns
unique_fecha_values = df['Fecha'].unique()
unique_fecha_values[:10]

# La inspección de los valores únicos en la columna de fecha revela el problema: algunas fechas tienen un dígito menos porque el día o el mes se representa con un solo dígito en lugar de dos (por ejemplo, 9122019 en lugar de 09122019).
# Después de revisar los valores de la fecha, parece que el formato real es DDMMAAAA (por ejemplo, 9122019 para el 9 de diciembre de 2019), no AAAAMMDD como asumimos inicialmente.

# Converting the 'Fecha' column to string and ensuring 8 characters by padding with zeros
df['Fecha'] = df['Fecha'].astype(str).str.zfill(8)

# Converting the 'Fecha' column to datetime using the correct format (DDMMYYYY)
df['Fecha'] = pd.to_datetime(df['Fecha'], format='%d%m%Y')

# Showing the first few rows of the DataFrame with the corrected 'Fecha' column
print(df.head())

# EJERCICIO 3: Convierte fecha al índice y saca df por pantalla.

df.set_index('Fecha', inplace=True)
print(df.head())

# EJERCICIO 4: Ordena por el índice de más antiguo a más reciente, saca por pantalla los 10 primeros registros y fíjate en la secuencia de la fecha ¿ves algo raro?

df_sorted = df.sort_index(ascending=True)
first_10_records = df_sorted.head(10)
print(first_10_records)

# EJERCICIO 5: Crea un nuevo dataframe llamado df_reg regularizando df para que tenga todos los días.
# Lo más sensato es que los datos de sabados, domingos y festivos sean los mismos que los del día anterior.
# Muestra por pantalla los 10 primeros resultados de df_reg.

df_reg = df_sorted.resample('D').ffill()
print(df_reg.head(10))

# EJERCICIO 6: Añade el mes a df como una variable llamada 'mes'

df_reg['mes'] = df_reg.index.month
print(df_reg.head())

# EJERCICIO 7: Añade el día a df como una variable llamada 'dia'

df_reg['dia'] = df_reg.index.day
print(df_reg.head())

# EJERCICIO 8: Añade el día de las semana a df (en nombre en inglés) como una variable llamada 'dia_semana'.

df_reg['dia_semana'] = df_reg.index.day_name()
print(df_reg.head())

# EJECICIO 9: Ahora que ya tenemos nuestro dataset ampliado con nuevas variables vamos a hacer algunas consultas.
# Comienza por sacar los datos de un día concreto, por ejemplo el 23 de septiembre. Hazlo usando el index.

specific_date_data = df_reg.loc['2019-09-23']
print(specific_date_data)

# EJERCICIO 10: Saca solo los datos de septiembre de 2019.

september_2019_data = df_reg.loc['2019-09']
print(september_2019_data.head())

# EJERCICIO 11: Saca solo los datos de cierre de cada viernes (variable 'ultimo' de cada viernes).

friday_closing_data = df_reg[df_reg['dia_semana'] == 'Friday']['Último']
print(friday_closing_data.head())

# EJERCICIO 12: Vemos que en esta nueva serie de los viernes hay algunos que están en nulos. Interpólalos.

friday_closing_data_interpolated = friday_closing_data.interpolate()
print(friday_closing_data_interpolated.head())

# EJERCICIO 13: import matplotlib.pyplot as plt

plt.style.use('fivethirtyeight')
plt.figure(figsize=(12, 6))
plt.plot(friday_closing_data_interpolated, marker='o', linestyle='-', color='blue')
plt.title('Datos de Cierre de Cada Viernes (Interpolados)')
plt.xlabel('Fecha')
plt.ylabel('Último')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# EJERCICIO 14: ¿Cual ha sido el último dato de volumen gestionado en cada trimestre?
# PISTA: recuerda usar solo los días laborables, si no aparecerán nulos.

business_days_data = df_reg[df_reg['dia_semana'].isin(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'])]
last_volume_per_quarter = business_days_data['vol'].resample('Q').last()
print(last_volume_per_quarter)

# EJERCICIO 15: ¿Hay diferencias en la variación ('var') según el día de la semana que sea?

# PISTAS:

# - Nos da igual que la variación sea en positivo o negativo, así que haz el valor absoluto de los datos antes de hacer la media
# - Puedes usar un apply que llame a una función que haga lo dicho en el punto anterior.

# Para analizar las diferencias en la variación ('var') según el día de la semana, podemos calcular la media del valor absoluto de la variación para cada día de la semana.
# Esto nos dará una idea de la magnitud promedio de la variación, independientemente de si es positiva o negativa.

# - Tomar el valor absoluto de la columna 'var'.
df_reg['var_abs'] = df_reg['var'].abs()

# - Agrupar los datos por el día de la semana usando groupby.
variation_by_day_of_week = df_reg.groupby('dia_semana')['var_abs'].mean()

# - Calcular la media de la variación absoluta para cada día de la semana.
print(variation_by_day_of_week)

# EJERCICIO 16: Saca la media del volumen gestionado ('vol') entre los días 7 de Julio y 28 de Julio.

july_7_to_28_data = df_reg['2019-07-07':'2019-07-28']
mean_volume_july_7_to_28 = july_7_to_28_data['vol'].mean()
print(mean_volume_july_7_to_28)

# EJERCICIO 17: Crea un nuevo dataset llamado df_w en el que trabajes a nivel semanal, siendo la función de agregación la media de las semana en cada una de las variables (excepto mes y dia). Muéstra por pantalla los 10 primeros registros.

# Resampling the DataFrame to a weekly frequency and calculating the mean for each week
# Excluding the 'mes' and 'dia' columns from the aggregation

# df_w = df_reg.drop(columns=['mes', 'dia']).resample('W').mean()
# print(df_w.head(10))

# EJERCICIO 18: Cambia las etiquetas al dataset anterior para que se vea claro que los datos son semanales.

# Resampling the DataFrame to a weekly frequency using kind='period'
# Calculating the mean for each week, excluding the 'mes', 'dia', and 'var_abs' columns

# df_w = df_reg.drop(columns=['mes', 'dia', 'var_abs']).resample('W', kind='period').mean()
# df_w.head(10)

# EJERCICIO 19: Saca un gráfico del cierre diario (variable 'ultimo' de df).

plt.figure(figsize=(12, 6))
plt.plot(df_reg['Último'], marker='', linestyle='-', color='blue')
plt.title('Datos de Cierre Diario')
plt.xlabel('Fecha')
plt.ylabel('Último')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# EJERCICIO 20: Crea una nueva variable en df llamada ultimo_mm_5 que sea la media móvil no ponderada de 5 elementos de la variable 'ultimo'. Muestra los 10 primeros registros de df.

df_reg['ultimo_mm_5'] = df_reg['Último'].rolling(window=5).mean()
print(df_reg.head(10))

# EJERCICIO 21: Crea una nueva variable en df llamada ultimo_mm_5_pond que sea la media móvil ponderada de 5 elementos de la variable 'ultimo'.
# Donde los pesos del dato más reciente al más lejano sean: 40%, 30%, 20%, 7%, 3%. Muestra los 10 primeros registros de df.

weights = [0.40, 0.30, 0.20, 0.07, 0.03]
df_reg['ultimo_mm_5_pond'] = df_reg['Último'].rolling(window=5).apply(lambda x: (x * weights).sum())
print(df_reg.head(10))

# EJERCICIO 22: Representa gráficamente:

# - ultimo en azul
# - ultimo_mm_5 en rojo
# ultimo_mm_5_pond en amarillo

# NOTAS: Previamente elimina todos los nulos del dataframe. Usa un figsize = (16,8)

# Removing all rows with null values from the DataFrame
df_reg_non_null = df_reg.dropna()

# Plotting the 'Último', 'ultimo_mm_5', and 'ultimo_mm_5_pond' series
plt.figure(figsize=(16, 8))
plt.plot(df_reg_non_null['Último'], color='blue', label='Último')
plt.plot(df_reg_non_null['ultimo_mm_5'], color='red', label='ultimo_mm_5 (Media Móvil 5)')
plt.plot(df_reg_non_null['ultimo_mm_5_pond'], color='yellow', label='ultimo_mm_5_pond (Media Móvil Ponderada 5)')
plt.title('Comparación de Datos de Cierre y Medias Móviles')
plt.xlabel('Fecha')
plt.ylabel('Valor')
plt.grid(True)
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# El gráfico muestra claramente cómo las medias móviles suavizan la serie temporal original, con la media móvil ponderada dando más peso a los datos más recientes.

# EJERCICIO 23: Como no se ve muy bien selecciona solo los datos de marzo y repite el gráfico.

# Filtering the DataFrame to include only the data for March
march_data = df_reg_non_null[df_reg_non_null.index.month == 3]

# Plotting the 'Último', 'ultimo_mm_5', and 'ultimo_mm_5_pond' series for March
plt.figure(figsize=(16, 8))
plt.plot(march_data['Último'], color='blue', label='Último')
plt.plot(march_data['ultimo_mm_5'], color='red', label='ultimo_mm_5 (Media Móvil 5)')
plt.plot(march_data['ultimo_mm_5_pond'], color='yellow', label='ultimo_mm_5_pond (Media Móvil Ponderada 5)')
plt.title('Comparación de Datos de Cierre y Medias Móviles (Marzo)')
plt.xlabel('Fecha')
plt.ylabel('Valor')
plt.grid(True)
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


