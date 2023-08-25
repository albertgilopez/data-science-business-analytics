print("******************")
print("BUSINESS ANALYTICS")
print("******************")

print("*************************")
print("VISUALIZACIÓN CON SEABORN")
print("*************************")

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import scipy.stats as sp

# %matplotlib inline. Es para decirle cómo tiene que sacar los gráficos.
# En este caso significa que los saque como gráficos estáticos integrados en el propio notebook (de tal forma que se guarde y distribuya más fácilmente).

pd.options.display.min_rows = 6

# Importación de los datos para usar de ejemplos
df = sns.load_dataset('tips')
print(df.head())

# VISUALIZACIÓN CON SEABORN. ¿Por qué usar Seaborn?

# Ya hemos aprendido los dos paquetes más importantes para hacer gráficos. Así que uno podría pensar ¿por qué aprender un tercero?

# Seaborn aporta principalmente 2 cosas sobre Matplotlib y Pandas:

# - Los gráficos son estéticamente más bonitos
# - Trae gráficos (normalmente de uso estadístico) que son más complejos pero que sin embargo se hacen de forma bastante fácil y directa

# Por tanto su uso no es imprescindible pero yo lo recomiendo cuando ya estés haciendo gráficos no para tí si no para presentar en algún tipo de entregable.
# O cuando quieres hacer un gráfico que con los otros paquetes te resultaría un poco más complejo y con Seaborn se haga de forma fácil.
# Digamos que es como una mezcla entre la sencillez de Pandas y las opciones de personalización de Matplotlib.

# En la práctica los 3 paquetes comparten mucho ya que están construidos sobre Matplotlib. Por tanto el uso práctico no será en plan "cargo sólo un paquete y me ciño únicamente a él".
# Si no que solemos cargar los 3 y será frecuente usarlos entremezclados. Por ejemplo hacer el gráfico con Pandas durante el desarrollo del análisis, modificar algunas opciones con Matplotlib y replicarlo finalmente en Seaborn para un informe.
# Al final termina siendo como un único conjunto total de recursos que tienes para hacer gráficos y que usas a conveniencia independientemente del paquete al que pertenezca cada uno.

# CÓMO HACER UN GRÁFICO EN SEABORN

# A grandes rasgos es el mismo proceso que con los anteriores paquetes: primero hacemos tipo de gráfico que queramos y luego lo personalizamos.
# La diferencia es que Seaborn está pensado para gráficos estadísticos, lo cual significa que por defecto nos va a sacar gráficos más cercanos a nuestras necesidades como data scientist.
# Y que además encapsula y organiza mejor todo el tema de parámetros y opciones, que hace que sea más fácil de usar.

# GRÁFICO DE LÍNEAS

# Se hace con lineplot y especificando el eje x y el eje y.

# Este gráfico se usa sobre todo con series temporales, con lo que será frecuente que mapeemos el eje x al index, que será la variable fecha.

# https://seaborn.pydata.org/generated/seaborn.lineplot.html#seaborn.lineplot

# - hue: permite representar otra variable en el gráfico mediante el color
# - size: permite representar otra variable en el gráfico mediante el tamaño de la línea
# - style: permite representar otra variable en el gráfico mediante el estilo de la línea
# - palette: para personalizar los colores de cada serie. Bien de forma preconfigurada, ver aquí las paletas que se pueden usar: https://matplotlib.org/3.3.3/tutorials/colors/colormaps.html, o bien mediante una lista personalizada.

sns.lineplot(data = df, 
             x = df.index, 
             y = 'tip',
             hue = 'sex', 
             size = 'sex', 
             style = 'sex'
            );

# Fíjate en la facilidad para incorporar una variable categórica como una nueva dimensión del gráfico. Si recuerdas para hacer eso con Matplotlib teníamos que pasarlo a numérica con .cat.codes() y poner el texto en la leyenda. Era complicado. Aquí sin embargo sale todo automáticamente.

# IMPORTANTE: Si vas a la documentación no encontrarás argumentos en los gráficos de Seaborn para hacer cosas básicas como cambiar el color, el tipo de línea, etc.
# El motivo es que para todos esos aspectos básicos usamos los argumentos de Matplolib que le pasamos a través de **kwargs
# Aunque lo estemos viendo ahora en el gráfico de líneas el mismo concepto aplica a todos los gráficos.

# Por ejemplo, vamos a cambiar el color, tamaño y tipo de la línea.

sns.lineplot(data = df, 
             x = df.index, 
             y = 'tip',
             color = 'red', 
             lw = 3, 
             ls = ':');

# GRÁFICO DE BARRAS

# Si recordamos, para hacer un gráfico de barras en Matplotlib nosotros teníamos primero que agregar los datos y después representarlos. Seaborn nos ahorra ese proceso.

# Si lo que queremos como agregación son las frecuencias (conteos) le podemos pasar directamente la variable que queremos representar y él calcula el conteo de frecuencias y lo representa con countplot.

# https://seaborn.pydata.org/generated/seaborn.countplot.html#seaborn.countplot

# - hue: permite representar otra variable en el gráfico mediante el color
# - palette: para personalizar los colores de cada barra. Bien de forma preconfigurada, ver aquí las paletas que se pueden usar: https://matplotlib.org/3.3.3/tutorials/colors/colormaps.html, o bien mediante una lista personalizada.
# - order: una lista con el orden que queremos para las barras

sns.countplot(data = df, x = 'sex');

# Si quisiéramos definir un color para todo el gráfico usaríamos color.

sns.countplot(data = df, x = 'sex', color = 'red');

# Pero si queremos asociar el color a una variable usamos hue.

sns.countplot(data = df, x = 'sex', hue = 'sex');

# Podemos adaptar los colores de forma pre-establecida con hue + palette.

sns.countplot(data = df, x = 'sex', hue = 'sex', palette = 'summer');

# O totalmente personalizada con palette y una lista.

sns.countplot(data = df, x = 'sex', palette = ['red','blue']);

# Si queremos otro tipo de agregación usaremos barplot. Que por defecto nos agregará según la media de cada categoría.

# https://seaborn.pydata.org/generated/seaborn.barplot.html#seaborn.barplot

# Por ejemplo esto representa la propina media por sexo

sns.barplot(data = df, x = 'sex', y = 'tip');

# Pero si quisiéramos otra función de agregación se lo podemos decir con el parámetro estimator.

# Por ejemplo podemos usar cualquiera de numpy, scipy, etc. Esto representa la mediana de la propina por sexo

sns.barplot(data = df, x = 'sex', y = 'tip', estimator = np.median);

# La línea vertical que nos pone en cada barra es el intervalo de confianza al 95%.
# Por ejemplo en el caso anterior nos estaría diciendo que aunque parece que la mediana de las mujeres es más baja realmente el intervalo de confianza en el que nos moveríamos es muy similar entre ambos sexos, y por tanto habría que tener cuidado con afirmar que las mujeres dejan menores propinas (y posiblemente someterlo a un test estadístico para comprobar si es o no estadísticamente significativo).
# Lo calcula internamente usando bootstrapping, ya que no disponemos de una distribución muestral si no solo del dato de nuestra muestra (repasa el módulo de introducción a la estadística del curso puente si esto te suena a chino).
# De todas formas en la mayoría de los casos no querremos hacer un uso inferencial si no simplemente descriptivo. Por lo que si las líneas nos molestan las podemos quitar con ci = None

sns.barplot(data = df, x = 'sex', y = 'tip', estimator = np.median, ci = None);

# TRUCO:

# Si queremos que el gráfico muestre porcentajes en lugar de frecuencias tendremos que usar esta opción de barplot en lugar de countplot pero además:

# - precalcular los porcentajes con value.counts(normalize = True)
# - fijarse en que ahora NO HAY QUE USAR DF si no el dataset con el precálculo
# - usar el índice como el eje y los valores (porcentajes) como el eje y

porcentajes = df.sex.value_counts(normalize = True)

sns.barplot(x = porcentajes.index, y = porcentajes.values * 100);

# Podemos cambiar a horizontal mapeando la variable a y en lugar de a x

sns.countplot(data = df, 
              y = 'sex',
              hue = 'smoker',
              palette='pastel');

# Usando order podemos definir un orden personalizado en una lista y que lo use para las barras

orden = ['Sun','Sat','Fri','Thur']
sns.countplot(data = df, y = 'day',order = orden);

# Otro uso práctico frecuente es cuando tenemos muchas categorías pero sólo queremos representar las más frecuentes.
# Y usamos order como un truco para hacer ese filtro.

# Vamos a representar sólo los 2 días con mayor frecuencia 
top2 = df.day.value_counts().index[:2]
sns.countplot(data = df, y = 'day',order = top2);

# BOXPLOT

# Se hace con boxplot: https://seaborn.pydata.org/generated/seaborn.boxplot.html#seaborn.boxplot

# - hue: permite representar otra variable en el gráfico mediante el color
# - palette: para personalizar los colores de cada caja. Bien de forma preconfigurada, ver aquí las paletas que se pueden usar: https://matplotlib.org/3.3.3/tutorials/colors/colormaps.html, o bien mediante una lista personalizada.
# - Para una variable simplemente se la mapeamos en el eje de las y si lo queremos vertical o en el de las x si lo queremos horizontal.

sns.boxplot(data = df, y = 'total_bill'); # en vertical
sns.boxplot(data = df, x = 'total_bill'); # en horizontal

# Para representar la distribución de una variable en cada valor de otra usamos ambos ejes. Una será categórica y la otra contínua.

sns.boxplot(data = df, x = 'sex', y = 'total_bill');
sns.boxplot(data = df, x = 'sex', y = 'total_bill', hue = 'smoker');

# HISTOGRAMA

# Se hace con histplot. Y por defecto nos da un histograma: https://seaborn.pydata.org/generated/seaborn.histplot.html#seaborn.histplot

# - bins: número de intervalos
# - hue: permite representar otra variable en el gráfico mediante el color
# - palette: para personalizar los colores de cada barra. Bien de forma preconfigurada, ver aquí las paletas que se pueden usar: https://matplotlib.org/3.3.3/tutorials/colors/colormaps.html, o bien mediante una lista personalizada.
# - cumulative: distribución acumulada

sns.histplot(data = df, x = 'total_bill');
sns.histplot(data = df, x = 'total_bill', bins = 50, color = 'green', cumulative = True);

# DENSIDAD

# Se hace con displot usando el parámetro kind = 'kde': https://seaborn.pydata.org/generated/seaborn.displot.html#seaborn.displot

# - hue: permite representar otra variable en el gráfico mediante el color
# - palette: para personalizar los colores de cada serie. Bien de forma preconfigurada, ver aquí las paletas que se pueden usar: https://matplotlib.org/3.3.3/tutorials/colors/colormaps.html, o bien mediante una lista personalizada.

sns.displot(data = df, x = 'total_bill',kind= 'kde');
sns.displot(data = df, x = 'total_bill',kind = 'kde', hue = 'sex');

# SCATTER PLOTS

# Hay diferentes gráficos con los que podemos hacer un scatter, pero el básico se hace con scatterplot.

# https://seaborn.pydata.org/generated/seaborn.scatterplot.html#seaborn.scatterplot

# - hue: permite representar otra variable en el gráfico mediante el color del marcador
# - size: permite representar otra variable en el gráfico mediante el tamaño del marcador
# - style: permite representar otra variable en el gráfico mediante la forma del marcador
# - palette: para personalizar los colores de cada serie. Bien de forma preconfigurada, ver aquí las paletas que se pueden usar: https://matplotlib.org/3.3.3/tutorials/colors/colormaps.html, o bien mediante una lista personalizada.
# - legend: tipo de leyenda 'auto', 'brief', 'full', or False

sns.scatterplot(data = df, x = 'total_bill', y = 'tip');
sns.scatterplot(data = df, x = 'total_bill', y = 'tip',
                hue = 'sex',
                size = 'smoker', 
                style = 'smoker',
                alpha = 0.3,
                legend = 'full'
               );

# Una variación interestante son los lmplot, que permiten hacer unos scatter pero creando también la línea de regresión.
# https://seaborn.pydata.org/generated/seaborn.lmplot.html#seaborn.lmplot

sns.lmplot(data = df, x = 'total_bill', y = 'tip');

# Además, si usamos otra variable de agrupado nos crea una recta para cada una y podemos comparar visualmente si hay diferencias por grupos.

sns.lmplot(data = df, x = 'total_bill', y = 'tip', hue = 'smoker');

# TRUCO: Aunque en muchos casos la relación entre las dos variables no será lineal.
# Así que podemos obtener un mejor insight con el parámetro lowess = True que ajustará una curva en lugar de una recta.
# Para ver mejor la curva podemos cambiarla de color o grosor con line_kws.

# NOTA: los parámetros kws son una forma de pasarle parámetros de Matplotlib en algunos gráficos como los scatter. Pero es un poco críptico porque no funciona en todos los gráficos y además hay que pasarlo como un diccionario. Por tanto simplemente apúntatelo como un código "receta" y aquí está para copiar-pegar cuando lo necesites.

# sns.lmplot(data = df, x = 'total_bill', y = 'tip', lowess = True, line_kws={'color': 'red', 'linewidth':10});

# PAIR PLOT

# Sirve para hacer gráficos automáticos comparando todas las variables cuantitativas entre sí.
# Pero sobre todo es útil en modelización predictiva para visualizar el tipo de relación de cada variable con la target.

# https://seaborn.pydata.org/generated/seaborn.pairplot.html

# - hue: permite representar otra variable en el gráfico mediante el color del marcador
# - size: permite representar otra variable en el gráfico mediante el tamaño del marcador
# - x_vars: lista con las variables predictoras
# - y_vars: variable a predecir
# - kind: tipo de gráfico. Para este uso recomiendo ponerlo a 'reg' y así nos muestra la recta de regresión
# - palette: para personalizar los colores de cada serie. Bien de forma preconfigurada, ver aquí las paletas que se pueden usar: https://matplotlib.org/3.3.3/tutorials/colors/colormaps.html, o bien mediante una lista personalizada.

# Por ejemplo, vamos a suponer que quisiéramos predecir el total de la cuenta a partir del resto de variables, y por tanto total_bill sería la target.

sns.pairplot(df,kind = 'kde')
sns.pairplot(df, x_vars = ['tip','size'], y_vars = 'total_bill', kind = 'reg');

# GRÁFICO DE CORRELACIÓN

# Se hace con un heatmap sobre una matriz de correlación: https://seaborn.pydata.org/generated/seaborn.heatmap.html

# - annot: si True incluye el dato en cada celda
# - cmap: el mapeo de color. https://matplotlib.org/3.1.0/tutorials/colors/colormaps.htm

# sns.heatmap(df.corr(), annot = True, cmap = 'Greys');

# PERSONALIZACIÓN

# TEMAS Y CONTEXTOS

# Seaborn tiene como unos formatos predeterminados, que al usarlos configuran varias opciones por defecto.

# Los temas configuran temas más de aspecto y estilo.
# Y los contextos están más orientados a configurar sobre todo las escalas pensando en dónde se va a publicar el gráfico.

# - darkgrid
# - whitegrid
# - dark
# - white
# - ticks

sns.set_style('darkgrid')
sns.histplot(df.total_bill);

sns.set_style('whitegrid')
sns.histplot(df.total_bill);

sns.set_style('dark')
sns.histplot(df.total_bill);

sns.set_style('white')
sns.histplot(df.total_bill);

sns.set_style('ticks')
sns.histplot(df.total_bill);

# Puedes resetear los cambios con: sns.reset_defaults()

sns.reset_defaults()

# Los contextos disponibles son:

# - paper
# - notebook
# - talk
# - poster

sns.set_context('paper')
sns.histplot(df.total_bill);

sns.set_context('notebook')
sns.histplot(df.total_bill);

sns.set_context('talk')
sns.histplot(df.total_bill);

sns.set_context('poster')
sns.histplot(df.total_bill);

# BORDES DEL GRÁFICO

# Los bordes se llaman spines. Para dejar sólo los ejes x e y usamos sns.despine()

sns.histplot(data = df, x = 'total_bill')
sns.despine();

# Si queremos elimarlos todos (o hacer una configuración personalizada) usamos los parámetros left, right, ...

sns.histplot(data = df, x = 'total_bill')
sns.despine(left = True, bottom = True);

# TAMAÑO DEL GRÁFICO

# Como Seaborn se basa en Matplotlib podemos usar sus opciones para definir el tamaño.

plt.figure(figsize = (8,2))
sns.histplot(data = df, x = 'total_bill');

# HACER SUBPLOTS

# Es parecido a cómo se hace en Matplotlib, pero en vez de hacer ax[0].plot como en Matplotlib aquí se incluye un parámtro ax dentro de la función.

f, ax = plt.subplots(1,2, figsize = (12,4))

sns.boxplot(ax = ax[0], data = df, y = 'total_bill')
sns.boxplot(ax = ax[1], data = df, x = 'total_bill');

# TÍTULOS DEL GRÁFICO Y DE EJES

# Se los ponemos con la api funcional de Matplotlib.

plt.figure(figsize = (8,2))
sns.histplot(data = df, x = 'total_bill')
plt.title('Este es el titulo', fontsize = 20)
plt.xlabel('Total de la factura', fontsize = 14);

# ORDENAR EL GRÁFICO

# Arriba en la parte del gráfico de barras horizontales vimos cómo ordenear por un orden manual usarndo order.
# Pero en muchas ocasiones querremos un orden automático, como por ejemplo en descendente o ascendente según el valor.

# Para ello necesitamos extraer los nombres de la Serie ordenda como queremos. Operativamente:

# - Hacer un value_counts()
# - Extraer el index del punto 1
# - Usarlo en el gráfico con order

sns.countplot(data = df, x = 'day', order = df.day.value_counts().index);

# En el caso de estar usando hue para representar otra dimensión también podemos ordenar esa dimensión de igual forma que antes, pero usando el parámetro hue_order.

sns.countplot(data = df, x = 'sex', hue = 'day', hue_order = df.day.value_counts().index);

# TAMAÑO DE LA LETRA

# Como vimos antes podemos cambiar los tamaños con los contextos, pero si queremos un ajuste un poco más fino podemos usar el parámetro font_scale que es un múltiplo del tamaño original.
# Como en la mayoría de los casos el gráfico será para el notebook podemos definir ese contexto y luego ponerle letra 1.5 veces superior con font_scale = 1.5

sns.set_context('notebook', font_scale = 1.5)
sns.histplot(data = df, x = 'total_bill')
plt.title('Este es el titulo');

# Otra opción es usar sns.set con font_scale.

sns.set(font_scale=2.5)
sns.histplot(data = df, x = 'total_bill')
plt.title('Este es el titulo');

# CAMBIAR LOS COLORES

# La mayoría de los gráficos tienen una opción color en la que podremos definirsélo directamente

sns.histplot(data = df, x = 'total_bill', color = 'red');

# Y también vimos en la sección de los gráficos el parámetro pallete, con el que podemos darle al gráfico un estilo prediseñado cuando estamos usando hue.
# Recordemos que podemos ver las paletas aquí: https://matplotlib.org/3.3.3/tutorials/colors/colormaps.html

sns.scatterplot(data = df, x = 'total_bill', y = 'tip', hue = 'sex', palette = 'summer');

# O podemos pasarle una lista con los colores que queramos directamente a palette y así tener una personalización completa.

sns.scatterplot(data = df, x = 'total_bill', y = 'tip', hue = 'sex', palette = ['red','black']);

# Palette no funciona únicamente con hue, si no también cuando haya una diferencia de algún tipo de grupo por color.
# Por ejemplo, si hacemos un countplot por defecto ya aplica diferentes colores, así que incluir palette lo puede personalizar.

f, ax = plt.subplots(1,2, figsize = (12,4))

sns.countplot(ax= ax[0], data = df, x = 'day')
sns.countplot(ax= ax[1], data = df, x = 'day', palette = 'summer');

# O en un boxplot donde la x tenga varios valores.

f, ax = plt.subplots(1,2, figsize = (12,4))

sns.boxplot(ax= ax[0], data = df, x = 'day', y = 'tip')
sns.boxplot(ax= ax[1], data = df, x = 'day', y = 'tip', palette = 'Greys');

# PERSONALIZACIONES BÁSICAS DE MATPLOTLIB

# Como ya hemos dicho varias veces Seaborn está construído encima de Matplotlib.
# Así que si hay alguna opción que Seaborn no la traiga como un parámetro propio, podemos intentar la de Matplotlib y en muchos casos la cogerá.
# Especialmente en los temas básicos como color, tipo de línea, grosor, etc.

# CAMBIAR TIPOS DE LÍNEA, COLORES, GROSOR, ...

# Los 3 últimos parámetros no son de Seaborn si no de Matplotlib

sns.lineplot(data = df, x = df.index, y = 'tip',ls = '--',linewidth = 8, color = 'red');

# AÑADIR LÍNEAS VERTICALES U HORIZONTALES

# En algunos casos, según la sintaxis de lo que queramos hacer, es posible que tengamos que guardar el gráfico como un objeto y luego aplicar la opción de Matplotlib

g = sns.lineplot(data = df, x = df.index, y = 'tip',ls = '--',linewidth = 8, color = 'red')
g.axvline(80, ls = '-.')
g.axhline(7, ls = '-.');

# CAMBIAR EL RANGO DE LOS EJES

g = sns.lineplot(data = df, x = df.index, y = 'tip',ls = '--',linewidth = 8, color = 'red')
g.set_xlim(50,150)

# TAMAÑO Y ROTACIÓN DE ETIQUETAS DE LOS EJES

# Ejemplo para hacer más pequeñas y rotar las etiquetas de los ejes
# Será frecuente que se nos solapen y Seaborn no tiene una buena solución por defecto

g = sns.countplot(data = df, x = 'day')
g.tick_params(axis='x', labelsize=10, labelrotation=45)

# FACETS

# Los facets son como "segmentaciones" en el sentido de que nos va a repetir el gráfico solicitado pero para cada valor de la variable que estamos usando como facet. Dos pasos:

# - Crear una figura con la variable de segmentación, con FacetGrid
# - Mapear el gráfico que queramos hacer y la variable a representar con map

f = sns.FacetGrid(df, col = 'smoker')
f.map(sns.histplot, 'total_bill');

# Podemos crear matrices cruzando dos variables de segmentación.
# Solo tenemos que incluir el parámetro row con la segunda variable.

f = sns.FacetGrid(df, col = 'smoker',  row = 'sex')
f.map(sns.histplot, 'total_bill');

# CONSEJO PRÁCTICO

# Como has visto hay muchas opciones. Y quizá no todo lo estandarizadas que sería deseable.
# Haremos muchas con Seaborn, pero tendremos que recurrir a veces a Matplotlib.
# En algunos gráficos podemos usar el parámetro internamente, en otros el mismo parámetro tendremos que hacerlo por fuera.

# Por ello voy a explicarte cómo yo suelo hacer los gráficos en la práctica para que puedas copiar el proceso.

# 1. Defino los aspectos generales como tamaño, paleta y letra
# 2. Hago el gráfico y las personalizaciones que me permite Seaborn (o las que le paso a Matplotlib a través de Seaborn)
# 3. Termino con las personalizaciones de Matplotlib

# Vamos a ver un par de ejemplos.

# Opciones generales

plt.figure(figsize = (12,6))
sns.set(font_scale=1.5, palette= "viridis")

# Gráfico principal y opciones Seaborn (o Matplotlib a través)

sns.countplot(data = df, 
              x = 'sex', 
              hue = 'day', 
              hue_order = df.day.value_counts().index)

# Opciones Matplotlib

plt.title('Titulo del grafico', fontsize = 20)
plt.xlabel('Sexo y dia', fontsize = 14)
plt.ylabel('Frecuencia', fontsize = 14);

# Opciones generales

f, ax = plt.subplots(1,2, figsize = (12,4))
sns.set(font_scale=1.5, palette= "Reds")

# Gráfico principal y opciones Seaborn (o Matplotlib a través)

sns.histplot(ax= ax[0], data = df, x = 'total_bill')
sns.histplot(ax= ax[1], data = df, x = 'tip')

# Opciones Matplotlib

ax[0].set_title('Grafico 1', fontsize = 20)
ax[0].set_xlabel('Eje x grafico 1', fontsize = 14)
ax[0].set_ylabel('Eje y grafico 1', fontsize = 14);

ax[1].set_title('Grafico 2', fontsize = 20)
ax[1].set_xlabel('Eje x grafico 2', fontsize = 14)
ax[1].set_ylabel('Eje y grafico 2', fontsize = 14);
