import os
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px 

st.set_page_config(layout="wide")

st.subheader("Análisis Exploratorio del Dataset: Impacto del Trabajo Remoto en la Salud Mental")




tad_descripcion, tab_Análisis_Exploratorio, tab_Filtrado_Básico, tab_Filtro_Final_Dinámico = st.tabs(["Descripción", "Análisis Exploratorio", "Filtrado Básico", "Filtro Final Dinámico"])

#----------------------------------------------------------
#Generador de datos
#----------------------------------------------------------
with tad_descripcion:      

    st.markdown('''
    ## Este dataset contiene información sobre el impacto del trabajo remoto en la salud mental. 
Contiene datos sobre:

### Introducción

* **Ubicación de trabajo:** Indica si los empleados trabajan desde casa o en la oficina.
* **Nivel de Estrés:**  Mide el nivel de estrés percibido por los empleados.
* **Nivel de Satisfacción con el Trabajo:**  Mide la satisfacción de los empleados con su trabajo actual.
* **Equilibrio entre la Vida Laboral y Personal:** Mide el equilibrio entre la vida laboral y personal percibido por los empleados.

### Desarrollo

* **Work_Location:** Ubicación de trabajo (Home, Office)
* **Stress_Level:** Nivel de estrés (1-5)
* **Job_Satisfaction:** Nivel de satisfacción con el trabajo (1-5)
* **Work_Life_Balance:** Equilibrio entre la vida laboral y personal (1-5) 

### Conclusión

* Identificar las tendencias en la salud mental de los empleados en entornos de trabajo remotos.
* Explorar la relación entre la ubicación de trabajo y el nivel de estrés, la satisfacción laboral y el equilibrio entre la vida laboral y personal. 
* Proporcionar información para mejorar la gestión de la salud mental de los empleados en el contexto del trabajo remoto.
    ''')  
    
    # Cargar el dataset CSV
current_dir = os.path.dirname(__file__)
file_path = os.path.join(current_dir, "..", "static", "datasets", "Impact_of_Remote_Work_on_Mental_Health.csv")

@st.cache_data
def load_data(file_path):
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        st.error("Archivo no encontrado. Verifica la ruta.")
        return pd.DataFrame()  # Retorna un DataFrame vacío en caso de error

df = load_data(file_path)

# Mostrar el DataFrame
st.write("Vista General del Dataset:")
st.dataframe(df)

# Verificar datos antes de continuar
if df.empty:
    st.warning("No se pudo cargar el dataset. Deteniendo análisis.")
else:
    # 1. Valores Faltantes
    st.write("Valores faltantes por columna:")
    st.write(df.isnull().sum())

    # 2. Estadísticas Descriptivas
    st.write("Estadísticas descriptivas:")
    st.write(df.describe())

    # Funciones para visualización
    def plot_histogram(column):
        plt.figure(figsize=(4, 2))
        sns.histplot(df[column].dropna(), bins=20, kde=True)
        st.pyplot(plt)
        st.markdown(f"**Histograma de {column}:** Este histograma muestra la distribución de los valores de la variable {column}.")
        plt.close()

    def plot_boxplot(column):
        plt.figure(figsize=(4, 2))
        sns.boxplot(x=df[column].dropna())
        st.pyplot(plt)
        st.markdown(f"**Boxplot de {column}:** Este boxplot muestra la distribución de los valores de la variable {column}, incluyendo la media, los cuartiles y los valores atípicos.")
        plt.close()  



#----------------------------------------------------------
#Analítica 1
#----------------------------------------------------------
with tab_Análisis_Exploratorio:    
    st.title("Análisis Exploratorio") 
    # 3. Distribución de Variables Numéricas
    st.write("Distribución de variables numéricas:")
    num_columns = df.select_dtypes(include=['float64', 'int64']).columns
    for col in num_columns:
        st.write(f"Distribución de {col}")
        plot_histogram(col)
        plot_boxplot(col)

    # 4. Mapa de Calor de Correlaciones
    st.write("Mapa de calor de correlaciones entre variables numéricas:")
    num_df = df.select_dtypes(include=['float64', 'int64'])
    corr = num_df.corr()

    def plot_heatmap(corr):
        plt.figure(figsize=(4, 2))
        sns.heatmap(corr, annot=True, cmap='coolwarm', linewidths=0.5)
        st.pyplot(plt)
        st.markdown("**Mapa de calor de correlaciones:** Este mapa de calor muestra la correlación entre las variables numéricas del dataset. Las celdas más rojas indican una correlación positiva más fuerte, mientras que las celdas más azules indican una correlación negativa más fuerte.")
        plt.close()

    plot_heatmap(corr)

    # 5. Visualización de Variables Categóricas
    st.write("Distribución de variables categóricas:")
    cat_columns = df.select_dtypes(include=['object']).columns
    for col in cat_columns:
        st.write(f"Frecuencia de {col}")
        fig, ax = plt.subplots()
        sns.countplot(data=df, y=col, ax=ax)
        st.pyplot(fig)
        st.markdown(f"**Frecuencia de {col}:** Este gráfico de barras muestra la frecuencia de cada categoría en la variable {col}.")
        plt.close()

    # 6. Histograma de Nivel de Estrés
    st.write("Histograma de Nivel de Estrés:")
    if 'Stress_Level' in df.columns:
        plot_histogram('Stress_Level')

    # 7. Filtrado por Ubicación de Trabajo
    if 'Work_Location' in df.columns:
        location = st.selectbox("Selecciona una ubicación para filtrar los datos", df['Work_Location'].dropna().unique())
        filtered_df = df[df['Work_Location'] == location]
        st.write("Datos filtrados por ubicación de trabajo seleccionada:")
        st.dataframe(filtered_df)

    # Asegurarnos de que la columna 'Stress_Level' sea numérica
    df['Stress_Level'] = pd.to_numeric(df['Stress_Level'], errors='coerce')

    # 8. Análisis Bivariado - Promedio de Nivel de Estrés por Ubicación de Trabajo
    if 'Stress_Level' in df.columns and 'Work_Location' in df.columns:
        st.write("Promedio de Nivel de Estrés por Ubicación de Trabajo:")
        location_stress = df.groupby("Work_Location")["Stress_Level"].mean()
        st.bar_chart(location_stress)
        st.markdown("**Promedio de Nivel de Estrés por Ubicación de Trabajo:** Este gráfico de barras muestra el promedio del nivel de estrés para cada ubicación de trabajo (Home u Office).")
    
with tab_Filtrado_Básico:
    st.title("Filtro Básico")
    st.markdown("""
    Permite filtrar datos usando condiciones simples.
    """)

    col1, col2 = st.columns(2)  # Removed the operator column

    column_to_filter = col1.selectbox("Selecciona la columna:", df.columns)

    # Determine input type based on column type
    if pd.api.types.is_numeric_dtype(df[column_to_filter]):
        filter_value = col2.number_input("Introduce el valor:", value=0)
    elif pd.api.types.is_bool_dtype(df[column_to_filter]):
        filter_value = col2.selectbox("Introduce el valor:", [True, False])
    else:
        filter_value = col2.text_input("Introduce el valor:")

    try:
        if filter_value is not None:
            if pd.api.types.is_numeric_dtype(df[column_to_filter]) or pd.api.types.is_bool_dtype(df[column_to_filter]):
                filter_condition = f"{column_to_filter} == {filter_value}"
            else: #String type
                filter_condition = f"{column_to_filter} == '{filter_value}'"

            filtered_df = df.query(filter_condition)
            st.dataframe(filtered_df)

            # Add bar chart (only if appropriate)
            if len(filtered_df) > 0 and not pd.api.types.is_numeric_dtype(df[column_to_filter]):
                plt.figure(figsize=(6, 4))
                sns.countplot(x=filtered_df[column_to_filter])
                st.pyplot(plt)
                plt.close()

    except (KeyError, ValueError, TypeError):
        st.error("Error en el filtro. Verifica la columna y el valor ingresado.")

#----------------------------------------------------------
#Analítica 3
#----------------------------------------------------------
with tab_Filtro_Final_Dinámico:
    st.title("Filtro Final Dinámico")
    st.markdown("""
    Muestra un resumen dinámico del DataFrame filtrado.
    """)

    if not filtered_df.empty:  
        st.write("Resumen del DataFrame filtrado:")
        st.dataframe(filtered_df)
        
       
        st.write("Gráfico de barras:")
        if 'Work_Location' in filtered_df.columns:
            location_counts = filtered_df['Work_Location'].value_counts()
            st.bar_chart(location_counts)

        st.write("Gráfico de dona:")
        if 'Work_Location' in filtered_df.columns:
            fig = px.pie(values=filtered_df['Work_Location'].value_counts(), 
                         names=filtered_df['Work_Location'].value_counts().index,
                         title='Distribución de la Ubicación de Trabajo')
            st.plotly_chart(fig)
        
        st.write("Estadísticas descriptivas:")
        st.dataframe(filtered_df.describe())
    else:
        st.write("Aplica un filtro en la pestaña 'Filtro Básico' para ver el resumen.")




    




