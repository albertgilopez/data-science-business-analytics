print("******************")
print("BUSINESS ANALYTICS")
print("******************")

print("**********************")
print("CONSULTAS INTERACTIVAS")
print("**********************")

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# %matplotlib inline. Es para decirle cómo tiene que sacar los gráficos.
# En este caso significa que los saque como gráficos estáticos integrados en el propio notebook (de tal forma que se guarde y distribuya más fácilmente).

pd.options.display.min_rows = 6

df = pd.read_csv('DataSetKivaCreditScoring.csv', sep = ';', index_col = 'id',
                parse_dates = ['Funded Date','Paid Date'])
print(df)
print(df.head())
print(df.info())

# El tipo de operaciones que estaremos haciendo más frecuentemente en Business Analytics es lo que conoce como queries o consultas interactivas.

# Básicamente consiste en ir "haciendo preguntas" a los datos, buscando conclusiones o patrones que puedan ser de interés.
# Y se llaman interactivas porque no estamos hablando de las típicas consultas para hacer informes que las lanzas y te vas a tomar un café hasta que salgan.
# Si no que son cosas mucho más dirigidas, y que normalmente tras ver los resultados de la anterior nos dará la pista para hacer la siguiente.
# Es lo que yo llamo ir tirando del hilo o interrogando a los datos.

# Python es muy buen lenguaje para esto, ya que al trabajar en memoria los tiempos de respuestas para datasets de tamaño razonable son casi instantáneos.
# Para que aterrices todo eso, preguntas típicas pueden ser: ¿cuales son los productos más vendidos?, ¿en qué tiendas?, ¿qué clientes realizan más devoluciones?, ¿y son iguales para todos los productos o dependen de su tipo? por poner algunos ejemplos

# En módulos futuros veremos mas sobre el "arte" de hacer consultas interactivas, pero de momento aquí vas a aprender las técnicas que necesitas dominar.
# En proyectos de este tipo tendremos que hacer cientos de consultas, y dominar estas técnias nos dará precisión de cirujano para obtener justo lo que queremos, solo lo que queremos, cuando lo queremos y con el menor código y esfuerzo posible.

# Hay 10 operaciones de consultas interactivas que tenemos que dominar.

# - Seleccion avanzada de columnas
# - Filtro avanzado de registros
# - Método Query
# - Ordenar registros y columnas
# - Consultas TOP N
# - FSC
# - Tablas cruzadas
# - Tablas dinámicas
# - Minicubo
# - Risk scorecard

# OPERACIONES DE CONSULTA
# SELECCION AVANZADA DE COLUMNAS

# Recordamos que podíamos seleccionar columnas con las notaciones de punto, corchetes y dobles corchetes. Si son más de una los dobles corchetes.

print(df['Country'])
print(df.loc[:,'Country'])

# Ahora vamos a aprender una nueva forma, con la función filter().
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.filter.html

# Hay que tener cuidado de no confundirse con el nombre. Aunque se llame filter realmente lo que hace es seleccionar, bien filas o bien columnas, aquí la usaremos para columnas.

print(df.filter(['Country']))

# A priori parece que hace lo mismo que las anteriores. Entonces ¿para qué aprender una nueva forma?.
# Hay una cosa útil de filter que son los parámetros like y regex.

# - Regex se refiere a usar una expresión regular. Es algo más complicado fuera del alcance de este curso. Pero que sepas que si decides dedicar unas horas a aprenderlo por tu cuenta podrías usarlo aquí.
# - Y like que es bastante más fácil de usar y nos da capacidades para seleccionar cadenas de texto similares.

print(df.filter(like = 'Coun'))

# Con lo que podemos sustituir la forma que habíamos aprendido hasta ahora que es más complicada.

print(df.loc[:,df.columns.str.contains('Coun')])

# FILTRO AVANZADO DE REGISTROS
# FILTRAR REGISTROS POR CIERTOS VALORES

# isin():https://pandas.pydata.org/docs/reference/api/pandas.Series.isin.html

# Devuelve un booleano con los registros que estén dentro de los valores pasados como una lista.

# Parámetros más importantes:

# - values: lista de valores
# - Como devuelve un booleano podríamos usar la indexación booleana y funcionaría.

paises_de_interes = ['India','Indonesia']
print(df[df.Country.isin(paises_de_interes)])

# Sin embargo mi recomendación como sabes es usar siempre loc ya que funciona en todos los escenarios.

print(df.loc[df.Country.isin(paises_de_interes)])

# También se puede hacer en negativo, es decir, seleccionar todo EXCEPTO lo que está en la lista. Se hace anteponiendo una tilde.

print(df.loc[~df.Country.isin(paises_de_interes)])

# FILTRAR REGISTROS ENTRE CIERTOS VALORES

# Hasta ahora para filtrar registros entre dos valore lo que hacíamos era definir un criterio compuesto y usar indexación booleana.

criterio = (df['Loan Amount'] >= 1000) & (df['Loan Amount'] <= 2000)
print(df.loc[criterio])

# Pero Pandas tiene un método que nos lo pone más fácil: between()
# Devuelve un booleano con los registros que estén entre los valores pasados como una lista.

# https://pandas.pydata.org/docs/reference/api/pandas.Series.between.html

# Parámetros más importantes:

# - left: desde
# - rigth: hasta
# - inclusive: si incluir los límites o no (por defecto sí los incluye)

print(df.loc[df['Loan Amount'].between(1000,2000)])

# EL MÉTODO QUERY

# Ya sabíamos filtrar registros usando loc e iloc.
# Y hemos aprendido 2 nuevas técnicas que nos lo ponen más fácil en casos concretos.
# Pero en este tipo de análisis en el que básicamente estaremos "interrogando los datos", o lo que se conoce como "consultas interactivas" como caso general, Pandas tiene otro método que nos va a resultar más sencillo.

# Se llama el método query()
# No obstante tampoco es perfecto ya que:

# - en líneas generales nos da menos opciones que loc e iloc
# - y en particular solo permite filtrar registros, no columnas (aunque hay un truco que veremos al final)
# - más que un método es casi una aproximación diferente a las consultas de selección de registros.

# Lo primero a entender es la lógica, ya que es un poco diferente. Vamos a ir viendo una a una las principales reglas.
# Las consultas se ponen en modo texto, como si fuera una cadena, entre comillas simples.
# Y si necesitamos usar comillas por ejemplo para decir el valor que queremos tenemos que usar comillas dobles.

print(df.query('Sector == "Food"'))

# Se usan operadores más legibles, como and, or y not, en lugar de &, | y ~

print(df.query('Sector == "Food" or Sector == "Agriculture"'))

# Si tenemos variables (como en nuestro caso) que tienen espacios entre los nombres tenemos que usar el acento inverso (backticks).

print(df.query('`Funded Amount` > 1000'))

# Si queremos consultar una variable entre dos valores podemos hacer una versión reducida de la consulta.

df.query('`Funded Amount` > 1000 and `Funded Amount` < 2000') # en lugar de esto
print(df.query('1000 < `Funded Amount` < 2000')) # podemos hacer esto

# Podemos comparar directamente variables entre sí dentro de la consulta.

print(df.query('`Paid Amount` == `Loan Amount`'))

# Incluso hacer operaciones entre variables dentro de la propia consulta.

print(df.query('`Paid Amount` - `Loan Amount` == 0'))

# Podemos usar el operador in y el not in para dar una lista de valores y simplificar la consulta.
# Hay que recordar usar las dobles comillas para los valores de la lista ya que estamos dentro de la cadena de la query.

print(df.query('`Country Code` in ["UG", "GZ"]'))
print(df.query('`Country Code` not in ["UG", "GZ"]'))

# Podemos usar variables calculadas por fuera, dentro de la consulta, pero tenemos que usar la arroba para indicarlo.

media = df['Funded Amount'].mean()
print(df.query('`Funded Amount` > @media'))

# Podemos usar directamente la palabra index para trabajar con el índice.

print(df.query('50 < index < 100'))

# Hemos visto que query nos da gran potencia para hacer consultas rápidas e interactivas.
# Pero todo lo que hemos hecho trabaja filtrando los registros y nos devuelve siempre todas las columnas.
# No tiene una forma directa dentro de query para seleccionar columnas.
# Pero podemos simplemente pasar una lista detrás de query con las columnas que queramos y obtendremos el mismo resultado.

print(df.query('50 < index < 100')[['Funded Date','Sector']])

# NOTA: sobre todas las consultas anteriores podríamos seguir operando para realizar análisis sobre lo que devuelve query.
# Cosas como: conteos, medias, etc. Pero de momento nos quedamos con la idea de que query no solo sirve para seleccionar registros, si no que después podremos hacer cosas directamente sobre ellos.
# Y dar respuesta a consultas como "¿Cual es la media de financiación de las operaciones del sector Food que además sean de Uganda o de Kenya?"

print(df.query('(`Country Code` == "UG" or `Country Code` == "KE") and Sector == "Food"')['Funded Amount'].mean())

# FILTRAR ESTILO SELECT DISTINCT

# Una operación común en SQL es el select distinct, que nos devuelve los valores únicos (sin duplicados) de la consulta que le hayamos hecho.
# Si quisiéramos hacerlo sobre una sola variable podríamos usar directamente el método unique que ya conocemos. Pero sobre dos o más variables no funcionará.

# Lo que sí podemos usar para conseguir el efecto select distinct es seleccionar las columnas y luego encadenar .drop_duplicates()

print(df[['Country','Sector']].drop_duplicates())

# ORDENAR
# ORDENAR REGISTROS
# ORDENAR POR EL ÍNDICE

# sort_index(): https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.sort_index.html

# Parámetros más importantes:

# - axis: 0 (defecto) para filas y 1 para columnas
# - ascending: para ordenar en descendente deberemos ponerlo a False

print(df.set_index('Paid Date').sort_index(ascending = False))

# ORDENAR POR UNA O VARIAS VARIABLES

# sort_values(): https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.sort_values.html

# Si ordenamos por varias variables se las tenemos que pasar como una lista.

# Parámetros más importantes:

# - ascending: para ordenar en descendente deberemos ponerlo a False

print(df.sort_values('Loan Amount'))
print(df.sort_values(['Loan Amount','Country']))

# ORDENAR COLUMNAS
# ORDEN ALFABETICO

# También podemos usar sort_index() para ordenar alfabéticamente las columnas, usando el parámetro axis = 1.

print(df.sort_index(axis = 1))

# ORDEN PERSONALIZADO
# CON POCAS COLUMNAS

# Para aplicar un orden personalizado a las columnas hay que:

# - Crear una lista con el orden deseado
# - Reindexar las columnas

# Para crear la lista podemos obtener la lista actual con list(df.columns) y luego copiar-pegar para definir el orden deseado.

orden_original = list(df.columns)
print(orden_original)

# Pasamos Status a la primera posición

orden_deseado = ['Status',
                 'Funded Date',
                 'Funded Amount',
                 'Country',
                 'Country Code',
                 'Loan Amount',
                 'Paid Date',
                 'Paid Amount',
                 'Activity',
                 'Sector',
                 'Delinquent',
                 'Name',
                 'Use']

print(orden_deseado)

# Para aplicar el cambio reodenamos con el método reindex() pasándole el orden deseado al argumento columns.

# https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.reindex.html

# No hace inplace ni tiene el argumento inplace así que si queremos persistir los cambios hay que asignar de nuevo a df.

print(df.reindex(columns = orden_deseado))

# CON MUCHAS COLUMNAS

# Pero si tenemos muchas columnas incluso el método anterior puede ser pesado.
# No hay una forma directa para decirle a Pandas "pon estas columnas así y luego el resto que hayamos tocado".

# Pero sí podemos hacer un pequeño truco:

# 1. Crear una lista solo con las variables que queremos modificar el orden
# 2. Crear una lista con el resto dropeando las de la lista anterior
# 3. Combinar ambas listas
# 4. Aplicar reindex()

# 1. Crear una lista solo con las variables que queremos modificar el orden

a_reodenar = ['Status',
             'Name',
             'Use']

print(a_reodenar)

# 2. Crear una lista con el resto dropeando las de la lista anterior

resto = df.drop(columns = a_reodenar).columns.to_list()
print(resto)

# 3. Combinar ambas listas

orden_deseado = a_reodenar + resto
print(orden_deseado)

# 4. Aplicar reindex()

print(df.reindex(columns = orden_deseado))

# CONSULTAS TOP N

# VALORES MÁS ALTOS DE UNA VARIABLE

# nlargest(): https://pandas.pydata.org/docs/reference/api/pandas.Series.nlargest.html

# Parámetros más importantes:

# - n: por defecto saca 5 pero podemos ponerle los que queremos

print(df['Funded Amount'].nlargest()) # Series

# Si queremos que nos devuelva todo el dataframe en lugar de solo la serie entonces usaremos el método de dataframe, pero hay que especificarle la variable con columns.

print(df.nlargest(n = 5, columns = 'Funded Amount'))

# VALORES MÁS BAJOS DE UNA VARIABLE

# nsmallest(): https://pandas.pydata.org/docs/reference/api/pandas.Series.nsmallest.html

# Parámetros más importantes:

# - n: por defecto saca 5 pero podemos ponerle los que queremos

print(df['Funded Amount'].nsmallest())

# Si queremos que nos devuelva todo el dataframe en lugar de solo la serie entonces usaremos el método de dataframe, pero hay que especificarle la variable con columns.

print(df.nsmallest(n = 5, columns = 'Funded Amount'))

# AGREGADOS

# Tanto nlargest() como nsmallest() pueden trabajar con groupby(), multiplicando su potencia de análisis.

print(df.groupby('Country')['Funded Amount'].nlargest())
print(df.groupby('Country')['Funded Amount'].nsmallest())

# Pero, ¿cómo hacemos si queremos sacar simplemente los N valores más frecuentes por grupo?
# Ya que para usar la anterior estructura necesitamos una variable de análisis, y con los conteos no tenemos.

# La solución es combinar nlargest (o nsmallest) con value_counts()

print(df.value_counts('Country').nlargest())

# TÉCNICAS DE ANÁLISIS POR GRUPOS
# EL FRAMEWORK SUIZO PARA CONSULTAS

# Al explorar los datos es frecuente analizar los estadísticos básicos pero agrupados por otras variables.
# También es una técnica muy potente para generación de insights y consultas interactivas.

# Veremos que se nos pueden presentar varias casuísticas como:

# - Un estadístico de una variable agrupado por otra variable
# - Un estadístico de varias variables agrupado por otras variables
# - Varios estadísticos de una variable agrupado por una variable
# - Varios estadísticos de varias variables agrupado por una variable

# Todo ello nos da gran potencia pero también puede resultar lioso.
# Por tanto, utilizaremos un framework general ("Framework Suizo para Consultas" (FSC), porque es como la navaja suiza de las consultas, que te permitirá resolver cualquier situación de análisis mediante consultas simplemente memorizando esta frase:

# Una o varias variables de agrupación (con groupby), de una o varias variables de análisis (indexadas) por uno o varios estadísticos (con agg).

# O su versión reducida en pseudocódigo: groupby() + indexación + agg()

# Y su sintaxis: df.groupby(['var_grupo1','var_grupo2'])[['var_analisis1','var_analisis2']].agg(['estadístico1','estadístico2'])

# Por tanto vemos 3 componentes principales:

# - Las variables de agrupación: usamos groupby() para aplicar varias se lo pasamos como lista: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.groupby.html
# - Las variables de análisis: fijarse que para aplicar varias hay que usar doble corchete (lista dentro de indexación)
# - Los estadísticos: count, mean, max, etc. Para aplicar varios usamos agg(): https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.agg.html

# Es muy importante aprender este framework general, ya que podremos reformular prácticamente cualquier consulta de negocio a él.
# Además a partir de él podremos simplificar al caso de solo una variable en algún componente o incluso a no tener que usar los 3 componentes.
# Este framework te da una potencia tremenda al analizar con Pandas para objetivos de Business Analytics.

print(df.groupby(['Country','Sector'])[['Loan Amount','Paid Amount']].agg(['count','mean']))

# Vemos que esta estructura genera un multiíndice. Es posible que queramos quitarlo con reset_index() para trabajar más cómodos.

print(df.groupby(['Country','Sector'])[['Loan Amount','Paid Amount']].agg(['count','mean']).reset_index())

# E incluso pivotar a formato largo para gestionar más fácil todos los datos.

print(df.groupby(['Country','Sector'])[['Loan Amount','Paid Amount']].agg(['count','mean']).reset_index().melt(id_vars = ['Country','Sector'],
                                                                                                         var_name = ['Variable','Metrica'],
                                                                                                         value_name = 'Valor'))

# TRUCO

# Cuando encadenamos varios métodos la visualización se hace más difícil.
# Podemos dividir el código en varias líneas usando alguno de estos métodos:

# - Poner el caracter de "continua" al final de cada línea: \
# - Meter toda la expresión entre paréntesis

print(df.groupby(['Country','Sector'])[['Loan Amount','Paid Amount']] \
    .agg(['count','mean']) \
    .reset_index() \
    .melt(id_vars = ['Country','Sector'],
          var_name = ['Variable','Metrica'],
          value_name = 'Valor'))

# O poniendo paréntesis:

(df.groupby(['Country','Sector'])[['Loan Amount','Paid Amount']]
    .agg(['count','mean'])
    .reset_index()
    .melt(id_vars = ['Country','Sector'],
          var_name = ['Variable','Metrica'],
          value_name = 'Valor'))

# FLEXIBILIDAD DEL FSC

# Este framework es muy flexible, así que hay que dedicarle varias horas de trabajo para exprimir todo su pontencial.
# Vamos a hacer usarlo en varios escenarios para que interiorices la lógica, pero te recomiendo que experimentes por tu cuenta.
# Por ejemplo, si sólo usamos un elemento en alguno de los componentes podemos pasar a una notación simple (sin listas)

print(df.groupby('Country')['Loan Amount'].agg('count'))

# E incluso si sólo estamos usando un estadístico no sería necesario usar agg, sirve con el estadístico como método.

print(df.groupby('Country')['Loan Amount'].count())

# Si nos fijamos, con la sintaxis anterior de corchetes simples (o con la sintaxis de punto) nos devuelve un Series, pero será frecuente que queramos un dataframe.
# Para ello podemos usar dobles corchetes (realmente es pasarle una lista a la indexación, aunque sea de un solo elemento) aunque tengamos una sola variable, porque así nos devuelve un dataframe.

print(df.groupby('Country')[['Loan Amount']].count())

# Vamos a ver algunos parámetros y variantes útiles y frecuentes.
# Con el parámetro as_index = False dentro del groupby no pone la variable de agregación como índice y entonces devuelve un dataframe, normalmente más "manejable".
# NOTA: esto solo funciona si estamos agrupando por una sola variable, si agrupamos por más tendremos que usar al final .reset_index() como ya habíamos visto más arriba.

print(df.groupby('Country', as_index = False)['Loan Amount'].agg('count'))

# Podemos usar directamente describe() con groupby() y tener un buen vistazo general de los valores de una variable.

print(df.groupby('Country')['Loan Amount'].describe())

# Si no le incluímos el componente de las variables de análisis aplicará los estadísticos sobre todas las variables de análisis del dataset para cada valor de la variable de agregación, lo cual nos puede dar mucha eficiencia.

# print(df.groupby('Country').agg(['count','mean','max','min'])) # hay que controlar que sean variables numéricas
# Transponemos al final para una mayor legibilidad
print(df.select_dtypes('number').agg(['count','mean','max','min']).T)

# Incluso podemos incluirle funciones definidas por nosotros (aunque irán sin comillas)

def nulos(x):
    return(x.isna().sum())

print(df.select_dtypes('number').agg(['count','mean','max','min', nulos]).T)

# Cuando usamos el componente de agrupación podemos construir una tabla personalizada de variables de análisis y los estadísticos que queremos en cada una.

# Para ello tenemos que usar la siguiente sintaxis de tupla dentro de agg: nombre = ('variable_analisis','estadistico')

# Vamos a coger como ejemplo una numérica y una categórica

print(df.groupby('Sector').agg(media_financiacion = ('Funded Amount','mean'),
                        fecha_mas_reciente = ('Funded Date', 'max')))

# CONTEOS AGRUPADOS DE VALORES DE VARIAS VARIABLES

# Ya conocemos value_counts() para conteos de una variable.
# Si queremos hacer conteos de una variable agrupada por otra-s usaremos la estructura groupby().variable + value_counts()
# Es un subtipo de la fórmula general presentada anteriormente, pero que estaremos haciendo de forma bastante frecuente.

print(df.groupby('Country').Sector.value_counts())

# Pero si intentamos quitar el multiíndice haciendo reset_index() como antes nos da un error.
# df.groupby('Country').Sector.value_counts().reset_index()

# El problema es que la Series salida del conteo nos la está llamando Sector, y al quitar el multiindice nos dice que está duplicado.
# Podemos renombrar la salida y después ya quitarle el multiíndice.

print(df.groupby('Country').Sector.value_counts().rename('Conteo').reset_index())

# APLICAR FILTRO AL RESULTADO DE GROUPBY ANTES DE HACER UN CALCULO

# TECNICA PRO: Esta técnica es avanzada pero en ocasiones es muy útil.
# Se trata de aplicar un filtro sobre el resultado de un groupby antes de aplicar la función de análisis correspondiente.
# En contextos de negocio estas operaciones son más frecuentes de lo que parecen. Por ejemplo:

# - Calcula el importe medio de transacción pero solo para compras que incluyan más de 3 productos
# - Calcula la facturación total por oficina pero solo para las oficinas que tengan entre 2 y 5 empleados
# - Saca el máximo que se ha gastado en una compra cada cliente que tenga un gasto medio superior a 1000€

# Lo hacemos con el siguiente proceso:

# - groupby() por la variable de agrupación y cálculo de la métrica por la que filtraremos (conteo, media, etc)
# - usar filter con una función lambda para filtrar solo los registros que cumplan la condición
# - volver a hacer gropby() sobre la variable de agrupación y calcular la métrica final a representar

# Por ejemplo imagínate que queremos la media del importe financiado pero sólo para los países que hayan tenido más de 100 operaciones de financiación.

# Veamos primero qué países deberían ser

print(df.Country.value_counts())

# Si aplicamos el filtro vemos que seleccionamos solo los que cumplen la condición

print(df.groupby('Country').filter(lambda x: x.Country.count() > 100).Country.unique())

# Ahora vamos a ponerlo todo junto para ver cómo sería la query completa

(print(df.groupby('Country').filter(lambda x: x.Country.count() > 100)
    .groupby('Country')['Funded Amount'].mean()))

# Otro ejemplo: Calcula la financiación máxima que se ha concedido por país pero sólo para países cuya financiación media es superior a 700$

(print(df.groupby('Country').filter(lambda x: x['Funded Amount'].mean() > 700)
    .groupby('Country')['Funded Amount'].max()))

# PRIMER O ÚLTIMO VALOR DE UNA VARIABLE POR GRUPO

# Podemos extraer el primer valor de una variable de análisis para cada valor de otra variable de agrupación con la siguiente estructura:

# groupby() + first() o groupby() + last()

# Cuidado, el primer (o último) valor no significa el mínimo ni el máximo, si no el primer valor que se encuentra según como esté ordenado el dataframe.

# Valor financiado del primer registro de cada país
print(df.groupby('Country')['Funded Amount'].first())

# Valor financiado del último registro de cada país
print(df.groupby('Country')['Funded Amount'].last())

# TABLAS CRUZADAS

# Es una manera muy frecuente para revisar relaciones entre variables.

# pd.crosstab(df['var1'],df['var2']): https://pandas.pydata.org/docs/reference/api/pandas.crosstab.html

# Parámetros más importantes:

# - normalize: lo saca en porcentajes (realmente tanto por 1): con 'all' sobre el total, con 'index' sobre las filas y con 'columns' sobre las columnas
# - margins: muestra los totales
# - margins_name: poner un nombre personalizado a los totales
# - values: la variable de análisis
# - aggfunc: la función que queremos usar como métrica (ver más abajo)

# Lo usamos cuando queremos un formato de salida de tabla cruzada.

# En porcentaje (realmente tanto por 1), y añadiendo los totales

print(pd.crosstab(df.Country,df.Sector, normalize = 'all', margins = True, margins_name= 'Total'))

# Por defecto crosstab saca conteos, pero podemos usarlo para analizar una tercera variable con los parámetros:

# - values: la variable de análisis
# - aggfunc: la función que queremos usar como métrica

# Media de financiación por país y sector
print(pd.crosstab(df.Country, df.Sector, values = df['Funded Amount'], aggfunc = 'mean'))

# crosstab() no trae por defecto ningún parámetro para reemplazar los nulos, pero podemos encadenar fillna()

# Media de financiación por país y sector
print(pd.crosstab(df.Country, df.Sector, values = df['Funded Amount'], aggfunc = 'mean').fillna(0))

# TABLAS DINÁMICAS

# Son una generalización de crosstab() pero más flexibles porque podemos definir las variables que queremos como index y como columns, incluso varias variables en cada una e incluso analizando varias métricas en cada celdilla.

# pivot_table(): https://pandas.pydata.org/docs/reference/api/pandas.pivot_table.html
# NOTA: Es un método de dataframe, es decir se hace con df.pivot_table()

# Parámetros más importantes:

# - index: variables a usar en el índice
# - columns : variables a usar en las columnas
# - values: la variable de análisis
# - aggfunc: la función que queremos usar como métrica
# - fill_value: valor para reemplazar las celdillas que sean nulos
# - margins: muestra los totales
# - margins_name: poner un nombre personalizado a los totales

print(df.pivot_table(index = 'Country', columns = 'Sector', values = 'Funded Amount', aggfunc = 'mean', fill_value=0))

# Podemos crear la estructura de filas y columnas como queramos, incluso con varias variables en cada una.

print(df.pivot_table(index = ['Country','Delinquent'],
               columns = ['Sector','Status'],
               values = 'Funded Amount',
               aggfunc = 'mean', fill_value=0))

# E incluso aplicar varios estadísticos de resumen. Aunque se vuelve difícil de interpretar rápidamente.

print(df.pivot_table(index = ['Country','Delinquent'],
               columns = ['Sector','Status'],
               values = 'Funded Amount',
               aggfunc = ['count','mean'],
               fill_value=0))


# RESALTAR INFORMACIÓN

# Si la salida de la consulta es grande, o nos cuesta localizar la info más importante a ojo podemos usar el método style de Pandas.

# Lo que hace es resaltar la información que le digamos.
# Tiene varias opciones por defecto, pero vamos a destacar:

# - highlight_max: para resaltar el máximo
# - highlight_min: para resaltar el mínimo
# - highlight_null: para resaltar los nulos

# Por defecto los resalta en amarillo, pero podemos especificar otro color con el parámetro color, e incluso encandenar uno tras otro para resaltar por ejemplo el máximo y el minimo.

df.groupby('Sector')[['Funded Amount']].mean().style.highlight_max().highlight_min(color = 'red')

# Podemos usar el método bar para crear unas barras proporcionales al valor del dato (estilo Excel)

df.groupby('Sector')[['Funded Amount']].mean().sort_values('Funded Amount',ascending = False).style.bar(color = 'green')

# Finalmente también podemos definir nuestras propias funciones personalizadas y aplicarlas al dataframe mediante:

# - apply(): si es algo que tenga que evaluar variable a variable
# - applymap(): si es algo que tenga que evaluar dato a dato

# Por ejemplo vamos a crear una versión reducida de df, llamada df2, y después aplicar una función personalizada

df2 = df.iloc[0:10].copy()
print(df2.head())

# Aplicamos una función personalizada

def mayor_que(dato,criterio = 400):
    if dato > criterio:
        return('background-color: lightgreen')
    else:
        return('color: red')

df2[['Funded Amount']].style.applymap(mayor_que)

# MINICUBOS

# Los "cubos" son una técnica muy usada en business intelligence (no confundir con business analytics) que consiste básicamente en organizar la información en métricas (lo que se quiere analizar) y dimensiones (las vistas de análisis).

# Y precalcular el resultado de las métricas en los cruces de las dimensiones.

# Con el objetivo de que cuando se necesite un dato no se tenga que calcular en tiempo real, si no que simplemente se recupere del cubo y por tanto la experiencia de usuario sea mucho mejor.

# Para business analytics podemos simplificar la técnica, haciendo un cubo unidimensional, es decir precalculando las métricas para cada dimensión, pero no para el cruce de dimensiones.

# Y lo vamos a llamar minicubo.

# El minicubo nos va a dar gran potencia de análisis y además va a ser la base de la técnica que aprenderemos después: el risk scorecard.

# Para construir un minicubo:

# - Seleccionar qué variables serán la métricas y cuales las dimensiones
# - Pasar a transaccional las dimensiones
# Agregar las métricas por "variable" y "valor" con las funciones deseadas (suma, conteo, etc)

# Por ejemplo vamos a construir un minicubo para analizar Funded Amount por las dimensiones Country, Sector, Activity y Status.

# PASO 1: Seleccionar qué variables serán la métricas y cuales las dimensiones

metrica = ['Funded Amount']
dimensiones = ['Country','Sector','Activity','Status']

minicubo = df[dimensiones + metrica]
print(minicubo)

# PASO 2: pasar a transaccional las dimensiones

minicubo = minicubo.melt(id_vars='Funded Amount')
print(minicubo)

# PASO 3: Agregar las métricas por "variable" y "valor" con las funciones deseadas

minicubo = minicubo.groupby(['variable','value'])['Funded Amount'].agg(conteo = 'count', media = 'mean')
print(minicubo)

# A partir de aquí podemos usar el minicubo para obtener insights de forma muy rápida.
# Por ejemplo: analiza el número de operaciones y la financiación media en cada sector.

minicubo.loc['Sector'].plot.bar();
plt.show()

# Y continar analizando con el minicubo es tan sencillo como cambiar la variable de indexación.

minicubo.loc['Status'].plot.bar();
plt.show()

# También podemos usar el minicubo para encontrar rápidamente insights sobre "perfiles".
# Por ejemplo encuentra los atributos de las operaciones que consiguen mayor financiación.

print(minicubo.media.nlargest(10))

# RISK SCORECARD

# Los Risk Scorecards son una técnica de business analytics muy potente pero que sin embargo muy pocos analistas conocen (fuera del ámbito del análisis de riesgo)
# En casos en los que por la razón que sea no se pueden hacer modelos predictivos esta técnica llega a ser un sustituto válido.
# Tal es así que aún hoy en día los bancos la siguen utilizando para sus análisis de riesgo.

# Aunque hablaremos en términos de riesgo (por respetar su origen) realmente se puede aplicar a prácticamente cualquier caso de negocio.
# Como se suele hacer sobre un evento binario (p.e el impago) el proceso básicamente consiste en calcular el riesgo individual de cada atributo (proporción de impago), asignarle unos puntos y luego simplemente calcular el riesgo de una operación sumando los puntos de sus atributos.

# En nuestro caso vamos a modificar el concepto para estimar la financiación esperada (una media) para un tipo concreto de operación, y usaremos para ello el minicubo.
# Por ejemplo: calcula la financiación media esperada para financiar un 'Beauty Salon' en 'Uganda' que previsiblemente será 'paid'.

# Eliminamos el multiindice
minicubo.reset_index(inplace = True)

# Definimos los criterios de la operación
criterios = ['Beauty Salon','Uganda','paid']

# Creamos el dataset del análisis de la operación
financiacion_df = minicubo.loc[minicubo.value.isin(criterios)]
print(financiacion_df)

# Calculamos la financiación esperada de la operación
print(financiacion_df.media.mean())


