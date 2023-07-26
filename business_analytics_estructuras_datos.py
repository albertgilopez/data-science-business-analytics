print("******************")
print("BUSINESS ANALYTICS")
print("******************")

print("*********************************")
print("ESTRUCTURAS DE DATOS PARA NEGOCIO")
print("*********************************")

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# %matplotlib inline. Es para decirle cómo tiene que sacar los gráficos.
# En este caso significa que los saque como gráficos estáticos integrados en el propio notebook (de tal forma que se guarde y distribuya más fácilmente).

pd.options.display.min_rows = 6

df = pd.read_csv('../../00_DATASETS/DataSetKivaCreditScoring.csv', sep = ';', index_col = 'id',
                parse_dates = ['Funded Date','Paid Date'])
print(df)
print(df.head())
print(df.info())

# CAMBIAR LA ESTRUCTURA DEL DATAFRAME

# Hay dos grandes formas de organizar la información: a lo ancho o a lo largo (y con sus escenarios intermedios).
# A lo ancho también se le llama formato tabular, y a lo largo también se llama formato transaccional.

# En Pandas tenemos dos funciones para pivotar entre estos dos tipos de estructuras:

# - melt: pasar de ancho a largo
# - pivot: pasar de largo a ancho

# No confundir con stack y unstack, que hacen algo parecido, pero los usábamos para mover los índex y columns, pero no para la estructura general de la tabla que es lo que vamos a hacer ahora.

# Cogemos solo 4 variables

red = df[['Funded Date','Country','Sector','Funded Amount']].copy()

# Simplificamos la fecha quitándole la parte de la hora
red['Funded Date'] = red['Funded Date'].dt.date

# Pasamos el indice a una variable para estudiar el comportamiento de las transformaciones
red.reset_index(inplace = True)

print(red.head())
print(red.info())

# DE ANCHO A LARGO

# melt(): https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.melt.html

# Pasaremos información que actualmente tenemos como columnas a registros.
# De tal forma que creará una nueva columna llamada "variable" donde meterá los nombres de las antiguas columnas que estamos pivotando, y otra nueva columna llamada "value" donde meterá el valor de la antigua columna en cada registro.

# Si queremos dejar alguna columna sin pivotar lo hacemos con el parámetro id_vars.

# Parámetros más importantes:

# - id_vars: son las variables que dejaremos sin pivotar (y por tanto es posible que se repitan a nivel de registros)
# - value_vars: son las variables que queremos pasar de columnas a filas
# - var_name: nombre a usar para la columna variables
# - value_name: nombre a usar para la columna valores

# Recordamos la dimensión inicial de red
print(red.shape)

# Vamos a empezar con el caso más sencillo. Pasar una sola columna a registros.
# Vemos que crea la estructura de variable y valor y que en este caso sigue manteniendo el mismo número de registros que teníamos.

print(red.melt(value_vars = 'Country'))

# Hacemos lo mismo pero dejamos el id como variable identificador, es decir, sin pivotar

print(red.melt(id_vars = 'id',
         value_vars = 'Country'))

# Ahora vamos a pivotar tanto Country como Sector y comprobamos:

# - como se ha duplicado el número de registros
# - que la variable duplicada es el id que habiamos puesto como identificador

# Por ejemplo, el registro 84 se ha convertido en dos registros, uno para recoger el country y otro para recoger el sector

# Ordenar no es necesario, lo hacemos para ver el efecto de que id se duplica

print(red.melt(id_vars = 'id',
         value_vars = ['Country','Sector']).sort_values('id'))

# Ahora vamos a mantener el id, la fecha y el importe y pivotar pais y sector
# Ordenar no es necesario, lo hacemos para ver el efecto de que id se duplica

print(red.melt(id_vars = ['id','Funded Date','Funded Amount'],
         value_vars = ['Country','Sector']).sort_values('id'))

# Por último vamos a llegar a la máxima estructura de pivotado de este dataset manteniendo solo el id como identificador.
# Vemos como el número de registros originales se ha multiplicado por 4 (porque estamos pivotando 4 variables).
# En este caso vamos a guardarlo en un nuevo dataframe para que nos sirva de partida para la siguiente sección.

largo = red.melt(id_vars = 'id',
         value_vars = ['Funded Date','Funded Amount','Country','Sector']).sort_values('id')

print(largo)

# DE LARGO A ANCHO

# pivot(): https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.pivot.html

# Lo usarmos cuando tenemos valores dentro de una variable y queremos que cada uno de esos valores pase a ser una nueva columna (por tanto reducirmos registros y crecemos en columnas).

# Parámetros más importantes:

# - index: la variable que se usará como índice (es importante para integrar bien las columnas en los nuevos registros)
# - columns: la columna actual que será la fuente de las nuevas columnas
# - values: la columna actual que será la fuente de los nuevos valores de las celdas

print(largo)

# Nos fijamos en que tenemos 20584 filas.
# Obviamente la variable identificadora que debería funcionar como index es 'id'.
# La columna que recoge los nombres de las futuras columnas es 'variable'.
# Y la columna que recoge sus respectivos datos es value.

print(largo.pivot(index = 'id',
           columns = 'variable',
           values = 'value'))


# CAMBIAR EL NIVEL DEL DATAFRAME

# En entornos empresariales es muy común que exita información a diferentes niveles.
# Por ejemplo cliente-producto, grupo-empresa, cliente-póliza, pedido-producto, etc.

# Siempre es muy importante tener claro el nivel de análisis al que se quiere trabajar.
# Y a veces habrá que agregar para tener ese nivel de análisis.
# Por ejemplo si quisiéramos trabajar a nivel de cliente pero tuviéramos las tablas a nivel de póliza tendríamos que agregar.

# Hay que aplicar diferentes técnicas según el tipo de cada variable:

# - Primero dummificar las categóricas como nuevas variables
# - Luego agregar los conteos y las variables continuas con alguna función de agregación: media, suma total, etc.

# En nuestro caso vamos a suponer que queremos analizar la financiación por países.
# Por sencillez vamos a usar solo 2 continuas, y 2 categóricas para demostrarlo (más el país claro)

# Creamos una versión reducida simplemente por simplicidad de la explicación

df2 = df.loc[:,['Country','Funded Amount','Loan Amount','Sector','Delinquent']].copy()
print(df2)

# Con las contínuas no tenemos problemas, porque simplemente usando una función de agregación (normalmente suma o media) ya podremos subir el nivel.
# Pero las categorías necisitamos dummificarlas antes para poder agregarlas.

# Dummificamos las categóricas

df2 = pd.get_dummies(df2,columns = ['Sector','Delinquent'])
print(df2)

# Agregar por país

print(df2.groupby('Country').sum())


