import streamlit as st
import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore
from pathlib import Path
import random
from faker import Faker
from datetime import datetime, timedelta
import io 
from datetime import datetime, timedelta
import xlsxwriter
import time
import altair as alt
import seaborn as sns
import matplotlib.pyplot as plt
from PIL import Image

st.set_page_config(layout="wide")

st.subheader("Proyecto Integrador")

# Imagen de fondo
st.markdown("""
""", unsafe_allow_html=True)
# Cargar la imagen original
image = Image.open("./static/images/logo3.png")

# Redimensionar la imagen a 100x500 píxeles
image_resized = image.resize((710, 300))  # (ancho, alto)

# Mostrar la imagen redimensionada
st.image(image_resized)

# Verificar si ya existe una instancia de la aplicación
if not firebase_admin._apps:
    # Cargar las credenciales de Firebase desde los secretos de Streamlit
    firebase_credentials = st.secrets["FIREBASE_CREDENTIALS"]
    # Convertir las credenciales a un diccionario Python
    secrets_dict = firebase_credentials.to_dict()
    # Crear un objeto de credenciales usando el diccionario
    cred = credentials.Certificate(secrets_dict)
    # Inicializar la aplicación de Firebase con las credenciales
    app = firebase_admin.initialize_app(cred)

# Obtener el cliente de Firestore
db = firestore.client()

# Definir las colecciones (al principio del script)
empleados_collection = db.collection('empleados')
asistencias_collection = db.collection('asistencias')
ausencias_collection = db.collection('ausencias')
reportes_collection = db.collection('reportes')

# tad_descripcion, tab_Generador, tab_datos, tab_Análisis_Exploratorio, tab_Filtro_Final_Dinámico = st.tabs(
#     ["Descripción", "Generador y eliminación de empleados", "Asistencias, Ausencias y Reportes", "Análisis Exploratorio", "Filtro Final Dinámico"]
# )

tab_Generador, tab_datos, tab_Análisis_Exploratorio, tab_Filtro_Final_Dinámico = st.tabs(
    ["Generador y eliminación de empleados", "Asistencias, Ausencias y Reportes", "Análisis Exploratorio", "Filtro Final Dinámico"]
)

# #----------------------------------------------------------
# #Generador de datos
# #----------------------------------------------------------
# with tad_descripcion:
#     st.markdown('''
#     ### Introducción
#     -   ¿Qué es el proyecto?
#     -   ¿Cuál es el objetivo principal?
#     -   ¿Por qué es importante?

#     ### Desarrollo
#     -   Explicación detallada del proyecto
#     -   Procedimiento utilizado
#     -   Resultados obtenidos

#     ### Conclusión
#     -   Resumen de los resultados
#     -   Logros alcanzados
#     -   Dificultades encontradas
#     -   Aportes personales
#     ''')

#----------------------------------------------------------
#Generador de datos
#----------------------------------------------------------
with tab_Generador:
    st.write(
        'Esta función Python genera datos ficticios de empleados.'
    )
    # Inicializar Faker para Colombia
    fake = Faker('es_CO')

    # Lista de ciudades colombianas
    ciudades_colombianas = [
        'Bogotá', 'Medellín', 'Cali', 'Barranquilla', 'Cartagena',
        'Cúcuta', 'Bucaramanga', 'Pereira', 'Santa Marta', 'Ibagué',
        'Pasto', 'Manizales', 'Neiva', 'Villavicencio', 'Armenia'
    ]

    def generate_fake_employees(n):
        employees = []
        for _ in range(n):
        # Añadir campos de nivel educativo y carrera
            nivel_educativo = random.choice(["Bachiller", "Técnico", "Universitario", "Posgrado"])
        if nivel_educativo == "Bachiller":
            carrera = None
        else:
            carrera = fake.job()  # Usa Faker para generar una carrera aleatoria
        employee = {  # Indentar la creación del diccionario 'employee'
            'nombre': fake.first_name(),
            'apellido': fake.last_name(),
            'email': fake.email(),
            'fechaContratacion': datetime.now().isoformat(),
            'ciudad': random.choice(ciudades_colombianas),  # Asigna una ciudad aleatoria
            'asistencias': [],
            'ausencias': [],
            'edad': random.randint(18, 65),
            'nivelEducativo': nivel_educativo,
            'carrera': carrera
        }
        employees.append(employee)
        return employees

    def delete_collection(collection):  # Recibe la colección como argumento
        docs = collection.get()  # Utiliza la colección recibida
        for doc in docs:
            doc.reference.delete()

    def add_data_to_firestore(collection, data):  # Recibe la colección como argumento
        for item in data:
            collection.add(item)  # Utiliza la colección recibida

    # Generación de Empleados
    col1, col2 = st.columns(2)

with col1:
        st.subheader('Empleados')
        num_employees = st.number_input('Número de empleados a generar', min_value=1, max_value=100, value=10)
        eliminar_empleados = st.checkbox('Eliminar empleados existentes')  # Casilla de verificación para eliminar empleados
        if st.button('Generar y Añadir Empleados'):
            if eliminar_empleados:
                with st.spinner('Eliminando empleados existentes...'):
                    delete_collection(empleados_collection)
            with st.spinner('Generando y añadiendo nuevos empleados...'):
                employees = generate_fake_employees(num_employees)
                add_data_to_firestore(empleados_collection, employees)
            st.success(f'{num_employees} empleados añadidos a Firestore')

            # Mostrar empleados generados
            employees = empleados_collection.stream()
            employees_data = [doc.to_dict() for doc in employees]
            df_employees = pd.DataFrame(employees_data)
            st.dataframe(df_employees)
with col2:
        # Eliminar un empleado por ID
        st.subheader('Eliminar Empleado por ID')
        empleado_id_eliminar = st.text_input('Ingresa el ID del empleado a eliminar', '')
        if st.button('Eliminar Empleado'):
            if empleado_id_eliminar:
                with st.spinner('Eliminando empleado...'):
                    empleados_collection.document(empleado_id_eliminar).delete()
                st.success(f'Empleado con ID {empleado_id_eliminar} eliminado.')
            else:
                st.warning('Por favor, ingresa un ID de empleado válido.')
                
            
#----------------------------------------------------------
# Datos
#----------------------------------------------------------
with tab_datos:
    st.header("Datos")
    st.write("Aquí puedes ver los datos que se encuentran en la base de datos de Firestore.")

    # Obtener los datos de la colección
    asistencias = asistencias_collection.stream()
    asistencias_data = [doc.to_dict() for doc in asistencias]
    df_asistencias = pd.DataFrame(asistencias_data)
    st.dataframe(df_asistencias)

    st.subheader("Generar Nueva Asistencia")

    # Obtener la lista de IDs de empleados existentes
    empleados_ids = [doc.id for doc in empleados_collection.stream()]

    # Campos de entrada para la asistencia
    empleado_id = st.selectbox("ID del Empleado", empleados_ids, key="empleado_id")  # Selección del ID del empleado
    fecha = st.date_input("Fecha", datetime.now().date(), key="fecha")
    hora_entrada = st.time_input("Hora de Entrada", datetime.now().time(), key="hora_entrada")
    hora_salida = st.time_input("Hora de Salida", datetime.now().time(), key="hora_salida")
    estado = st.selectbox("Estado", ["Presente", "Tardanza", "Ausente"], key="estado")  # Selección del estado

    # Botón para generar y guardar la asistencia
    if st.button("Generar y Guardar Asistencia"):
        if empleado_id:
            # Crear el documento de asistencia
            nueva_asistencia = {
                'empleadoID': empleado_id,
                'fecha': datetime.combine(fecha, hora_entrada).isoformat(),
                'horaEntrada': datetime.combine(fecha, hora_entrada).isoformat(),
                'horaSalida': datetime.combine(fecha, hora_salida).isoformat(),
                'estado': estado
            }
            # Agregar el documento a Firestore
            asistencias_collection.add(nueva_asistencia)
            st.success("Asistencia creada correctamente.")
        else:
            st.warning("Por favor, selecciona un ID de empleado válido.")

    #----------------------------------------------------------
    # Ausencias
    #----------------------------------------------------------

    st.subheader("Generar Nueva Ausencia")

    # Obtener la lista de IDs de empleados existentes
    empleados_ids = [doc.id for doc in empleados_collection.stream()]

    # Campos de entrada para la ausencia
    empleado_id = st.selectbox("ID del Empleado", empleados_ids, key="empleado_id_ausencia")
    fecha = st.date_input("Fecha", datetime.now().date(), key="fecha_ausencia")
    tipo = st.selectbox("Tipo", ["Justificada", "No Justificada"], key="tipo_ausencia")
    motivo = st.text_area("Motivo", key="motivo_ausencia")  # Campo opcional
    estado = st.selectbox("Estado", ["Aprobada", "Rechazada"], key="estado_ausencia")

    # Botón para generar y guardar la ausencia
    if st.button("Generar y Guardar Ausencia"):
        if empleado_id:
            # Crear el documento de ausencia
            nueva_ausencia = {
                'empleadoID': empleado_id,
                'fecha': datetime.combine(fecha, datetime.now().time()).isoformat(),  # Timestamp de fecha y hora de entrada
                'tipo': tipo,
                'motivo': motivo,
                'estado': estado
            }
            # Agregar el documento a Firestore
            ausencias_collection.add(nueva_ausencia)
            st.success("Ausencia creada correctamente.")
        else:
            st.warning("Por favor, selecciona un ID de empleado válido.")

    #----------------------------------------------------------
    # Reportes
    #----------------------------------------------------------
    st.subheader("Generar Reporte")

    # Obtener la lista de IDs de empleados existentes
    empleados_ids = [doc.id for doc in empleados_collection.stream()]

    # Selección del empleado
    empleado_id = st.selectbox("ID del Empleado", empleados_ids, key="empleado_id_reporte")

    # Botón para generar el reporte
    if st.button("Generar Reporte"):
        if empleado_id:
            # Obtener las asistencias y ausencias del empleado
            asistencias_empleado = asistencias_collection.where("empleadoID", "==", empleado_id).stream()
            ausencias_empleado = ausencias_collection.where("empleadoID", "==", empleado_id).stream()

            # Calcular total de asistencias y ausencias
            total_asistencias = 0
            total_ausencias = 0
            for asistencia in asistencias_empleado:
                total_asistencias += 1
            for ausencia in ausencias_empleado:
                total_ausencias += 1

            # Crear el documento del reporte
            nuevo_reporte = {
                'empleadoID': empleado_id,
                'fechaInicio': datetime.now().isoformat(),
                'fechaFin': datetime.now().isoformat(),
                'totalAsistencias': total_asistencias,
                'totalAusencias': total_ausencias
            }

            # Agregar el documento a Firestore
            reportes_collection.add(nuevo_reporte)
            st.success("Reporte creado correctamente.")

            # Exportar reporte a Excel
            df_reporte = pd.DataFrame([nuevo_reporte])
            # Guarda el DataFrame como un buffer de bytes en memoria
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df_reporte.to_excel(writer, sheet_name='Reporte', index=False)
            # Genera el botón de descarga
            st.download_button(
                label="Descargar Reporte",
                data=output.getvalue(),
                file_name="reporte.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.warning("Por favor, selecciona un ID de empleado válido.")
            

#----------------------------------------------------------
# Analítica 1
#----------------------------------------------------------
with tab_Análisis_Exploratorio:    
    st.title("Análisis Exploratorio")

    # Definir df como un DataFrame vacío al principio
    df = pd.DataFrame() 

    # Cargar los datos desde Firestore al inicio de la sección
    empleados = empleados_collection.stream()
    empleados_data = [doc.to_dict() for doc in empleados]
    df_empleados = pd.DataFrame(empleados_data)

    asistencias = asistencias_collection.stream()
    asistencias_data = [doc.to_dict() for doc in asistencias]
    df_asistencias = pd.DataFrame(asistencias_data)

    ausencias = ausencias_collection.stream()
    ausencias_data = [doc.to_dict() for doc in ausencias]
    df_ausencias = pd.DataFrame(ausencias_data)
        
    reportes = reportes_collection.stream()
    reportes_data = [doc.to_dict() for doc in reportes]
    df_reportes = pd.DataFrame(reportes_data)

    st.subheader("Cargar Datos")
    uploaded_file = st.file_uploader("Sube un archivo Excel", type=["xlsx"], key="file_uploader_exploratorio") # Clave única para este widget
    if uploaded_file is not None:
        try:
        # Leer el archivo Excel
            df = pd.read_excel(uploaded_file)
        
        except Exception as e:
            st.error(f"Error al cargar el archivo: {e}")
        

        # Actualizar los DataFrames con los datos del Excel
        df_empleados = df.copy()
        df_asistencias = df.copy()
        df_ausencias = df.copy()
        df_reportes =df.copy()
            
    if 'estado' not in df_empleados.columns: 
            df_empleados['estado'] = None

    # Exportar datos a Excel
    st.subheader("Exportar Datos a Excel")

    # Exportar DataFrame de empleados
    if st.button("Exportar Empleados"):
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            df_empleados.to_excel(writer, sheet_name="Empleados", index=False)
        st.download_button(
            label="Descargar Empleados",
            data=buffer.getvalue(),
            file_name="empleados.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    # Exportar DataFrame de asistencias
    if st.button("Exportar Asistencias"):
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            df_asistencias.to_excel(writer, sheet_name="Asistencias", index=False)
        st.download_button(
            label="Descargar Asistencias",
            data=buffer.getvalue(),
            file_name="asistencias.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    # Exportar DataFrame de ausencias
    if st.button("Exportar Ausencias"):
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            df_ausencias.to_excel(writer, sheet_name="Ausencias", index=False)
        st.download_button(
            label="Descargar Ausencias",
            data=buffer.getvalue(),
            file_name="ausencias.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
    #Exportar DataFrame de reportes
    if st.button("Exportar Reportes"):
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            df_reportes.to_excel(writer, sheet_name="Reportes", index=False)
        st.download_button(
            label="Descargar Reportes",
            data=buffer.getvalue(),
            file_name="reportes.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    # Mostrar información del DataFrame de empleados
    st.subheader("Empleados")
    st.dataframe(df_empleados.head())  # Mostrar las primeras 5 filas en una tabla
    st.write(f"**Forma del DataFrame:**\n{df_empleados.shape}")
    st.write(f"**Tipos de datos:**\n{df_empleados.dtypes}")
    st.write(f"**Valores nulos:**\n{df_empleados.isnull().sum()}")
    
    # Verifica si df tiene columnas
    if not df.empty:
        st.dataframe(df.describe())  # Mostrar resumen estadístico en una tabla

    # Mostrar información del DataFrame de asistencias
    st.subheader("Asistencias")
    st.dataframe(df_asistencias.head())  # Mostrar las primeras 5 filas en una tabla
    st.write(f"**Forma del DataFrame:**\n{df_asistencias.shape}")
    st.write(f"**Tipos de datos:**\n{df_asistencias.dtypes}")
    st.write(f"**Valores nulos:**\n{df_asistencias.isnull().sum()}")
    st.dataframe(df_asistencias.describe()) # Mostrar resumen estadístico en una tabla

    # Mostrar información del DataFrame de ausencias
    st.subheader("Ausencias")
    st.dataframe(df_ausencias.head())  # Mostrar las primeras 5 filas en una tabla
    st.write(f"**Forma del DataFrame:**\n{df_ausencias.shape}")
    st.write(f"**Tipos de datos:**\n{df_ausencias.dtypes}")
    st.write(f"**Valores nulos:**\n{df_ausencias.isnull().sum()}")
    st.dataframe(df_ausencias.describe()) # Mostrar resumen estadístico en una tabla

    # Mostrar información del DataFrame de reportes
    st.subheader("Reportes")
    if not df.empty:
        st.dataframe(df.head()) # Mostrar las primeras 5 filas en una tabla
        st.write(f"**Forma del DataFrame:**\n{df.shape}")
        st.write(f"**Tipos de datos:**\n{df.dtypes}")
        st.write(f"**Valores nulos:**\n{df.isnull().sum()}")
        st.dataframe(df.describe()) # Mostrar resumen estadístico en una tabla

    # Ejemplo de conteo de valores únicos (en este caso, para el estado de las ausencias)
    if not df.empty:
        st.write(f"**Frecuencia de estados de ausencia:**\n{df['estado'].value_counts()}")

    # Gráfico de barras para el nivel educativo
    st.subheader("Nivel Educativo de los Empleados")
    chart_educativo = alt.Chart(df_empleados).mark_bar().encode(
        alt.X("nivelEducativo:N"),
        alt.Y("count():Q")
    )
    st.altair_chart(chart_educativo, use_container_width=True)
    
    # Gráfico de barras de distribución por edad
    st.subheader("Distribución por Edad")
    chart_edad = alt.Chart(df_empleados).mark_bar().encode(
    alt.X("edad:Q", bin=alt.Bin(extent=[18, 68], step=5)),  # Rango de 18 a 68, intervalos de 5
    alt.Y("count():Q", axis=alt.Axis(format="d"))  # Cantidad en enteros
    )
    st.altair_chart(chart_edad, use_container_width=True)

#----------------------------------------------------------
#Analítica 2
#----------------------------------------------------------
with tab_Filtro_Final_Dinámico:
    st.title("Filtro Final Dinámico")
    st.subheader("Filtro Final Dinámico")

    df = pd.DataFrame()  # DataFrame vacío inicial
    uploaded_file = st.file_uploader("Sube un archivo Excel", type=["xlsx"], key="file_uploader_dinamico")
    if uploaded_file is not None:
        try:
            df = pd.read_excel(uploaded_file)

            st.subheader("Filtros")
            # Filtro por fecha (con manejo de errores)
            try:
                fecha_inicio = st.date_input("Fecha de inicio", datetime.now().date(), key="fecha_inicio")
                fecha_fin = st.date_input("Fecha de fin", datetime.now().date(), key="fecha_fin")
                fecha_inicio = pd.to_datetime(fecha_inicio)
                fecha_fin = pd.to_datetime(fecha_fin)
            except ValueError as e:
                st.error(f"Error en las fechas: {e}. Ingrese fechas válidas.")


            tipo_dato = st.selectbox("Tipo de dato", ["Asistencias", "Ausencias", "Reportes"], key="tipo_dato")

            ciudad_filtro = [] #Lista vacia por defecto
            if 'ciudad' in df.columns:
                ciudad_filtro = st.multiselect("Ciudad", list(df['ciudad'].unique()), key="ciudad_filtro")
            else:
                st.warning("La columna 'ciudad' no existe en el archivo. El filtro de ciudad no estará disponible.")


            # Aplicar filtros
            df_filtrado = df.copy()
            try:
                if 'fechaContratacion' in df_filtrado.columns:
                    df_filtrado['fechaContratacion'] = pd.to_datetime(df_filtrado['fechaContratacion'])
                    df_filtrado = df_filtrado[
                        (df_filtrado['fechaContratacion'] >= fecha_inicio) &
                        (df_filtrado['fechaContratacion'] <= fecha_fin)
                    ]
                else:
                    st.warning("La columna 'fechaContratacion' no se encuentra. El filtrado por fecha no se aplicará.")
            except (KeyError, ValueError) as e:
                st.error(f"Error al filtrar por fecha: {e}")

            if ciudad_filtro:
                df_filtrado = df_filtrado[df_filtrado['ciudad'].isin(ciudad_filtro)]

            # Mostrar resultados y generar gráficos
            if not df_filtrado.empty:
                st.write(f"**Criterios de filtrado:**")
                st.write(f" - Fecha de inicio: {fecha_inicio}")
                st.write(f" - Fecha de fin: {fecha_fin}")
                st.write(f" - Ciudad: {ciudad_filtro}")

                st.dataframe(df_filtrado)
                st.subheader("Gráficos")
                try:
                    if tipo_dato == "Asistencias" or tipo_dato == "Ausencias":
                        chart = alt.Chart(df_filtrado).mark_bar().encode(
                            alt.X("ciudad:N"),
                            alt.Y("count():Q")
                        )
                        st.altair_chart(chart, use_container_width=True)
                    elif tipo_dato == "Reportes":
                        chart = alt.Chart(df_filtrado).mark_bar().encode(
                            alt.X("edad:Q"),
                            alt.Y("count():Q")
                        )
                        st.altair_chart(chart, use_container_width=True)

                        if 'edad' in df_filtrado.columns: #Verifica que exista la columna edad
                            fig, ax = plt.subplots()
                            sns.histplot(data=df_filtrado, x='edad', ax=ax)
                            st.pyplot(fig)

                        if 'edad' in df_filtrado.columns and 'ciudad' in df_filtrado.columns: #Verifica que existan las columnas
                            sns.scatterplot(data=df_filtrado, x='edad', y='ciudad')
                            st.pyplot()

                except (KeyError, ValueError) as e:
                    st.error(f"Error al generar gráficos: {e}. Revisa las columnas en tu archivo.")
            else:
                st.info("No hay datos que coincidan con los criterios de filtro.")

        except Exception as e:
            st.error(f"Error al procesar el archivo: {e}")
    else:
        st.info("Por favor, sube un archivo Excel.")