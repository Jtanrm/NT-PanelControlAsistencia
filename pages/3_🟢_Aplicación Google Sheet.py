import streamlit as st
import pandas as pd
from googleapiclient.discovery import build
from google.oauth2 import service_account


st.set_page_config(layout="wide")

st.subheader("Analizador de Datos de Google Sheets")

st.markdown("""
Este código lee datos de una hoja de cálculo de Google Sheets llamada "Sheet1", los procesa con Pandas y actualiza una segunda hoja llamada "Sheet2" con nuevos datos. La interfaz de usuario de Streamlit permite al usuario ingresar el ID de la hoja de cálculo y visualizar los datos procesados.            
    """)  

st.text('id documento datos_proyecto')
st.text('1dVyVkVs4ax-dywYCvo0VCeyi4-yHiUTwMebZ0UyOW8Y') 

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = st.text_input("ID  hoja de cálculo")
RANGE1 = "Sheet1!A:O"
RANGE2 = "Sheet2!A:O"

google_sheet_credentials = st.secrets["GOOGLE_SHEET_CREDENTIALS"]  
secrets_dict = google_sheet_credentials.to_dict()     
creds = None
creds = service_account.Credentials.from_service_account_info(secrets_dict, scopes=SCOPES)
service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()

# def read_sheet():
#     result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE1).execute()      
#     values = result.get('values', [])
#     df = pd.DataFrame(values)
#     return df

# def update_sheet(df):
#     body = {'values': df.values.tolist()}
#     result = sheet.values().update(
#         spreadsheetId=SPREADSHEET_ID, range=RANGE2,
#         valueInputOption="USER_ENTERED", body=body).execute()
#     return result

# # Botón para leer
# if st.button("Analizar datos de Google Sheet"):  
#     df = read_sheet()
#     st.header("Datos hoja1")
#     st.dataframe(df)
#     df_update = pd.DataFrame({
#         'Columna1': ['Nuevo1', 'Nuevo2', 'Nuevo3'],
#         'Columna2': [1, 2, 3],
#         'Columna3': ['A', 'B', 'C'],
#         'Columna4': ['#', '%', '=']
#     })

#      # Actualizar la hoja de cálculo
#     result = update_sheet(df_update)
#     st.header("Datos hoja2")
#     st.success(f"Hoja actualizada. {result.get('updatedCells')} celdas actualizadas.")

#     # Mostrar el DataFrame actualizado
#     st.dataframe(df_update)

# def read_sheet():
#     """Lee los datos de la primera hoja."""
#     result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE1).execute()
#     values = result.get('values', [])
#     df = pd.DataFrame(values[1:], columns=values[0])  # Asumiendo que la primera fila son los encabezados
#     return df

# def update_sheet(df):
#     """Actualiza la segunda hoja con el DataFrame proporcionado."""
#     body = {'values': df.values.tolist()}
#     result = sheet.values().update(
#         spreadsheetId=SPREADSHEET_ID, range=RANGE2,
#         valueInputOption="USER_ENTERED", body=body).execute()
#     return result

# def analyze_data(df):
#     """Realiza un análisis simple sobre el DataFrame."""
#     # Ejemplo: contar la cantidad de valores únicos en cada columna
#     analysis = df.nunique().reset_index()
#     analysis.columns = ['Columna', 'Valores Únicos']
#     return analysis

# # Botón para realizar el análisis
# if st.button("Analizar datos de Google Sheet"):
#     if SPREADSHEET_ID:
#         df = read_sheet()
#         if not df.empty:
#             st.header("Datos de la Hoja 1")
#             st.dataframe(df)

#             # # Análisis de datos
#             # analysis_df = analyze_data(df)
#             # st.header("Análisis de Datos")
#             # st.dataframe(analysis_df)

#             # # Actualizar la segunda hoja con los resultados del análisis
#             # result = update_sheet(analysis_df)
#             # st.success(f"Hoja actualizada. {result.get('updatedCells')} celdas actualizadas.")
#             # st.header("Resultados en Hoja 2")
#             # st.dataframe(analysis_df)

            


#         else:
#             st.warning("La hoja está vacía o no se pudo leer.")
#     else:
#         st.warning("Por favor, ingresa un ID de hoja de cálculo válido.")




# #Funciona
# def read_sheet():
#     """Lee los datos de la primera hoja."""
#     result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE1).execute()
#     values = result.get('values', [])
#     df = pd.DataFrame(values[1:], columns=values[0])  # Asumiendo que la primera fila son los encabezados
#     return df

# def update_sheet(df):
#     """Actualiza la segunda hoja con el DataFrame proporcionado."""
#     # Convertir todos los valores a string para evitar problemas de serialización
#     body = {'values': df.astype(str).values.tolist()}
#     result = sheet.values().update(
#         spreadsheetId=SPREADSHEET_ID, range=RANGE2,
#         valueInputOption="USER_ENTERED", body=body).execute()
#     return result

# def clean_data(df):
#     """Convierte las columnas relevantes a tipo numérico y maneja errores."""
#     numeric_columns = ['Población', 'Hogares con acceso a internet', 'Penetración de internet (%)',
#                        'Uso de internet', 'Dispositivos móviles', 'Uso de teléfonos inteligentes (%)',
#                        'Acceso a computadores (%)', 'Uso de redes sociales (%)', 'Compras online (%)',
#                        'Nivel educativo', 'Edad promedio', 'Ingresos promedio']

#     for col in numeric_columns:
#         df[col] = pd.to_numeric(df[col], errors='coerce')  # Convierte y reemplaza errores con NaN

#     return df

# def analyze_data(df):
#     """Realiza los análisis solicitados sobre el DataFrame."""
#     results = {}

#     # Limpiar los datos
#     df = clean_data(df)

#     # Región con menor penetración de internet
#     min_penetration = df.loc[df['Penetración de internet (%)'].idxmin(), ['Región', 'Penetración de internet (%)']]
#     results['Región con menor penetración de internet'] = min_penetration

#     # Edad promedio por departamento
#     edad_promedio = df.groupby('Departamento')['Edad promedio'].mean().reset_index()
#     results['Edad promedio por departamento'] = edad_promedio

#     # Agrupar por departamento, los municipios con mayor uso de internet
#     municipios_uso_internet = df.groupby('Departamento').apply(lambda x: x.loc[x['Uso de internet'].idxmax(), ['Municipio', 'Uso de internet']]).reset_index(drop=True)
#     results['Municipios con mayor uso de internet por departamento'] = municipios_uso_internet

#     # Departamentos con mayor uso de dispositivos móviles
#     max_dispositivos_movil = df.groupby('Departamento')['Dispositivos móviles'].sum().reset_index()
#     max_dispositivos_movil = max_dispositivos_movil.loc[max_dispositivos_movil['Dispositivos móviles'].idxmax()]
#     results['Departamentos con mayor uso de dispositivos móviles'] = max_dispositivos_movil

#     # Organizar las regiones de menor a mayor según el nivel educativo
#     nivel_educativo = df.groupby('Región')['Nivel educativo'].mean().reset_index()
#     nivel_educativo = nivel_educativo.sort_values('Nivel educativo')
#     results['Regiones organizadas por nivel educativo'] = nivel_educativo

#     # Municipios con mayores compras online
#     mayores_compras_online = df.loc[df['Compras online (%)'].idxmax(), ['Municipio', 'Compras online (%)']]
#     results['Municipios con mayores compras online'] = mayores_compras_online

#     return results

# # Botón para realizar el análisis
# if st.button("Analizar datos de Google Sheet"):
#     if SPREADSHEET_ID:
#         df = read_sheet()
#         if not df.empty:
#             st.header("Datos de la Hoja 1")
#             st.dataframe(df)

#             # Análisis de datos
#             results = analyze_data(df)
#             st.header("Resultados del Análisis")
#             for title, result_df in results.items():
#                 st.subheader(title)
#                 st.dataframe(result_df)

#             # Actualizar la segunda hoja con el análisis (concatenamos resultados)
#             combined_results = pd.concat(results.values(), axis=0, ignore_index=True)
#             update_sheet(combined_results)
#             st.success("Hoja actualizada con los resultados del análisis.")
#         else:
#             st.warning("La hoja está vacía o no se pudo leer.")
#     else:
#         st.warning("Por favor, ingresa un ID de hoja de cálculo válido.")

def read_sheet():
    """Lee los datos de la primera hoja."""
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE1).execute()
    values = result.get('values', [])
    df = pd.DataFrame(values[1:], columns=values[0])  # Asumiendo que la primera fila son los encabezados
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
    numeric_columns = ['Población', 'Hogares con acceso a internet', 'Penetración de internet (%)',
                       'Uso de internet', 'Dispositivos móviles', 'Uso de teléfonos inteligentes (%)',
                       'Acceso a computadores (%)', 'Uso de redes sociales (%)', 'Compras online (%)',
                       'Nivel educativo', 'Edad promedio', 'Ingresos promedio']

    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')  # Convierte y reemplaza errores con NaN

    return df

def analyze_data(df):
    """Realiza los análisis solicitados sobre el DataFrame y devuelve resultados con descripciones."""
    results = []

    # Limpiar los datos
    df = clean_data(df)

    # Análisis
    # Región con menor penetración de internet
    min_penetration = df.loc[df['Penetración de internet (%)'].idxmin(), ['Región', 'Penetración de internet (%)']]
    results.append(['Región con menor penetración de internet', min_penetration['Región'], min_penetration['Penetración de internet (%)']])

    # Edad promedio por departamento
    edad_promedio = df.groupby('Departamento')['Edad promedio'].mean().reset_index()
    for _, row in edad_promedio.iterrows():
        results.append(['Edad promedio en ' + row['Departamento'], row['Edad promedio']])

    # Agrupar por departamento, los municipios con mayor uso de internet
    municipios_uso_internet = df.groupby('Departamento').apply(lambda x: x.loc[x['Uso de internet'].idxmax(), ['Municipio', 'Uso de internet']]).reset_index(drop=True)
    for _, row in municipios_uso_internet.iterrows():
        results.append(['Mayor uso de internet en ' + row['Municipio'], row['Uso de internet']])

    # Departamentos con mayor uso de dispositivos móviles
    max_dispositivos_movil = df.groupby('Departamento')['Dispositivos móviles'].sum().reset_index()
    max_dep = max_dispositivos_movil.loc[max_dispositivos_movil['Dispositivos móviles'].idxmax()]
    results.append(['Departamento con mayor uso de dispositivos móviles', max_dep['Departamento'], max_dep['Dispositivos móviles']])

    # Organizar las regiones de menor a mayor según el nivel educativo
    nivel_educativo = df.groupby('Región')['Nivel educativo'].mean().reset_index().sort_values('Nivel educativo')
    for _, row in nivel_educativo.iterrows():
        results.append(['Nivel educativo en ' + row['Región'], row['Nivel educativo']])

    # Municipios con mayores compras online
    mayores_compras_online = df.loc[df['Compras online (%)'].idxmax(), ['Municipio', 'Compras online (%)']]
    results.append(['Municipio con mayores compras online', mayores_compras_online['Municipio'], mayores_compras_online['Compras online (%)']])

    # Convertir resultados a DataFrame
    results_df = pd.DataFrame(results, columns=['Descripción', 'Valor1', 'Valor2'])

    return results_df

# Botón para realizar el análisis
if st.button("Analizar datos de Google Sheet"):
    if SPREADSHEET_ID:
        df = read_sheet()
        if not df.empty:
            st.header("Datos de la Hoja 1")
            st.dataframe(df)

            # Análisis de datos
            results_df = analyze_data(df)
            st.header("Resultados del Análisis")
            st.dataframe(results_df)

            # Actualizar la segunda hoja con el análisis
            update_sheet(results_df)
            st.success("Hoja actualizada con los resultados del análisis.")
        else:
            st.warning("La hoja está vacía o no se pudo leer.")
    else:
        st.warning("Por favor, ingresa un ID de hoja de cálculo válido.")