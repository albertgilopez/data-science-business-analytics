print("******************")
print("BUSINESS ANALYTICS")
print("******************")

print("********************************")
print("CREACIÓN DE VARIABLES DE NEGOCIO")
print("********************************")

# En este módulo vamos a aprender las 11 técnicas más importantes con las que podremos crear diferentes variables de interés para el negocio.
# Con ellas aprovecharemos la información que existe en el dataset pero le daremos una forma que suele tener importancia prácticamente en cualquie negocio como incrementos, rankings, etc.

# En ocasiones se llama a estas variables "sintéticas", ya que no existían como tal en el dataset original.
# En proyectos reales este tipo de técnicas son muy potentes, ya que permiten aportar nueva luz al negocio que estaba en los datos, pero hasta este momento era desconocida.

# CREACIÓN DE VARIABLES DE NEGOCIO

# - Apply y Transform
# - Agregación Horizontal
# - Discretizar
# - Condiciones Simples
# - Condiciones Múltiples
# - Acumulados
# - Incrementos
# - Lags
# - Rankings
# - Pareto
# - Dummies

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# %matplotlib inline. Es para decirle cómo tiene que sacar los gráficos.
# En este caso significa que los saque como gráficos estáticos integrados en el propio notebook (de tal forma que se guarde y distribuya más fácilmente).

pd.options.display.min_rows = 6

df = pd.read_csv('../00_DATASETS/DataSetKivaCreditScoring.csv', sep = ';', index_col = 'id',
                parse_dates = ['Funded Date','Paid Date'])
print(df)
print(df.head())
print(df.info())

# CREAR O TRANSFORMAR VARIABLES A PARTIR DE OTRAS

# Hay varias formas de hacer esto en Pandas, y a veces hacen lo mismo, por lo que es un poco confuso.

# Principalmente usaremos:

# - Cálculos directos
# - apply()
# - transform()

# CÁLCULOS DIRECTOS

# Cuando querramos crear unas variables a partir de otras, en la mayoría de los casos, simplemente las podremos construir usando operaciones aritméticas básicas.

# Por ejemplo vamos a crear una nueva variable que nos indique qué parte de la financiación adicional ya ha sido devuelta.

df['Devuelto'] =  df['Paid Amount'] / df['Funded Amount'] * 100
print(df["Devuelto"])

# apply()

# Implementa la técnica conocida como: split-apply-combine, que básicamente consiste en dividir el objeto original por algún iterable, aplicar una función a cada elemento, y después volver a combinar todos los elementos en un único dataframe.
# Y todo esto de forma automática para el usuario. Es importante entender este principio general porque después podemos aplicarlo en muchos casos diferentes.

# Por ejemplo si el objeto original es un Series, entonces los iterables serán cada uno de los valores, así que apply irá ejecutando la función sobre cada uno de ellos y al final nos devolverá de nuevo toda la nueva Serie como un único objeto.
# Pero si el objeto original fuera un dataset (y lo recorremos por columnas), cada objeto iterable sería una columna, sobre la que apply ejecutaría la función, y nos devolvería de nuevo todo el resultado integrado.

# Como función en apply() podemos usar alguna nativa de Python o de algún paquete, alguna definida por nosotros o incluso funciones lambda, no hace inplace.

# https://pandas.pydata.org/docs/reference/api/pandas.Series.apply.html
# https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.apply.html

def a_euros(importe):
    return(importe/1.16)

print(df['Loan Amount'].apply(a_euros).head(3))
print(df['Loan Amount'].apply(lambda x: x/1.16).head(3))

# Aquí hemos usado apply sobre una variable (Series).
# Pero también podríamos usar la versión sobre dataframes, especificando el eje sobre el que trabajar.
# Por ejemplo, si ponemos axis = 1 entonces estaremos trabajando a nivel de registro en vez de columna.

# Calculamos una nueva variable como la media del mismo registro en otras variables

def media_importes(registro):
    return(sum(registro)/len(registro))

print(df[['Loan Amount','Funded Amount','Paid Amount']].apply(media_importes,axis=1).head(3))

# Un punto diferencial de apply es que además de poder usar funciones que devuelven el mismo número de elementos que toman, también puede usar funciones que devuelven agregados.

# Por ejemplo vamos a seleccionar un par de variables numéricas y calcular la suma total de cada una.

print(df[['Loan Amount','Funded Amount']].apply(sum,axis=0))

# También podemos usar la agregación de columnas, en lugar de registros.
# Es frecuente por ejemplo para hacermedias de ventanas temporales, p.e. tenemos ventas_Enero, ventas_Febrero y ventas_Marzo, y creamos una variable Venta_media_Q1.

# Con nuestros datos vamos a hacer la media de las 3 variables de financiación.

df['Media Financiacion'] = df[['Funded Amount','Loan Amount','Paid Amount']].apply(lambda fila: fila.mean(), axis = 1)
print(df)

# AGREGACIÓN HORIZONTAL

# Para operaciones estandar (suma, media, multiplicación, etc.) existe una forma más sencilla de hacer lo que en el ejercicio anterior hicimos con apply y axis = 1.
# Simplemente usando el método de la operación pero especificándole axis = 1.

# Es una manera muy útil para crear nuevas variables de negocio en ciertos contextos a partir de otras variables que sean comparables, por ejemplo:

# - Si tenemos las ventas de diferentes productos en columnas y queremos calcular las ventas totales de cada cliente
# - Si tenemos mediciones de temperaturas en columnas y queremos calcular la temperatura máxima del registro
# - Si tenemos valoraciones de diferentes productos en columnas y queremos aplicar la desviación típica para localizar a clientes que varíen poco frente a los que siempre dan unos o cincos a todo

print(df[['Funded Amount','Loan Amount','Paid Amount']])

print(df[['Funded Amount','Loan Amount','Paid Amount']].sum(axis = 1)) # suma horizontal
print(df[['Funded Amount','Loan Amount','Paid Amount']].max(axis = 1)) # máximo horizontal
print(df[['Funded Amount','Loan Amount','Paid Amount']].min(axis = 1)) # mínimo horizontal
print(df[['Funded Amount','Loan Amount','Paid Amount']].std(axis = 1)) # desviación típica horizontal

# transform()

# Lo mismo que hemos hecho con apply podemos hacerlo con transform. Incluso con las funciones lambda. No hace inplace.

# https://pandas.pydata.org/docs/reference/api/pandas.Series.transform.html

def a_euros(importe):
    return(importe/1.16)

print(df['Loan Amount'].transform(a_euros).head(3))

# Vemos que la salida es la misma que con apply(). Entonces ¿en qué se diferencian?

# - A transform podemos pasarle un diccionario de variables y funciones. A apply no. Por tanto transform es mejor cuando queremos hacer varios cambios simultáneos
# - Apply permite generar un output agregado. Transform no, ya que tiene que devolver el mismo número de elementos que toma. Por tanto apply es mejor si queremos hacer agregados

# Ejemplo de aplicar un diccionario de transformaciones con transform (que no funcionaría con apply)

trans_dict = {'Funded Amount': np.exp,
             'Loan Amount': np.sqrt}

print(df.transform(trans_dict)) 

# Ejemplo de obtener un output agregado con apply (que no funcionaría con transform)

print(df.select_dtypes('int64').apply(sum))
# print(df.select_dtypes('int64').transform(sum)) # esta línea da error

# DISCRETIZAR

# Discretizar es el proceso mediante el que transformamos una variable cuantitativa a una variable categórica, normalmente ordinal.

# Un ejemplo típico es pasar la variable edad a tramos de edad. Tenemos varias alternativas:

# - Pasarle los cortes que queremos usar
# - Pasarle el número de tramos que queremos obtener e intentará crearlos de un tamaño similar
# - Pasarle los percentiles en los que queremos que corte.

# A nivel de funciones usaremos pd.cut() y pd.qcut()

# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.cut.html
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.qcut.html

print(df)
df['Funded Amount'].plot.hist();
# plt.show()

# DISCRETIZACIÓN AUTOMÁTICA PASÁNDOLE LOS CORTES

cortes = [500,1000,1500] # definimos los cortes en una lista

df['Funded Amount Disc Cortes'] = pd.cut(df['Funded Amount'],cortes) # discretizamos

df['Funded Amount Disc Cortes'].value_counts().sort_index().plot.bar(); # revisamos
# plt.show()

# Nos fijamos en que los límites inferiores y superiores son los que nosotros le decimos.
# Pero en la práctica solemos querer dejarlos abiertos, porque no sabemos qué valores nos podrán estar entrando en esa variable en el futuro.
# Así que podemos usar -float("inf") y float("inf") para incluir los extremos abiertos.

cortes = [-float("inf"), 500, 1000, 1500, float("inf")] # definimos los cortes en una lista

df['Funded Amount Disc Cortes'] = pd.cut(df['Funded Amount'],cortes) # discretizamos

df['Funded Amount Disc Cortes'].value_counts().sort_index().plot.bar(); # revisamos
# plt.show()

# En ocasiones querremos personalizar los nombres de las categorías resultantes.
# Lo hacemos pasándole una lista con los nombres deseados al parámetro labels.

cortes = [-float("inf"), 500, 1000, 1500, float("inf")]
nombres = ['00_Menos de 500', 
           '01_Entre 500 y 1000', 
           '02_Entre 1000 y 1500',
           '03_Más de 1500']

df['Funded Amount Disc Cortes'] = pd.cut(df['Funded Amount'],cortes, labels = nombres)

df['Funded Amount Disc Cortes'].value_counts().sort_index().plot.bar();
# plt.show()

# Notar que no está cambiando los nombres en el gráfico, si no que los ha escrito así directamente en dataframe al crear la variable.
print(df['Funded Amount Disc Cortes'])

# DISCRETIZACIÓN AUTOMÁTICA PASÁNDOLE EL NÚMERO DE INTERVALOS

# Si en lugar de pasar la lista con los cortes le pasamos el número de intervalos deseados los creará de un rango de intervalo similar (pero no similar en cuanto al número de registros en cada tramo).
# Notar que aquí usa como límites inferior y superior el mínimo y máximo que exista en los datos, con el potencial riesgo en los futuros valores que habíamos comentado.

df['Funded Amount Disc Cortes'] = pd.cut(df['Funded Amount'],4)
df['Funded Amount Disc Cortes'].value_counts().sort_index().plot.bar();
# plt.show()

# DISCRETIACIÓN AUTOMÁTICA PASÁNDOLE LOS PERCENTILES DE CORTE

# Si en lugar de pasar la lista con los cortes le pasamos el número de intervalos deseados los creará de un tamaño similar (en cuanto al número de registros en cada tramo)
# Notar que aquí usa como límites inferior y superior el mínimo y máximo que exista en los datos, con el potencial riesgo en los futuros valores que habíamos comentado.

cortes = [0, 0.25, 0.5, 0.75, 1]

df['Funded Amount Disc Cortes'] = pd.qcut(df['Funded Amount'],cortes)
df['Funded Amount Disc Cortes'].value_counts().sort_index().plot.bar();
# plt.show()

# CREAR VARIABLES A PARTIR DE CONDICIONES SIMPLES

# Llamamos condición simple a que la variable tome un valor si se cumple una condición y otro si no se cumple.
# Un caso típico es la creación de indicadores, donde el indicador toma el valor 1 si se cumple y 0 si no.
# Una forma sencilla de hacerlo es usando np.where(condición, valor si cierto, valor si falso)

# Por ejemplo vamos a crear un indicador que tome 1 si la cantidad financiada es superior a 1000.

df['Indicador'] = np.where(df['Funded Amount'] > 1000, 1, 0)
print(df)

# Otra forma de hacerlo con Pandas es usar apply + funcióin lambda + if

df['Indicador2'] = df['Funded Amount'].apply(lambda x: 1 if x > 1000 else 0)
print(df)

# CREAR VARIABLES A PARTIR DE CONDICIONES MULTIPLES

# Será frecuente querer crear nuevas variables como el resultado de aplicar condiciones sobre otras. Lo que sería el equivalente de case when en sql.
# Podríamos hacerlo con una serie de np.where anidados, pero en mi opinión la siguiente opción es más legible.

# Usaremos select de Numpy, al que hay que pasarle:

# - Una lista con las condiciones a evaluar (cada condición tiene que ir entre paréntesis)
# - Una lista con los resultados en caso de que las condiciones sean ciertas

# También tiene un parámetro default que podemos usar para detectar errores.

# https://numpy.org/doc/stable/reference/generated/numpy.select.html

# Al final conviene revisar que todo está bien con un value_counts()

# Por ejemplo, vamos a crear una nueva variable a partir de la cantidad financiada.
# NOTA: no confundir conceptualmente con la discretización manual. En aquella sólo podemos hacer cortes sobre la propia variable
# Sin embargo con la técnica que estamos viendo ahora podemos usar condiciones de varias variables, y también podemos usar que no son estrictramente cortes (por ejemplo igualdades en variables categóricas)
# Por sencillez vamos a crear tres grupos (<500, 500 a 1000, > 1000)

# Lista de condiciones
condiciones = [(df['Funded Amount'] <= 500),
               (df['Funded Amount'] > 500) & (df['Funded Amount'] <=1000),
               (df['Funded Amount'] > 1000)]

# Lista de resultados
resultados = ['01_Menor_o_igual_500','02_Entre_500_y_1000','03_Mayor_que_1000']
                
# Aplicamos select
df['Discretizada'] = np.select(condiciones,resultados, default = -999)

# Por último comprobamos con value_counts()
print(df.Discretizada.value_counts())

# CREAR O TRANSFORMAR VARIABLES AGRUPADAS

# La función clave aquí es groupby(): https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.groupby.html

# Parámetros más importantes:

# - na_action: se puede poner a 'ignore' para que no aplique la función sobre los nulos y los deje como nulos

# Una estructura de análisis muy común es combinar groupby() con apply() o transform().

# De nuevo hay una diferencia importante:

# - apply() devolverá un resultado agrupado para cada valor de la variable del groupby()
# - transform () devolverá el resultado de la agrupación pero repetido para cada valor de la variable del groupby()

# ¿QUÉ PASA CUANDO AGRUPAMOS? 

# Al aplicar los distintos métodos o funciones sobre un nuevo objeto de tipo agrupado tendrán un comportamiento diferente al habitual, que normalmente será aplicar ese método a cada elemento del grupo.

print(type(df.groupby('Sector')))

# USO DE GROUPBY CON APPLY

# Genera un dato agregado con el estadístico o función aplicada dentro de apply.
# Podemos usar apply para conocer el total de financiación en cada sector, a modo de insights

print(df.groupby('Sector')[['Funded Amount']].apply(sum))

# TÉCNICA PRO: O incluso podemos definir funciones personalizadas y luego aplicarlas con apply sobre el resultado de la agrupación.

# Por ejemplo vamos a encontrar las operaciones más antiguas por cada sector de cada país.
# Para ello definimos una función a la que le pasaremos cada agrupación mediante apply y sobre ella identficará los datos más antiguos.

def mas_antiguas(grupo):
    return(grupo['Funded Date'].nsmallest(2))

print(df.groupby(['Country','Sector']).apply(mas_antiguas))

# O todavía más eficiente con una función lambda

print(df.groupby(['Country','Sector'])['Funded Date'].apply(lambda grupo: grupo.nsmallest(2)))

# TRUCO: Como vemos, cuando usamos más de una variable en el groupby nos genera un multiíndice.
# Esto a veces puede ser molesto. Podemos evitarlo con el parámetro as_index = False, que nos pasará el multiíndice a columnas normales del dataframe.

# Vamos a ver el multíndice
print(df.groupby(['Country','Sector'])['Funded Amount'].sum())

# Aplicamos as_index = False
print(df.groupby(['Country','Sector'],as_index = False)['Funded Amount'].sum())

# USO DE GROUPBY CON TRANSFORM

# Al usar transform no agrega el resultado, si no que devuelve el mismo resultado para cada registro que pertence al grupo.
# Esto es muy útil para calcular variables del procentaje de contribución de cada miembro al total del grupo.

# Por ejemplo agrupando por equipo comercial y calculando con transform la suma del total de ventas nos devolvería una nueva variable con ese total de ventas del equipo.
# Después podríamos crear una nueva variable que divida las ventas de cada comercial por el total de su grupo.

# Podemos usar transform para añadir la suma de cada grupo a cada registro
df['Financiacion_Sector'] = df.groupby('Sector')[['Funded Amount']].transform(sum)

# Y calcular cuanto ha contribuído cada operación al total de su sector
df['Contrib_a_finan_sector'] = df['Funded Amount'] / df['Financiacion_Sector'] * 100

print(df[['Sector','Financiacion_Sector','Contrib_a_finan_sector']])

# Otro uso típico es para hacer una imputación avanzada de nulos, por la moda o media del grupo en lugar de la global

# Calcular la media de cada grupo para imputar por ella en lugar de por la media global
print(df.groupby('Sector')[['Funded Amount']].transform(np.mean))

# CREAR ACUMULADOS

# Los acumulados consisten en ir acumulando al total el dato del siguiente registro.
# Son muy usados en muchas operaciones de business analytics.

# Tenemos métodos ya construidos para los acumulados más comunes:

# - cumsum
# - cummax
# - cummin
# - cumprod

# Vamos a ir acumulando el importe de financiación concedida
print(df[['Funded Amount']].cumsum())

# CREAR ACUMULADOS POR GRUPOS

# Usaremos la estructura groupby() + función de acumulado.
# Va haciendo el acumulado hasta que cambia de grupo, momento en el que resetea y vuelve a empezar.

# Vamos a ir acumulando el importe de financiación concedida en cada sector
print(df.groupby('Sector')[['Funded Amount']].cumsum())

# CREAR INCREMENTOS

# Los incrementos consisten en ir comparando el dato de cada registro con el anterior y calculando el porcentaje que crece o decrece.

# Podríamos definirlo a mano, pero Pandas tiene un método para ponérnoslo más fácil: pct_change()
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.pct_change.html

# Parámetros más importantes:

# - periods: el número de registros hacia atrás sobre el que calcular el incremento, por defecto es 1

# Lógicamente los datos deben estar ordenados por la variable de interés, se usa sobre todo en series temporales.
# Por ejemplo sobre el acumulado que calculamos más arriba a generar ahora el porcentaje que va creciendo cada día.

# Vamos a ir acumulando el importe de financiación concedida

df['Acum'] = df[['Funded Amount']].cumsum()
df['Incr'] = df.Acum.pct_change()

print(df[['Funded Amount','Acum','Incr']].head(10))

# CREAR INCREMENTOS POR GRUPOS

# Usaremos la estructura groupby() + pct_change()

# Creamos un acumulado por sector para posteriormente calcular los incrementos
df['Acum_sector'] = df.groupby('Sector')['Funded Amount'].cumsum()

# Vamos a ir acumulando el importe de financiación concedida en cada sector y calcular el incremento
df['Incr_sector'] = df.groupby('Sector')['Acum_sector'].pct_change()

print(df[['Sector','Funded Amount','Acum','Incr','Acum_sector','Incr_sector']].head(10))

# CREAR LAGS

# Los lags son desplazamientos hacia atrás o hacia delante dentro de la misma variable.
# Por ejemplo para comparar el valor de la variable hoy con el que era ayer o hace 15 días.

# Podemos hacerlos con el método shift(): https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.shift.html

# Parámetros más importantes:

# - periods: el número de registros a moverse. Si es positivo se moverá hacia atrás y si es negativo hacia adelante
# - fill_value: el valor con el que rellenar los nulos que se generen por el efecto del desplazamiento

# Lógicamente los datos deben estar ordenados por la variable de interés, se usa sobre todo en series temporales.
# Por ejemplo sobre el acumulado que calculamos más arriba a generar ahora un indicador que nos diga si la financiación acumulada se ha incrementado en más de 400$ con respecto al día anterior.

# Primero creamos el lag

df['Acum_lag_1'] = df.Acum.shift(1, fill_value=0)
print(df[['Funded Amount','Acum','Acum_lag_1']].head(10))

# Ahora creamos el indicador

df['Mas_de_400'] = np.where(df.Acum - df.Acum_lag_1 >= 400,1,0)
print(df[['Funded Amount','Acum','Acum_lag_1','Mas_de_400']].head(10))

# CREAR LAGS POR GRUPOS

# A veces querremos que solo se cumpla la condición si los registros pertenecen a un mismo grupo.
# Por ejemplo en una estructura en transaccional cliente, mes, saldo querriámos marcar como fuga de capital cuando el saldo sea menos de 10.000€ que en el mes anterior, pero sólo en el caso de que sea el mismo cliente claro.

# Para ello podemos combinar groupby() + shift()

# En nuestro caso vamos a replicar ese efecto con el saldo acumulado y el sector.
# Es decir, queremos crear un indicador que sea 1 cuando el saldo acumulado sea 400$ superior al registro anterior, pero sólo si es del mismo sector.

# Primero creamos el lag
df['Acum_lag_1'] = df.groupby('Sector').Acum_sector.shift(1, fill_value=0)

# Creamos el indicador
df['Mas_de_400'] = np.where(df.Acum_sector - df.Acum_lag_1 >= 400,1,0)
print(df[['Sector','Funded Amount','Acum','Acum_sector','Acum_lag_1','Mas_de_400']].head(10))

# CREAR RANKINGS

# Los contextos de negocio están llenos de oportunidades para hacer rankings:

# - Oficinas con más ventas
# - Clientes que dejan más margen
# - Proveedores más costosos
# - Días del año con más afluencia en tiendas

# rank(): https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.rank.html

# Parámetros más importantes:

# - method: average, min, max, first. Es la posición que pone de ranking cuando hay empates. Con averagle pondría un valor intermedio, con min le pone a los empates el mínimo de ranking, con max les pone el máximo, con first asigna el ranking por el orden de aparición en el array
# - ascending: si True (por defecto) le da el ranking 1 al mínimo de la variable, si False le da el ranking 1 al máximo de la variable
# - na_option: qué ranking le da cuando encuentra un nulo en la variable. Con keep pone un nulo en el ranking, con top pone nulos en los primeros valores del ranking, con bottom pone nulos en los últimos valores del ranking. Cuidado, puede cambiar si cambiamos el ascending
# - pct: devuelve el ranking en porcentaje

# Vamos a crear un ranking para Funded Amount
df['FA_Ranking'] = df['Funded Amount'].rank(method = 'first', ascending = False)
print(df.sort_values(by = 'FA_Ranking').head(10))

# ANALISIS DE PARETO

# El análisis de Pareto es sin duda uno de los más importantes en busines analytics.
# Es el típico análisis de "el 20% de las causas provoca el 80% de los efectos". Por lo que también se le conoce como análisis 20/80
# Y en contextos de negocio se cumple en casi cada cosa que analicemos (por supuesto no de forma literal 20/80):

# - El 20% de los clientes supondrán el 80% de los beneficios
# - El 20% de los comerciales realizarán el 80% de las ventas
# - El 20% de proveedores se llevarán el 80% del presupuesto

# Por tanto es imprescindible que aprendas a realizarlo correctamente y también a interpretarlo.
# Hay implementaciones ya construidas, por ejemplo en Scipy, pero aquí vamos a aprender a hacerlo paso a paso.

# Concretamente este es el proceso que hay que seguir:

# 1. Debemos partir de una tabla en la que tengamos unidad de análisis y su dato correspondiente. En ocasiones tendremos que agregar para conseguir esa tabla inicial (como veremos en nuestro ejemplo)
# 2. Ordenar en descendente por la métrica de interés
# 3. Crear una variable con la posición, siendo 1 el mayor valor y aumentando secuencialmente hasta llegar al menor valor
# 4. Crear una variable con la posición en porcentaje, dividiendo cada posición por el máximo de la posición
# 5. Crear una variable con la suma acumulada del valor
# 6. Crear una variable con el acumulado en porcentaje, dividiendo cada posición por el máximo del acumulado
# 7. Por claridad quedarnos solo con las variables index, posición en porcentaje y acumulado en porcentaje
# 8. Si queremos visualizarlo en un gráfico

# Para el ejemplo vamos a hacer un análisis de Pareto sobre la distribución del total de financiación que se ha concedido a cada país.

# 1. Agregar para conseguir la tabla de partida

df_pais = df.groupby('Country')[['Funded Amount']].sum()
print(df_pais)

# 2. Ordenar en descendente por la métrica de interés

df_pais.sort_values('Funded Amount', ascending = False, inplace = True)
print(df_pais)

# 3. Crear una variable con la posición, siendo 1 el mayor valor y aumentando secuencialmente hasta llegar al menor valor

df_pais['Posicion'] = np.arange(start = 1, stop = len(df_pais) + 1)
print(df_pais)

# 4. Crear una variable con la posición en porcentaje, dividiendo cada posición por el total de registros

df_pais['Posicion_Porc'] = df_pais.Posicion.transform(lambda x: x / df_pais.shape[0] * 100)
print(df_pais)

# 5. Crear una variable con la suma acumulada del valor

df_pais['Acum'] = df_pais['Funded Amount'].cumsum()
print(df_pais)

# 6. Crear una variable con el acumulado en porcentaje, dividiendo cada valor por el máximo del acumulado

df_pais['Acum_Porc'] = df_pais.Acum.transform(lambda x: x / max(df_pais.Acum) * 100)
print(df_pais)

# 7. Por claridad quedarnos solo con las variables index, posición en porcentaje y acumulado en porcentaje

df_pais = df_pais[['Posicion_Porc','Acum_Porc']]
print(df_pais)

print(df_pais.Posicion_Porc.values)

# 8. Visualizarlo en un gráfico

f, ax = plt.subplots(figsize = (16,8))
ax.plot(df_pais.index, df_pais.Acum_Porc)
ax.plot(df_pais.index, df_pais.Posicion_Porc)
ax.tick_params(axis='x', labelsize=12, labelrotation=90)
plt.show()

# CREACIÓN DE UNA FUNCIÓN PARA HACER PARETO

# Replicar todos los pasos anteriores cada vez que queramos hacer un Pareto es muy laborioso.
# Vamos a encapsular todos los pasos en una función, que podrás usar en tus proyectos solo con copiar y pegar.

# A esta función hay que pasarle:

# La variable a analizar (como un Series)
# La salida que queramos que nos devuelva ('tabla'/'grafico'): por defecto es 'tabla'

def pareto_ds4b(variable, salida = 'tabla'):
    # Ordenar en descendente y pasar a dataframe
    pareto = variable.sort_values(ascending = False).to_frame()

    # Cambiar el nombre a la variable
    pareto.columns = ['Valor']

    # Crear la posición
    pareto['Posicion'] = np.arange(start = 1, stop = len(pareto) + 1)
    pareto['Posicion_Porc'] = pareto.Posicion.transform(lambda x: x / pareto.shape[0] * 100)

    # Crear el acumulado
    pareto['Acum'] = pareto['Valor'].cumsum()
    max_pareto_acum = max(pareto.Acum)
    pareto['Acum_Porc'] = pareto.Acum.transform(lambda x: x / max_pareto_acum * 100)

    # Simplificar
    pareto = pareto[['Posicion_Porc','Acum_Porc']]
    
    #Devolver la salida
    if salida == 'grafico':
        f, ax = plt.subplots(figsize = (16,8))
        ax.plot(pareto.Posicion_Porc, pareto.Acum_Porc)
        ax.plot(pareto.Posicion_Porc, pareto.Posicion_Porc)
        ax.tick_params(axis='x', labelsize=12, labelrotation=90)
        return(ax)
    else:
        return(pareto)

# Vamos a probarla creando de nuevo la tabla agregada con el nivel de análisis que necesitamos.

agregado_financiacion = df.groupby('Country')[['Funded Amount']].sum()
print(agregado_financiacion)

# Llamamos la función para que nos devuelva la tabla con el Pareto
pareto_ds4b(agregado_financiacion['Funded Amount'])

# Y ahora le pedimos el gráfico
pareto_ds4b(agregado_financiacion['Funded Amount'], salida = 'grafico');

# CREAR ALEATORIOS

# Realmente estas funciones no son de Pandas, si no de Numpy, concretamente de su módulo random.

# Las más interesantes son:

# - seed: crea una semilla para generar resultados reproducibles
# - rand: crea un real entre 0 y 1
# - randint: crea un entero en el rango que le digamos
# - randn: crea una distribución normal de reales
# - choice: elige aleatoriamente entre una lista

# Todos tienen el parámetro size que determina el número de elementos generados. Si lo usamos en un dataframe normalmente será igual al número de registros.
# Para añadirlas al dataframe como nuevas variables podemos usar las formas que ya conocemos o usar el método assign, que básicamente crea las nuevas variables y mantiene las anteriores: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.assign.html

# Numero de registros
num_reg = df.shape[0]

# Creamos la semilla
np.random.seed(1234)

# Incorporamos una variable de aleatorios de cada tipo visto anteriomente

df = df.assign(rand_v = np.random.rand(num_reg),
          randint_v = np.random.randint(1,101,num_reg),
          randn_v = np.random.randn(num_reg),
          choice_v = np.random.choice(['rojo','verde','amarillo'],num_reg)
         )

print(df.iloc[:,-4:].describe(include = 'all').T)

# CREAR VARIABLES DUMMIES

# Las variables dummy son el resultado de convertir una variable categórica en varias variables 0/1.
# A este proceso (en argot de modelización) también se le llama one hot encoding.

# Se hace con get_dummies(): https://pandas.pydata.org/docs/reference/api/pandas.get_dummies.html

# Parámetros más importantes:

# - columns: las variables a dumificar en formato lista (aunque sea una)
# - drop_first: si dejar fuera la primera categoría o no. Si lo hacemos para modelización con modelos afectados por la colinealidad deberíamos ponerlo a True

# Revisamos cuantos valores tiene Status
df.Status.value_counts()

# Dumificamos Status
pd.get_dummies(df,columns = ['Status'])

# Dumificamos Status quitando una cateogría
pd.get_dummies(df,columns = ['Status'], drop_first=True)  
