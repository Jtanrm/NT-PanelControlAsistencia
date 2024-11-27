import streamlit as st
import pandas as pd
from googleapiclient.discovery import build
from google.oauth2 import service_account
import matplotlib.pyplot as plt
import seaborn as sns
import webbrowser
import streamlit.components.v1 as components
from PIL import Image


st.set_page_config(layout="wide")

st.subheader("Analizador de Datos de Google Sheets")

# Imagen de fondo
st.markdown("""
""", unsafe_allow_html=True)
# Cargar la imagen original
image_sheet = Image.open("./static/images/googlesheet.png")

# Redimensionar la imagen a 100x500 píxeles
image_resized = image_sheet.resize((310, 150))  # (ancho, alto)

# Mostrar la imagen redimensionada
st.image(image_resized)



st.markdown("""
Este código lee datos de una hoja de cálculo de Google Sheets llamada "Sheet1", los procesa con Pandas y actualiza una segunda hoja llamada "Sheet2" con nuevos datos. La interfaz de usuario de Streamlit permite al usuario ingresar el ID de la hoja de cálculo y visualizar los datos procesados.            
""")  

st.subheader("Analisis de hurtos de motocicletas y automotores en Antioquia")

# Imagen de fondo
st.markdown("""
""", unsafe_allow_html=True)
# Cargar la imagen original
image = Image.open("./static/images/dijin.png")

# Redimensionar la imagen a 100x500 píxeles
image_resized = image.resize((200, 200))  # (ancho, alto)

# Mostrar la imagen redimensionada
st.image(image_resized)

st.markdown("""
En este conjunto de datos la ciudadanía puede encontrará información del delito de hurto en Antioquia a través de las modalidades de motocicletas y automotores desde 01 de enero del año 2020 al 30 de abril del año 2024.

Fuente: DIJIN - Policía Nacional. Cifras sujetas a variación, en proceso de integración y consolidación con información de fiscalía general de la nación.

""")

st.text('------------------------------------')

st.text('Link archivo en Google Sheet')
st.text('https://docs.google.com/spreadsheets/d/1dVyVkVs4ax-dywYCvo0VCeyi4-yHiUTwMebZ0UyOW8Y/edit?usp=sharing')

# # Crear el botón
# if st.button('Abrir archivo en Google Sheets'):
#     # Abrir la URL cuando el botón es presionado
#     webbrowser.open('https://docs.google.com/spreadsheets/d/1dVyVkVs4ax-dywYCvo0VCeyi4-yHiUTwMebZ0UyOW8Y/edit?usp=sharing')

st.markdown(
    """
    <a href="https://docs.google.com/spreadsheets/d/1dVyVkVs4ax-dywYCvo0VCeyi4-yHiUTwMebZ0UyOW8Y/edit?usp=sharing" target="_blank">
            Abrir archivo en Google Sheets
    </a>
    """, 
    unsafe_allow_html=True
)

st.text('------------------------------------')

st.text('Id documento datos_proyecto')
st.text('1dVyVkVs4ax-dywYCvo0VCeyi4-yHiUTwMebZ0UyOW8Y') 

# Entrada del ID del documento de Google Sheets
SPREADSHEET_ID = st.text_input("ID hoja de cálculo")
RANGE1 = "Sheet1!A:O"
RANGE2 = "Sheet2!A:O"

google_sheet_credentials = st.secrets["GOOGLE_SHEET_CREDENTIALS"]
secrets_dict = google_sheet_credentials.to_dict()     
creds = None
creds = service_account.Credentials.from_service_account_info(secrets_dict, scopes=["https://www.googleapis.com/auth/spreadsheets"])
service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()

def read_sheet():
    """Lee los datos de la primera hoja."""
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE1).execute()
    values = result.get('values', [])
    df = pd.DataFrame(values[1:], columns=values[0])  # Asumiendo que la primera fila son los encabezados

    # Convertir la columna 'FECHA HECHO' a tipo datetime
    df['FECHA HECHO'] = pd.to_datetime(df['FECHA HECHO'], format='%d/%m/%Y')
    return df

def update_sheet(df):
    """Actualiza la segunda hoja con el DataFrame proporcionado."""
    # Convertir todos los valores a string para evitar problemas de serialización
    body = {'values': df.astype(str).values.tolist()}
    result = sheet.values().update(
        spreadsheetId=SPREADSHEET_ID, range=RANGE2,
        valueInputOption="USER_ENTERED", body=body).execute()
    return result

def clean_data(df):
    """Convierte las columnas relevantes a tipo numérico y maneja errores."""
    # Limpiar la columna 'CANTIDAD' para asegurarse de que es numérica
    df['CANTIDAD'] = pd.to_numeric(df['CANTIDAD'], errors='coerce')  # Convierte y reemplaza errores con NaN
    return df

def analyze_data(df):
    """Realiza los análisis solicitados sobre el DataFrame y devuelve resultados con descripciones."""
    results = []

    # Limpiar los datos
    df = clean_data(df)

    # Asegurarse de que 'AÑO' exista como columna (extraer el año de 'FECHA HECHO')
    df['AÑO'] = df['FECHA HECHO'].dt.year

    # Análisis 1: 5 primeros Municipios con mayor número de HURTO AUTOMOTORES
    hurto_automotores = df[df['TIPO DE HURTO'] == 'HURTO AUTOMOTORES']
    hurto_automotores_municipio = hurto_automotores.groupby('MUNICIPIO')['CANTIDAD'].sum().reset_index()
    top_5_hurtos_automotores = hurto_automotores_municipio.sort_values(by='CANTIDAD', ascending=False).head(5)
    results.append(['Top 5 Municipios con Hurtos Automotores', top_5_hurtos_automotores.to_string(index=False)])

     # Graficar los 3 primeros Municipios con mayor número de HURTO AUTOMOTORES
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(data=top_5_hurtos_automotores, x='MUNICIPIO', y='CANTIDAD', ax=ax, palette='viridis')
    ax.set_title('Top 5 Municipios con Hurtos Automotores')
    st.pyplot(fig)

    # Análisis 2: 5 primeros Municipios con mayor número de HURTO MOTOCICLETAS
    hurto_motocicletas = df[df['TIPO DE HURTO'] == 'HURTO MOTOCICLETAS']
    hurto_motocicletas_municipio = hurto_motocicletas.groupby('MUNICIPIO')['CANTIDAD'].sum().reset_index()
    top_5_hurtos_motocicletas = hurto_motocicletas_municipio.sort_values(by='CANTIDAD', ascending=False).head(5)
    results.append(['Top 5 Municipios con Hurtos Motocicletas', top_5_hurtos_motocicletas.to_string(index=False)])

    # Graficar los 3 primeros Municipios con mayor número de HURTO MOTOCICLETAS
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(data=top_5_hurtos_motocicletas, x='MUNICIPIO', y='CANTIDAD', ax=ax, palette='magma')
    ax.set_title('Top 5 Municipios con Hurtos Motocicletas')
    st.pyplot(fig)

    # Análisis 3: Cuántos hurtos no se reportaron por año
    hurto_no_reportado = df[df['ARMAS MEDIOS'] == 'SIN EMPLEO DE ARMAS']
    hurto_no_reportado_anual = hurto_no_reportado.groupby('AÑO')['CANTIDAD'].sum().reset_index()
    results.append(['Hurtos No Reportados por Año', hurto_no_reportado_anual.to_string(index=False)])

     # Graficar los hurtos no reportados por año
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.lineplot(data=hurto_no_reportado_anual, x='AÑO', y='CANTIDAD', ax=ax, marker='o', color='orange')
    ax.set_title('Hurtos No Reportados por Año')
    st.pyplot(fig)

    # Análisis 4: Hurtos de automotores realizados con LLAVE MAESTRA por cada año
    hurto_automotores_llave_maestra = hurto_automotores[hurto_automotores['ARMAS MEDIOS'] == 'LLAVE MAESTRA']
    hurto_automotores_llave_maestra_anual = hurto_automotores_llave_maestra.groupby('AÑO')['CANTIDAD'].sum().reset_index()
    results.append(['Hurtos Automotores con Llave Maestra por Año', hurto_automotores_llave_maestra_anual.to_string(index=False)])

    # Graficar los hurtos de automotores con llave maestra por año
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.lineplot(data=hurto_automotores_llave_maestra_anual, x='AÑO', y='CANTIDAD', ax=ax, marker='o', color='red')
    ax.set_title('Hurtos Automotores con Llave Maestra por Año')
    st.pyplot(fig)

    # Análisis 5: Hurtos de automotores realizados con ARMA DE FUEGO por cada año
    hurto_automotores_arma_fuego = hurto_automotores[hurto_automotores['ARMAS MEDIOS'] == 'ARMA DE FUEGO']
    hurto_automotores_arma_fuego_anual = hurto_automotores_arma_fuego.groupby('AÑO')['CANTIDAD'].sum().reset_index()
    results.append(['Hurtos Automotores con Arma de Fuego por Año', hurto_automotores_arma_fuego_anual.to_string(index=False)])

     # Graficar los hurtos de automotores con arma de fuego por año
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.lineplot(data=hurto_automotores_arma_fuego_anual, x='AÑO', y='CANTIDAD', ax=ax, marker='o', color='green')
    ax.set_title('Hurtos Automotores con Arma de Fuego por Año')
    st.pyplot(fig)

    # Análisis 6: Hurtos de automotores realizados sin empleo de armas por cada año
    hurto_automotores_sin_armas = hurto_automotores[hurto_automotores['ARMAS MEDIOS'] == 'SIN EMPLEO DE ARMAS']
    hurto_automotores_sin_armas_anual = hurto_automotores_sin_armas.groupby('AÑO')['CANTIDAD'].sum().reset_index()
    results.append(['Hurtos Automotores Sin Empleo de Armas por Año', hurto_automotores_sin_armas_anual.to_string(index=False)])

    # Graficar los hurtos de automotores sin armas por año
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.lineplot(data=hurto_automotores_sin_armas_anual, x='AÑO', y='CANTIDAD', ax=ax, marker='o', color='blue')
    ax.set_title('Hurtos Automotores Sin Empleo de Armas por Año')
    st.pyplot(fig)

    # Análisis 7: Año con mayor número de hurtos de automotores
    año_max_hurto_automotores = hurto_automotores.groupby('AÑO')['CANTIDAD'].sum().idxmax()
    results.append(['Año con Mayor Número de Hurtos de Automotores', año_max_hurto_automotores])

    # Análisis 8: Año con mayor número de hurtos de motocicletas
    año_max_hurto_motocicletas = hurto_motocicletas.groupby('AÑO')['CANTIDAD'].sum().idxmax()
    results.append(['Año con Mayor Número de Hurtos de Motocicletas', año_max_hurto_motocicletas])

    # Análisis 9: Número de hurtos por tipo de arma/medio por cada año
    hurtos_por_tipo_armas = df.groupby(['ARMAS MEDIOS', 'AÑO'])['CANTIDAD'].sum().reset_index()
    hurtos_tipo_armas_interes = hurtos_por_tipo_armas[hurtos_por_tipo_armas['ARMAS MEDIOS'].isin(['SIN EMPLEO DE ARMAS', 'ARMA DE FUEGO', 'LLAVE MAESTRA'])]
    results.append(['Número de Hurtos por Tipo de Arma/Medio por Año', hurtos_tipo_armas_interes.to_string(index=False)])

    # Graficar los hurtos por tipo de arma/medio
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(data=hurtos_tipo_armas_interes, x='AÑO', y='CANTIDAD', hue='ARMAS MEDIOS', marker='o', ax=ax)
    ax.set_title('Número de Hurtos por Tipo de Arma/Medio por Año')
    st.pyplot(fig)

    # Convertir resultados a DataFrame para visualización
    results_df = pd.DataFrame(results, columns=['Descripción', 'Valor'])
    
    return results_df

# Botón para realizar el análisis
if st.button("Analizar datos de Google Sheet"):
    if SPREADSHEET_ID:
        df = read_sheet()
        if not df.empty:
            st.header("Datos de la Hoja 1")
            st.dataframe(df)

            # Realizar el análisis
            results_df = analyze_data(df)
            st.header("Resultados del Análisis")
            st.dataframe(results_df)

            # Actualizar la segunda hoja con los resultados
            update_sheet(results_df)
            st.success("Hoja actualizada con los resultados del análisis.")

        else:
            st.warning("La hoja está vacía o no se pudo leer.")
    else:
        st.warning("Por favor, ingresa un ID de hoja de cálculo válido.")
