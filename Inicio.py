import streamlit as st
from PIL import Image

st.set_page_config(layout="wide", page_title="Mapping Demo", page_icon="🌍")

st.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    """, unsafe_allow_html=True)



# Título y subtítulo
st.title("Panel de Control de Asistencia de Empleados")
st.subheader("Asistify")

# Imagen de fondo
image = Image.open("./static/images/Asistify.png")
st.image(image, width=400, use_container_width=False)


# Integrantes
st.header("Nuestro Equipo")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.image("./static/images/DANNY .jpg", width=200)  # Reemplaza con la ruta de la foto
    st.write("**DANNY EDISON IDARRAGA GOMEZ**")
    st.write(" Scrum Master")

with col2:
    st.image("./static/images/EDUAR.jpg", width=200)  # Reemplaza con la ruta de la foto
    st.write("**JORGE EDUARDO MUÑOZ QUINTERO**")
    st.write("Product Owner")
    
with col3:
    st.image("./static/images/JHONATAN.jpg", width=200)  # Reemplaza con la ruta de la foto
    st.write("**JHONATAN RODRIGUEZ MUÑOZ**")
    st.write("Developer")
    
with col4:
    st.image("./static/images/SERGIO.jpg", width=200)  # Reemplaza con la ruta de la foto
    st.write("**SERGIO MARENCO**")
    st.write("Developer")
    
    

# Descripción del proyecto
st.header("Sobre el Proyecto Asistify")
st.write("Esta aplicación está diseñada para que los Administradores puedan gestionar y monitorear la asistencia de los empleados de forma eficiente y centralizada. La plataforma permite registrar la asistencia, ausencias y tardanzas de cada empleado, simplificando el proceso de seguimiento. Además, ofrece herramientas para generar reportes detallados, brindando una visión completa y en tiempo real sobre la puntualidad y el cumplimiento de horarios, lo que facilita la toma de decisiones informadas en la gestión de las personas. En una empresa con un número significativo de empleados, el Administrador enfrenta serias dificultades para gestionar la asistencia debido a registros manuales y hojas de cálculo. Esta falta de un sistema centralizado provoca errores en el cálculo de horas trabajadas y dificultades en la generación de reportes precisos. La necesidad de un sistema que permita el seguimiento eficiente y preciso de la asistencia se vuelve evidente para optimizar la gestión del personal y facilitar la toma de decisiones.")
st.write("""¿Qué es el proyecto?
El Panel de Control de Asistencia de Empleados es una aplicación que permite al Administrador gestionar y monitorear la asistencia de los empleados de manera eficiente. La aplicación está diseñada para centralizar el registro de asistencia, ausencias y tardanzas, y facilitar la generación de reportes detallados sobre la asistencia de los empleados.
 """)


# Más información
st.header("Tecnología utilizada")

# Puedes añadir secciones como:
# - Tecnología utilizada
# - Resultados esperados
# - Presentación de resultados (fecha y formato)
# - Contacto para preguntas

st.write("""
Nuestro Panel de Control de Asistencia de Empleados Asistify está impulsado por herramientas tecnológicas de última generación, que garantizan una experiencia fluida y resultados precisos. Construido sobre una arquitectura confiable en Streamlit, el sitio proporciona una interfaz intuitiva y accesible desde cualquier dispositivo.

El procesamiento de datos se realiza con Python y la versátil librería Pandas, permitiendo gestionar y analizar grandes volúmenes de información de asistencia en tiempo real. Para visualizar tendencias y métricas clave, hemos incorporado gráficos dinámicos e interactivos que facilitan el monitoreo de datos y mejoran la toma de decisiones.

Esta solución integra tecnología robusta y amigable, diseñada para que puedas mantener el control total de la asistencia y el rendimiento del equipo en una plataforma única y eficiente.
""")

st.header("Resultados esperados")

st.write("Reducción de errores en el registro de asistencia: La digitalización y centralización de los registros permiten una mayor precisión y reducen los errores comunes en el seguimiento manual.")

st.write("""
    Monitoreo en tiempo real de la asistencia: Los administradores pueden ver la asistencia y puntualidad de los empleados en tiempo real, permitiendo una respuesta rápida ante ausencias o retrasos.
""")

st.write("""
    Generación automática de reportes detallados: Con la integración de Pandas y gráficos dinámicos, se espera una generación de reportes rápida y detallada, que proporciona una visión clara de los patrones de asistencia y facilita la toma de decisiones.
""")

st.write("""
    Mejoras en la eficiencia de gestión de recursos humanos: Al contar con reportes precisos y accesibles desde Streamlit, el equipo de recursos humanos puede gestionar la asistencia de manera más eficiente, ahorrando tiempo y recursos.
""")

st.write("""
    Transparencia y responsabilidad de los empleados: El acceso a datos claros y en tiempo real fomenta la responsabilidad, ya que los empleados saben que su asistencia y puntualidad están siendo monitoreadas con precisión.
""")
st.header("Equipo instalado")
st.video("https://www.youtube.com/watch?v=VEAtg3LtB0A")


# Footer con links
st.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">

    <div style="text-align: center; margin-top: 50px;">
        <a href="https://www.google.com" style="color: #DB4437; margin: 0 15px;">
            <i class="fab fa-google fa-2x"></i>
        </a>
        <a href="https://www.facebook.com" style="color: #4267B2; margin: 0 15px;">
            <i class="fab fa-facebook fa-2x"></i>
        </a>
        <a href="https://www.linkedin.com" style="color: #0077B5; margin: 0 15px;">
            <i class="fab fa-linkedin fa-2x"></i>
        </a>
    </div>
    """, unsafe_allow_html=True
)