import streamlit as st
from PIL import Image

st.set_page_config(layout="wide", page_title="Mapping Demo", page_icon="🌍")

st.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    """, unsafe_allow_html=True)



# Título y subtítulo
st.title("Proyecto Integrador: Fire Developer")
st.subheader("Un Viaje Creativo con [Nombre del Equipo]")

# Imagen de fondo
image = Image.open("./static/proyecto integrador.png") 
st.image(image, width=700, use_column_width=True)  

# Integrantes
st.header("Nuestro Equipo")

col1, col2, col3 = st.columns(3)

with col1:
    st.image("./static/user.png", width=200)  # Reemplaza con la ruta de la foto
    st.write("**DANNY EDISON IDARRAGA GOMEZ**")
    st.write("[Rol en el proyecto]")

with col2:
    st.image("./static/user.png", width=200)  # Reemplaza con la ruta de la foto
    st.write("**JORGE EDUARDO MUÑOZ QUINTERO**")
    st.write("[Rol en el proyecto]")
    
with col3:
    st.image("./static/user.png", width=200)  # Reemplaza con la ruta de la foto
    st.write("**JHONATAN RODRIGUEZ MUÑOZ**")
    st.write("[Rol en el proyecto]")
    
    

# Descripción del proyecto
st.header("Sobre el Proyecto")
st.write("""
[Escribe aquí una breve descripción del proyecto, incluyendo el objetivo principal, la problemática que aborda y el enfoque que se utiliza. Puedes ser creativo y usar un lenguaje atractivo.]
""")

# Más información
st.header("Más Información")

# Puedes añadir secciones como:
# - Tecnología utilizada
# - Resultados esperados
# - Presentación de resultados (fecha y formato)
# - Contacto para preguntas

st.write("""
[Agrega la información adicional que consideres relevante.]
""")

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