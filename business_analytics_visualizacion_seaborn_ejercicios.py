print("******************")
print("BUSINESS ANALYTICS")
print("******************")

print("**************************************")
print("VISUALIZACIÓN CON SEABORN - EJERCICIOS")
print("**************************************")

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os 

# %matplotlib inline. Es para decirle cómo tiene que sacar los gráficos.
# En este caso significa que los saque como gráficos estáticos integrados en el propio notebook (de tal forma que se guarde y distribuya más fácilmente).

pd.options.display.min_rows = 6

# Importación de los datos para usar de ejemplos
df = sns.load_dataset('tips')
print(df.head())

# Crea un gráfico de líneas sobre la variable total_bill.

plt.figure(figsize=(12, 6))
sns.lineplot(data=df.total_bill, color='blue', label='Total Bill')
plt.title("Total Bill Over Observations")
plt.xlabel("Observation")
plt.ylabel("Total Bill ($)")
plt.grid(True)
plt.tight_layout()
plt.show()

# Sobre el gráfico anterior: haz la línea de tamaño 5 que sea de rayas - puntos y que sea roja

plt.figure(figsize=(12, 6))
sns.lineplot(data=df.total_bill, color='red', label='Total Bill', linewidth=5, linestyle='-.')
plt.title("Total Bill Over Observations")
plt.xlabel("Observation")
plt.ylabel("Total Bill ($)")
plt.grid(True)
plt.tight_layout()
plt.show()

# Ahora sobre el mismo gráfico inicial:

# - haz que el tamaño varíe según el sexo
# - haz que el estilo varíe según si es fumador
# - haz que el color varíe según el sexo

# NOTA: el gráfico no será legible, pero el ejercicio pretende destacar la diferencia en los parámetros a usar si queremos definir directamente los mismos o si queremos asociarlos a otras variables.

plt.figure(figsize=(12, 6))

# Usando los parámetros hue, style, y size en Seaborn
sns.lineplot(data=df, x=df.index, y='total_bill', hue='sex', style='smoker', size='sex',
             sizes={'Male': 5, 'Female': 2.5}, palette={'Male': 'blue', 'Female': 'red'})

plt.title("Total Bill Over Observations")
plt.xlabel("Observation")
plt.ylabel("Total Bill ($)")
plt.grid(True)
plt.tight_layout()
plt.legend(title='Legend', loc='upper left', bbox_to_anchor=(1, 1))
plt.show()

# Haz un histograma del total de las facturas.

plt.figure(figsize=(10, 6))
sns.histplot(df['total_bill'], bins=20, color='skyblue', kde=True)
plt.title("Histogram of Total Bill")
plt.xlabel("Total Bill ($)")
plt.ylabel("Frequency")
plt.grid(axis='y')
plt.tight_layout()
plt.show()

# Ahora representa y superpón los histogramas del total de las facturas para hombres y mujeres.

plt.figure(figsize=(10, 6))

# Histograma para hombres
sns.histplot(df[df['sex'] == 'Male']['total_bill'], bins=20, color='blue', label='Male', kde=True, alpha=0.5)

# Histograma para mujeres
sns.histplot(df[df['sex'] == 'Female']['total_bill'], bins=20, color='red', label='Female', kde=True, alpha=0.5)

plt.title("Histogram of Total Bill by Gender")
plt.xlabel("Total Bill ($)")
plt.ylabel("Frequency")
plt.grid(axis='y')
plt.legend()
plt.tight_layout()
plt.show()

# El alpha de Seaborn en los histogramas parece que lo que hace es hacer los colores más pálidos, pero no es una trasparencia real.
# Para compararlo mejor prueba a generar un df para hombres y otro para mujeres (copia y pega el código inferior) y luego genera dos gráficos en la misma fila, uno para hombres (en azul) y el otro para mujeres (en rojo).

# df_h = df[df.sex == 'Male']
# df_m = df[df.sex == 'Female']

df_h = df[df.sex == 'Male']
df_m = df[df.sex == 'Female']

# Creando dos gráficos en la misma fila: uno para hombres y el otro para mujeres
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Histograma para hombres
sns.histplot(df_h['total_bill'], bins=20, color='blue', label='Male', kde=True, ax=axes[0])
axes[0].set_title("Histogram of Total Bill for Males")
axes[0].set_xlabel("Total Bill ($)")
axes[0].set_ylabel("Frequency")
axes[0].grid(axis='y')
axes[0].legend()

# Histograma para mujeres
sns.histplot(df_m['total_bill'], bins=20, color='red', label='Female', kde=True, ax=axes[1])
axes[1].set_title("Histogram of Total Bill for Females")
axes[1].set_xlabel("Total Bill ($)")
axes[1].set_ylabel("Frequency")
axes[1].grid(axis='y')
axes[1].legend()

plt.tight_layout()
plt.show()

# O para no tener que estar separando los datos, intenta generar directamente los dos gráficos usando el FacetGrid.

g = sns.FacetGrid(df, col="sex", hue="sex", palette={"Male": "blue", "Female": "red"}, height=6, aspect=1)
g.map(sns.histplot, "total_bill", bins=20, kde=True)

# Configurando los títulos y etiquetas
g.set_axis_labels("Total Bill ($)", "Frequency")
g.set_titles("Gender = {col_name}")
g.add_legend(title="Gender")

plt.tight_layout()
plt.show()

# Crea un gráfico de densidad sobre las propinas.

plt.figure(figsize=(10, 6))
sns.kdeplot(df['tip'], shade=True, color="purple")
plt.title("Density Plot of Tips")
plt.xlabel("Tip ($)")
plt.ylabel("Density")
plt.grid(axis='y')
plt.tight_layout()
plt.show()

# Diferencia sobre el gráfico anterior la distribución por sexo usando el color.

plt.figure(figsize=(10, 6))

# KDE para hombres
sns.kdeplot(df[df['sex'] == 'Male']['tip'], shade=True, color="blue", label="Male")

# KDE para mujeres
sns.kdeplot(df[df['sex'] == 'Female']['tip'], shade=True, color="red", label="Female")

plt.title("Density Plot of Tips by Gender")
plt.xlabel("Tip ($)")
plt.ylabel("Density")
plt.grid(axis='y')
plt.legend()
plt.tight_layout()
plt.show()

# Representa en un gráfico de barras cuantas compras ha habido en cada día de la semana.

plt.figure(figsize=(10, 6))
sns.countplot(data=df, x='day', order=df['day'].value_counts().index, palette="viridis")
plt.title("Number of Purchases by Day of the Week")
plt.xlabel("Day of the Week")
plt.ylabel("Number of Purchases")
plt.grid(axis='y')
plt.tight_layout()
plt.show()

# Mismo gráfico pero en porcentajes.
# NOTA: es posible que tengas que precalcularlos.

# Calculando los porcentajes de compras por día de la semana
total_purchases = len(df)
purchases_by_day = df['day'].value_counts()
percentage_by_day = (purchases_by_day / total_purchases) * 100

plt.figure(figsize=(10, 6))
sns.barplot(x=percentage_by_day.index, y=percentage_by_day.values, palette="viridis")
plt.title("Percentage of Purchases by Day of the Week")
plt.xlabel("Day of the Week")
plt.ylabel("Percentage (%)")
plt.grid(axis='y')
plt.tight_layout()
plt.show()

# Crea un boxplot para analizar las diferencias entre el tamaño de las facturas por día de la semana.

plt.figure(figsize=(10, 6))
sns.boxplot(data=df, x='day', y='total_bill', palette="coolwarm")
plt.title("Boxplot of Total Bill by Day of the Week")
plt.xlabel("Day of the Week")
plt.ylabel("Total Bill ($)")
plt.grid(axis='y')
plt.tight_layout()
plt.show()

# Crea un gráfico de dispersión para ver la relación entre el total de la factura y las propinas, y diferencia cada punto con colores en función de si es hombre o mujer.
# Añade también una curva de regresión para cada uno.

plt.figure(figsize=(12, 7))
sns.lmplot(data=df, x='total_bill', y='tip', hue='sex', palette={'Male': 'blue', 'Female': 'red'}, aspect=1.5)

plt.title("Scatter Plot of Total Bill vs. Tip by Gender with Regression Line")
plt.xlabel("Total Bill ($)")
plt.ylabel("Tip ($)")
plt.grid(True)
plt.tight_layout()
plt.show()

# El mismo gráfico pero aplícale el estilo 'dark'
# Resetea el estilo y vuelve a generar el gráfico.

sns.set_style("dark")
lm_plot_dark = sns.lmplot(data=df, x='total_bill', y='tip', hue='sex', palette={'Male': 'blue', 'Female': 'red'}, aspect=1.5)
lm_plot_dark.fig.suptitle("Scatter Plot of Total Bill vs. Tip by Gender with Regression Line (Dark Style)")
plt.xlabel("Total Bill ($)")
plt.ylabel("Tip ($)")
plt.grid(True)
plt.tight_layout()
plt.show()

sns.reset_defaults()
