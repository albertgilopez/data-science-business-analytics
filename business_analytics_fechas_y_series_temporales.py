print("******************")
print("BUSINESS ANALYTICS")
print("******************")

print("**************************")
print("FECHAS Y SERIES TEMPORALES")
print("**************************")

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import scipy.stats as sp

# %matplotlib inline. Es para decirle cómo tiene que sacar los gráficos.
# En este caso significa que los saque como gráficos estáticos integrados en el propio notebook (de tal forma que se guarde y distribuya más fácilmente).

pd.options.display.min_rows = 6

df = pd.read_csv('DataSetKivaCreditScoring.csv', sep = ';', index_col = 'id',
                parse_dates = ['Funded Date','Paid Date'])
print(df)
print(df.head())
print(df.info())

# En casos empresariales nos encontraremos constantemente con datos referentes a fechas.
# En algunos ámbitos incluso son el principal dato de análisis, como por ejemplo en los históricos de ventas, de activos finacieros, de consumo de energía, etc.
# Sin embargo por su propia naturaleza son variables que debemos tratar de forma especial.
# En este módulo vamos a aprender las principales técnicas que necesitaremos cuando estemos trabajando con fechas para labores de análisis en entornos profesionales.
# Como siempre desde un punto de vista práctico vamos a aprender las 10 operaciones más poderosas con fechas que nos van a permitir generar insights de alto valor sobre este tipo de datasets.

# - Crear fechas
# - Extraer componentes
# - Redondear fechas
# - Indexar fechas
# - Business Moments
# - Restar fechas
# - Downsampling
# - Upsampling
# - Regularización
# - Ventanas móviles

# TRABAJAR CON FECHAS Y SERIES TEMPORALES

# El creador original de Pandas trabajaba como analista de mercados financieros, por lo que Pandas incorpora unas funcionalidades nativas muy potentes para series temporales.
# Aunque el análisis de series temporales es un ámbito que tiene su metodología propia y requiere un curso específico, sí vamos a ver aquí como usar esas funcionalidades para poder sacar el máximo partido a las variables tipo fecha que podamos tener en nuestro dataset.
# Técnicamente una serie temporal es cuando medimos la misma variable en varios puntos en el tiempo. Pero vamos a ver también formas útiles de trabajar con fechas en general, aunque no sea exactamente una serie temporal.

# Por otro lado, teorícamente, las mediciones deberían ser siempre bajo los mismos espacios de tiempo, por ejemplo todo los días. Pero en la realidad tampoco es así y veremos que Pandas nos da herramientas para gestionar eso que se llaman "series irregulares".
# Por último señalar que Python tiene sus propias estructuras y funciones para series temporales, igual que Numpy (muchas de las cuales usa Pandas). Lo cual puede ser un lio.
# Realmente con Pandas tendremos todo lo necesario para trabajar con este tipo de datos, así que la recomendación es usar siempre Pandas y evitar complejidad.

# NOTA: Los nulos temporales en Pandas aparecen como NaT (not a time) en lugar del típico NaN (not a number).

# TIPOS DE DATOS TEMPORALES

# En Pandas hay 3 estructuras de datos para gestionar datos temporales:

# - datetime (o timestamp): es un momento temporal concreto que incluye fecha y hora, por ejemplo 22/01/2021 a las 15:36:13. Tiene los componentes: year, month, day, hour, minute, second
# - period: es un período de tiempo, con inicio y final definidos, que se repite con una frecuencia por ejemplo un mes
# - timedelta: es la diferencia entre 2 momentos temporales. Tiene los componentes: day, hour, minute, second

# Nos vamos a centrar en datetime ya que es con lo que frecuentemente trabajaremos.
# El datetime es un único tipo de datos que incluye tanto fechas como horas. Es decir no tenemos como en Python un tipo para las fechas y otro para las horas.
# Se basa en el datetime64 de Numpy, que veremos a veces en las salidas.

# Además de estos 3 tipos también tenemos una cosa que se llaman offsets, que son como periodos temporales pero que respetan las reglas del calendario, por ejemplo "días laborables". Cuando los veamos más abajo te dejaré un link a la documentación de los principales offsets.

# FECHAS COMO ÍNDICE

# Este tema puede causar confusión al principio, por eso lo abordamos antes de empezar.
# Es bastante normal que cuando trabajamos con series temporales el índice del dataframe sea la variable fecha.
# Pero no siempre que tengamos una fecha tiene que ser un índice.
# Dada la importancia que tiene el concepto de índice en Pandas ocurre que cuando la fecha está como índice tiene unos métodos que no tiene cuando no está como índice (aunque sea la misma variable).
# Simplemente hay que ser consciente de ello y acordarse de que si no nos está dejando usar cierto método o funcionalidad posiblemente sea porque no está como índice.
# Cuando ponemos una fecha como índice nos crea un nuevo tipo: el datetimeindex, que como decimos aporta nuevas funcionalidades.

# CREAR FECHAS

# Hay 3 formas típicas en las que crearemos una fecha:

# - crearla directamente a partir, por ejemplo de una cadena
# - convertir a fecha en el momento, en el que estamos importando los datos
# - convertir a fecha a posteriori, cuando ya tenemos importandos los datos

# CREAR FECHAS DIRECTAMENTE

# Lo hacemos con la función Timestamp(): https://pandas.pydata.org/docs/reference/api/pandas.Timestamp.html

# Permite crear fechas con Timestamp a partir de sus componentes o de una cadena.

print(pd.Timestamp(year = 2021, month = 1, day = 21))

# En cuanto al tipo de dato la función Timestamp genera un datetime.

df['fecha_temp'] = pd.Timestamp(year = 2021, month = 1, day = 21)
print(df.info())

df.drop(columns = 'fecha_temp', inplace = True)
print(df)

# A PARTIR DE UNA CADENA

print(pd.Timestamp('2021-03-31'))

# Acepta inteligentemente varios formatos

print(pd.Timestamp('Jan 5, 2021'))

# Una cosa a tener en cuenta por si nos la encontramos, es que en algunos sistemas se almacena la fecha como un número relativo a una fecha de inicio, por ejemplo es común el número de nanosegundos desde la fecha Unix (1 de Enero de 1970), lo que se conoce como Unix epoch.

# Pandas usa por defecto esa convención si le pasamos un número.

print(pd.Timestamp(1))

# Aunque también podemos pasárselo en otras unidades, por ejemplo 365 días desde esa fecha

print(pd.Timestamp(365, unit = 'D'))

# CONVERTIR A FECHA EN LA IMPORTACIÓN. Dos subcasos:

# - Solo convertir a fechas
# - Convertir a fechas y poner una como índice

# Para convertir a fechas usaremos el parámetro parse_dates pasándole como lista las variables que son fechas.
# Si además queremos que una de ellas sea el índice se lo decimos con index_col.

# Pasar a tipo fecha
pd.read_csv('DataSetKivaCreditScoring.csv', sep = ';', parse_dates = ['Funded Date','Paid Date']).info()

# Establecer además el índice
pd.read_csv('DataSetKivaCreditScoring.csv', sep = ';', index_col = 'Funded Date',
                parse_dates = ['Funded Date','Paid Date']).info()

# CONVERTIR A FECHA TRAS LA IMPORTACIÓN

# Si ya tenemos un dataframe importado en el que las fechas no están todavía como datetime podemos transformarlas a posteriori con la función:

# to_datetime(): https://pandas.pydata.org/docs/reference/api/pandas.to_datetime.html

# Parámetros más importantes:

# - dayfirst: si el día viene primero, lo usaremos mucho por tener fechas europeas
# - yearfirst: si el año viene primero, para casos en los que venga con solo 2 dígitos

# Vamos a importar el df sin parsear las fechas

df2 = pd.read_csv('DataSetKivaCreditScoring.csv', sep = ';', index_col = 'id')
print(df2.head(3))

# Vemos en qué tipo están las fechas

print(df2.dtypes)

# Transformamos Funded Date y comprobamos su tipo

df3 = df2.copy()
df3['Funded Date'] = pd.to_datetime(df3['Funded Date'])

print(df3.dtypes)
print(df3.head(3))

# Pero si tuviéramos una fecha europea podría haber confusión
# Por ejemplo el 1 de Febrero lo entiende como el 2 de Enero
print(pd.to_datetime('01/02/2021'))

# Pero si usamos dayfirst ya lo entiende bien
print(pd.to_datetime('01/02/2021', dayfirst = True))

# Será común que si convertimos una fecha a posteriori también queramos ponerla como índice

df3 = df2.copy()
df3['Funded Date'] = pd.to_datetime(df3['Funded Date'])
df3.set_index('Funded Date',inplace = True)
df3 = df3.loc[~df3.index.isna()].sort_index() #eliminar nulos del índice y ordenarlo

print(df3.head())

# EXTRAER PARTES DE FECHAS

# Una de los usos más frecuentes será extraer diferentes partes de la fecha (año, mes, etc) por ejemplo para crear nuevas variables.

# Hay que diferenciar dos casos:

# - si la fecha ya es el índice: usaremos .year, .month, etc
# - si la fecha es un datetime pero no es índice: tendremos que usar el accessor .dt

# Cuando la fecha ya es un datetimeindex

print(df3.index.year)
print(df3.index.month)
print(df3.index.day)
print(df3.index.day_name())

# Cuando la fecha ya es un datetime pero no es índice

print(df['Funded Date'].dt.year)
print(df['Funded Date'].dt.month)
print(df['Funded Date'].dt.day)

# Hay muchos más atributos del accesor .dt de los que mostramos aquí. Te animo a que los revises al menos por alto haciendo lo siguiente:

# - Ir a esta url: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.dt.date.html
# - Ctrl + F en tu navegador (o la opción que sea para buscar) y activar "resaltar todo"
# - Buscar .dt. e ir revisando

# REDONDEAR FECHAS

# Cuando la fecha está como índice podemos redondearla fácilmente. Necesitamos definir:

# - Hacia donde queremos redondear
# - A qué unidad queremos redondear

# El hacia donde se lo especificamos con un método:

# - round(): redondea hacia la unidad más cercana (bien abajo o bien arriba)
# - floor(): redondea hacia abajo
# - ceil(): redondea hacia arriba

# La unidad se lo especificamos como un parámetro offset 'H', 'D', etc. Puedes verlos aquí:
# https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#offset-aliases

print(df3.index)
print(df3.index.round('H')) # al más cercano
print(df3.index.floor('H')) # hacia abajo
print(df3.index.ceil('H')) # hacia arriba

# INDEXAR FECHAS

# Pandas es muy potente a la hora de indexar fechas.
# La mejor forma de entender la funcionalidad es ir viendo ejemplos.
# Para ellos vamos a crear una versión simplificada de nuestro df.

dfs = pd.read_csv('DataSetKivaCreditScoring.csv', sep = ';', index_col = 'Funded Date',
                parse_dates = ['Funded Date'],usecols = ['Funded Date','Country','Loan Amount'])

print(dfs.head(3))

# Una fecha completa exacta
print(dfs.loc['2005-03-31 06:27:55+00:00'])

# Una parte de la fecha, por ejemplo solo ese día
print(dfs.loc['2007-03-02'])

# Una parte de la fecha, por ejemplo solo ese mes

dfs.loc['2007-03']
dfs = dfs.loc[~dfs.index.isna()].sort_index() # eliminar nulos del índice y ordenarlo
print(dfs)

# Una parte de la fecha, por ejemplo solo ese año
print(dfs.loc['2007'])

# O cualquiera de los anteriores pero haciendo un rango con slicing
print(dfs.loc['2007-03-01':'2007-03-15'])

# Podemos dejar abierta una parte
print(dfs.loc['2007-03-01':])

# Otra cosa curiosa es que la sintaxis del slice funciona para la parte de las fechas (como acabamos de ver) pero no funciona para la parte de las horas.
# Para las horas tendremos que usar el método .between_time()

# dfs.loc['02:00:00':'04:00:00'] # por ejemplo esto dará un error
dfs.between_time('02:00:00','04:00:00') # tenemos que hacerlo así

# TÉCNICA PRO:

# Si la fecha no está como índice no podremos usar tampoco el slicing.
# Pero hay una alternativa, que es usando between para generar un vector lógico que pasar al loc.

# Lo vemos con df en el que Funded Date no es índice
print(df.loc[df['Funded Date'].between('2007-03-01','2007-03-15')])

# Nos hemos centrado en la parte de indexar registros, pero como estamos usando loc realmente podemos indexar columnas a la misma vez para extraer solo las variables que nos interesen en el perído que nos interese

# print(df.set_index('Funded Date').loc['2005-03':'2005-04', ['Funded Amount','Country']]) # warning-error non-monotonic

# BUSINESS MOMENTS

# Podemos seleccionar automáticamente momentos que suelen ser relevantes en contextos de negocio como el primer día del mes, el cierre del trimestre, etc.

# Para ello usamos el método asfreq(): https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.asfreq.html
# Y le pasamos el offset deseado como parámetro: https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#offset-aliases

# Es importante que para que funcione la fecha tiene que estar como índice, no tener duplicados y estar ordenada en ascendente.
# Notar que asfreq() va a reindexar el índice en intervalos regulares, lo cual significa que generará un registro para la fecha que toque incluso si no existe dato para ella en el dataset original, y por tanto puede generar nulos (que podríamos gestionar con su argumento method)

# Para ilustrar bien esta operación vamos a usar el dataset del IBEX:

ibex = pd.read_csv('Historico_IBEX35_Diario.csv',
                   decimal = ',', thousands = '.',
                   parse_dates = ['Fecha'],
                   index_col = 'Fecha',
                   infer_datetime_format=True).sort_index()

print(ibex)

# Vamos a seleccionar solo el primer día de cada mes
print(ibex.asfreq('MS'))

# Ahora el último día de cada mes (notar como aplica de forma inteligente los meses de 28, 30 o 31 días)
print(ibex.asfreq('M'))

# Ahora el último dato de cada trimestre
print(ibex.asfreq('Q'))

# Además en muchos contextos de negocios solo interesan los días laborables, así que si le ponemos una B (de business) delante del offset solo tendrá en cuenta de lunes a viernes.
# Por ejemplo en el caso anterior, en los dos primeros registros justo coincidió que los últimos días del trimestre no eran laborables.
# Pero podemos usar fácilmente la B para que coja automáticamente el último día del trimestre QUE ERA LABORABLE.

print(ibex.asfreq('BQ'))

# Pero todavía tenemos más potencia!
# Imagínate que quieres seleccionar solo los miércoles de cada semana.
# Eso se llaman offsets anclados, y tenemos un montón disponibles: ttps://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#anchored-offsets

# Seleccionar los miércoles de cada semana
print(ibex.asfreq('W-WED').head(6))

# ¿Y qué tal sería poder seleccionar solo los miércoles pero de cada 15 días)?
# Pues solo tenemos que poner el número deseado delante de las unidades

print(ibex.asfreq('2W-WED').head(6))

# RESTAR FECHAS

# Para calcular el tiempo entre dos fechas podemos simplemente restarlas.
# Ello nos devuelve un nuevo tipo de dato que se llama timedelta.
# Que además podemos descomponerlo en sus diferentes componentes mediante el atributo dt.components

# Calculamos la diferencia

delta = df['Paid Date'] - df['Funded Date']
print(delta)

print(delta.dt.components) # la descomponemos

# Como el resultado es un dataframe podemos acceder al componente que nos interese
print(delta.dt.components['hours'])

# RESAMPLING

# Resampling consiste en hacer transformaciones en la frecuencia de los datos cuando el índice es un datetimeindex.

# En la práctica le daremos sobre todo 2 usos:

# - Convertir a una frecuencia más baja o downsampling
# - Convertir a una frecuencia más alta o upsampling

# Además nos va a regularizar la serie, lo cual es interesante ya que en la realidad nos pasará a menudo que no tenemos datos de todas las unidades temporales, por ejemplo de todos los días.
# Resample es una especie de groupby, por lo que siempre va a necesitar algún tipo de función de agregación posterior. Si no simplemente crea el objeto pero no generará resultados: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.resample.html

# DOWNSAMPLING

# Lo que queremos hacer es pasar a unidades de tiempo mayores, por ejemplo de horas a días.
# Se llama así porque al agregar se reduce el número de registros. 

# Al estar agregando tenemos que seleccionar alguna función de agregación.
# Y al hacerlo también nos va a regularizar la serie.

# Por ejemplo veamos los valores de nuestra serie df3:

print(pd.Series(df3.index.unique().sort_values()).head(10))

# Ahora vamos a hacer un resampling diario sumando por ejemplo el Funded Amount y vemos como nos va a crear todos los días intermedios:

print(df3.resample('D')[['Funded Amount']].sum().head(10))

# odemos aplicar la función de agregacion a todo el dataframe, aunque solo lo va a hacer sobre las variables en las que tenga sentido.

print(df3.resample('D').sum().head(10))

# Si quisiéramos usar diferentes funciones de agregación en cada variable podemos usar .agg()

# print(df3.resample('D').agg({'Funded Amount':'sum','Sector':sp.stats.mode})) # sp.stats.mode deprecated

# Vamos a hacer otro ejemplo quitando el 31 de Marzo de 2005 que nos molesta un poco y luego agregando cada 4 horas.

print(df3.loc['2005-04-01':].resample('4h').sum().head(10))

# TÉCNICA PRO

# Podemos construir variables de negocio muy interesantes combinando la agregación de downsampling con la agregación horizontal de variables.
# Por ejemplo suponiendo que tuviera sentido agregar nuestras 3 variables vamos a calcular varios estadísticos.

# Esto tendría sentido en casos como:

# - si las columnas fueran número de compras
# - si las columnas fueran el consumo de energía de diferentes máquinas
# - si las columnas fueran el grado de sobre carga de diferentes equipos de una misma red
# ...

print(df3.loc['2005-04-01':].resample('4h').sum())
# print(df3.loc['2005-04-01':].resample('4h').sum().agg(['sum', 'max', 'min', 'mean', 'std'], axis = 1))

# CAMBIANDO LAS ETIQUETAS

# Como vemos es muy flexible.
# Los códigos para especificarle diferentes unidades temporales se llaman "offset aliases" y podemos consultarlos aquí: https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#offset-aliases
# Fíjate que por ejemplo si ponemos solo M o Y se refiere al final del mes o año, mientras que si usamos MS o YS se refiere al principio del mes o año.

print(df3.loc['2005-04-01':].resample('M').sum().head(4))

# Ahora bien, vemos que la etiqueta que saca es la de un día, mientras que el dato se corresponde a todo un mes.
# O por ejemplo ¿qué pasas si agregamos por trimestre?

print(df3.loc['2005-04-01':].resample('Q').sum())

# Aunque nos está poniendo como etiqueta el último día del trimestre, lo cual ya se entiende bien, realmente le estamos poniendo la etiqueta de un día a un dato que es de todo el trimestre.
# Esa es la diferencia que comentábamos al princio del todo entre el timestamp y el period.
# Realmente ahora el dato hace referencia a un período (el trimestre entero).
# Afortunadamente resampling tiene el parámetro kind, con el cual podemos decirle que el nuevo dato es un período y nos va a poner directamente una etiqueta mejor.

# Repetimos el cálculo pero diciéndole que es un periodo
print(df3.loc['2005-04-01':].resample('Q', kind = 'period').sum())

# Pero cuidado lo que nos devuelve como indice ya no es un objeto datetimeindex si no un periodindex.
# No son exactamente iguales, por lo que como siempre en Python si tenemos comportamientos no esperados tenemos que ser muy conscientes del tipo de objeto que estamos manejando.

# Comprobamos el nuevo tipo de índice
print(df3.loc['2005-04-01':].resample('Q', kind = 'period').sum().info())

# TÉCNICA PRO

# La combinación entre resample y size nos permite responder preguntas de negocio muy interesantes del estilo: ¿Cuantos eventos pasan cada x tiempo?
# Por ejemplo imagina que estamos analizando ventas online y queremos saber cuantas se han producido cada media hora.

# Con nuestros datos vamos a calcular cuantas operaciones de financiación se producen cada intervalo de 5 días.

print(df3.loc['2005-04-01':].resample('5D').size())

# También podemo usar los anchored offsets con resample.
# Los recordamos: https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#anchored-offsets

# Por ejemplo vamos a sacar el número de financiaciones que se han producido los viernes de cada semana.

print(df3.loc['2005-04-01':].resample('W-FRI').size())

# TRUCO: OHLC

# Ohlc es una función diseñada para el ámbito financiero para calcular automáticamente los valores de apertura, más altos, más bajos, y de cierre respectivamente.
# Pero realmente lo que hace en general es calcular el primero, máximo, mínimo y ultimo, por lo que junto con resample puede ser muy útil ya que nos calculará esas variables por los intervalos de resample.

# Por ejemplo vamos a calcular el ohlc SEMANAL sobre los datos de apertura de nuestro dataset del IBEX.

print(ibex.resample('W').Apertura.ohlc().head())

# De nuevo al estar trabajando con periodos concretos quizá tiene más sentido que las etiquetas no sean puntos fijos si no periodos.
# Vemos que en el caso de ser semanas lo que hace es ponernos el inicio y fin de cada semana

print(ibex.resample('W',kind = 'period').Apertura.ohlc().head())

# UPSAMPLING SENCILLO

# Lo que queremos hacer es pasar a unidades de tiempo más pequeñas, por ejemplo de meses a días.
# Se llama así porque al hacerlo se incrementa el número de registros.

# Por tanto realmente nos estamos "inventando" datos.

# Principalmente incorporando nulos, un valor fijo o bien arrastrando hacia arriba o hacia abajo los valores:

# - asfreq(): para rellenar con nulos
# - asfreq(valor): para rellenar con el valor
# - ffill: para arrastrar hacia abajo
# - bfill: para arrastrar hacia arriba

# Y al hacerlo también nos va a regularizar la serie.

# Por ejemplo vamos a crear un dataframe demo con datos diarios y después lo bajaremos a franjas de 6h.

# Creamos un dataset diario

ind = pd.date_range('2005-04-01',periods = 100,freq= 'D')
diario = pd.DataFrame(data = np.random.rand(len(ind)),columns = ['var'], index = ind)
print(diario.head(8))

# Rellenamos con nulos
print(diario.resample('6h').asfreq().head(8))

# Rellenamos con un valor
print(diario.resample('6h').asfreq(5).head(8))

# Arrastramos hacia abajo
print(diario.resample('6h').ffill().head(8))

# Arrastramos hacia arriba
print(diario.resample('6h').bfill().head(8))

# UPSAMPLING AVANZADO

# Pero todavía podemos rellenar de formas más avanzadas, usando:

# interpolate(): https://pandas.pydata.org/docs/reference/api/pandas.core.resample.Resampler.interpolate.html

# Con el parámetro method nos permite diferentes formas de interpolar pero seguramente usaremos 'linear' para una interpolación lineal entre dos valores válidos

print(diario.resample('6h').interpolate(method = 'linear').head(8))

# REGULARIZAR UN DATAFRAME SIN AGREGAR

# Pero es posible que solo queramos regularizar el dataframe sin agregar ni interpolar.
# Es decir simplemente insertar vacías las filas necesarias para hacerlo regular.

# De nuevo podemos usar asfreq(): https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.asfreq.html

# Parámetros más importantes:

# - method: por si queremos rellenar hacia arriba o abajo
# - fill_value: para rellenar con un valor fijo

# Por ejemplo vamos a crear un dataframe irregular para la demo:

# - Primero con date_range crearemos uno regular de 100 días.

ind = pd.date_range('2005-04-01',periods = 100,freq= 'D')
regular = pd.DataFrame(data = np.random.rand(len(ind)),columns = ['var'], index = ind)
print(regular.head(8))

# - Despúes lo convertiremos en irregular eliminando 1 día de cada 2.

irregular = regular[::2]
print(irregular.head(10).head(8))

# - Y finalmente aplicaremos asfreq()

print(irregular.asfreq('D').head(8))

# Podemos rellenar los nulos con un valor fijo en lugar del nulo con fill_value.

print(irregular.asfreq('D',fill_value = 0).head(8))

# O arrastar los valores hacia abajo con method

print(irregular.asfreq('D', method = 'ffill').head(8))

# O arrastrar los valores hacia arriba con method

print(irregular.asfreq('D', method = 'bfill').head(8))

# VENTANAS MÓVILES
# VENTANAS MÓVILES NO PONDERADAS

# Las ventanas móviles son muy usadas en series temporales.
# Entre otras cosas sirven para "suavizar" las curvas y ver mejor efectos como tendencias o estacionalidad eliminando la excesiva variación que pueden tener los datos individuales.
# Básicamente consisten en que cada punto no va a tener su valor individual si no algún tipo de agregación de x días anteriores (o siguientes).

# Por ejemplo, el dato individual sería que el dato del día 7 tuviera el dato del día 7 y el del día 8 tuviera el dato del día 8.
# Pero si usamos una ventana temporal de 7 días el día 7 va a tener el dato agregado entre los días 1 y 7, y el día 8 va a tener el dato agregado entre los días 2 y 8 y así...
# Por eso al crear ventanas móviles nos va a generar nulos en aquellos datos en los que no haya podido calcular la ventana, en nuestro ejemplo tendría nulos en los días del 1 al 6.

# Quizá el agregado más conocido y más usado sea la media, dando lugar a las medias móviles, pero realmente podemos usar el que queramos.

# Creamos las ventanas móviles con rolling(): https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.rolling.html

# Para hacer el ejemplo vamos a regularizar y agregar por día, y después crearemos varias ventanas móviles.

agregado_dia = df3.sort_index().loc['2005-04-01':].resample('D',kind = 'period').sum()
print(agregado_dia.head(10))

# Suma móvil de 3 días
# print(agregado_dia.rolling(3).sum().head(8))

# También podemos generar varias métricas basadas en ventanas usando .agg()
print(agregado_dia['Funded Amount'].rolling(3).agg(['sum','mean']).head(8))

# Hay que tener en cuenta que tenemos que pasarle una ventana que siempre sea fija.
# Por ejemplo pasarle "Mes" no funciona ya que no es fijo.

# Media movil mensual
# print(agregado_dia.rolling('M').mean())

# Pero podríamos pasarle 30 días.
# print(agregado_dia.rolling(30).mean().head(40))

# Vamos a ver cómo hacer ventanas móviles suaviza la curva.

agregado_dia['Funded Amount'].plot(figsize = (16,8))
agregado_dia['Funded Amount'].rolling(30).mean().plot(figsize = (16,8));
plt.show()

# VENTANAS MÓVILES PONDERADAS

# No es raro, sobre todo en usos de predicción, que queramos darle más peso a los datos más recientes de la ventana en lugar de que todos pesen lo mismo.

# Para ello podemos usar el método:

# ewm(): https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.ewm.html

# Básicamente hay que decirle un método de ponderación. Hay varios y son relativamente complejos.

# Comparamos la media móvil con la media móvil ponderada exponencialmente
agregado_dia['Funded Amount'].rolling(30).mean().plot(figsize = (16,8), color = 'red')
agregado_dia['Funded Amount'].ewm(span = 30).mean().plot(figsize = (16,8), color = 'blue');
plt.show()

# O también podríamos aplicar con rolling una ponderación propia (o cualquier otra función personalizada).
# Por ejemplo pongamos que queremos ventanas de 3 días donde el más reciente pese el 50%, el del medio un 30% y el más lejano un 20%.

def mi_ponderacion(x):
    ponderacion = x[0] * 0.2 + (x[1] * 0.3) + (x[2] * 0.5)
    return(ponderacion)

print(agregado_dia['Funded Amount'].rolling(3).apply(mi_ponderacion))

# Comparamos la media móvil con la media móvil ponderada con ponderación propia
agregado_dia['Funded Amount'].rolling(3).mean().plot(figsize = (16,8), color = 'red')
agregado_dia['Funded Amount'].rolling(3).apply(mi_ponderacion).plot(figsize = (16,8), color = 'blue');
plt.show()

