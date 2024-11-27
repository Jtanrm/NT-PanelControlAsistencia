import streamlit as st
from PIL import Image
import google.generativeai as genai

# Configurar la API de Google desde secrets
genai.configure(api_key=st.secrets.GEMINI.api_key)

# Especificar la versión del modelo
model = genai.GenerativeModel("gemini-1.5-flash")

# Función para inicializar el modelo
def get_model():
    return genai.GenerativeModel("gemini-1.5-flash")

# # CSS personalizado (estilos integrados del Gemini Eco)
# st.markdown("""
#     <style>
#     .main {
#         padding: 1rem;
#     }
#     .stTitle {
#         text-align: center;
#         color: #2c3e50;
#         font-size: 2rem !important;
#         margin-bottom: 1rem !important;
#     }
#     .contenedor-principal {
#         background-color: #f8f9fa;
#         padding: 1rem;
#         border-radius: 10px;
#         margin-bottom: 1rem;
#     }
#     .caneca-card {
#         background-color: white;
#         padding: 1rem;
#         border-radius: 10px;
#         box-shadow: 0 2px 4px rgba(0,0,0,0.1);
#         height: 100%;
#         transition: all 0.3s ease;
#     }
#     .caneca-seleccionada {
#         transform: scale(1.02);
#         box-shadow: 0 4px 8px rgba(0,0,0,0.2);
#         border: 2px solid #4CAF50;
#     }
#     .icono-caneca {
#         font-size: 2rem;
#         margin-bottom: 0.5rem;
#     }
#     .ejemplos-lista {
#         font-size: 0.9rem;
#         color: #666;
#         margin: 0;
#         padding-left: 1.2rem;
#     }
#     .resultado {
#         text-align: center;
#         padding: 1rem;
#         border-radius: 10px;
#         margin: 1rem 0;
#         background-color: #e8f5e9;
#     }
#     .instrucciones {
#         background-color: #fff;
#         padding: 1rem;
#         border-radius: 10px;
#         margin-bottom: 1rem;
#         border-left: 4px solid #2196F3;
#     }
#     .stButton button {
#         width: 100%;
#         height: 3rem;
#     }
#     div[data-testid="stVerticalBlock"] {
#         gap: 0.5rem;
#     }
#     </style>
# """, unsafe_allow_html=True)

# Tabs principales
st.title("Gemini AI - Interactúa y Comenta Código")

# Imagen de fondo
st.markdown("""
""", unsafe_allow_html=True)
# Cargar la imagen original
image = Image.open("./static/images/Google Ai Gemini.png")

# Redimensionar la imagen a 100x500 píxeles
image_resized = image.resize((700, 300))  # (ancho, alto)

# Mostrar la imagen redimensionada
st.image(image_resized)

# gemini_pro, gemini_vision, gemini_Eco, gemini_Travel = st.tabs(
#     ["Gemini Pro", "< Gemini code />", "Gemini Eco", "Gemini Traveling"]
# )

gemini_pro, gemini_vision, gemini_Travel = st.tabs(
    ["Gemini Pro", "< Gemini code />", "Gemini Traveling"]
)

# Tab para Gemini Pro
with gemini_pro:
    st.header("Interactuar con Gemini Pro")

    # Imagen de fondo
    st.markdown("""
    """, unsafe_allow_html=True)
    # Cargar la imagen original
    image_ia = Image.open("./static/images/interaccionIA.jpg")

    # Redimensionar la imagen a 100x500 píxeles
    image_resized = image_ia.resize((810, 300))  # (ancho, alto)

    # Mostrar la imagen redimensionada
    st.image(image_resized)

    user_input = st.text_input("Ingresa tu texto:")
    if st.button("Generar"):
        if user_input:
            response = model.generate_content(user_input)
            st.write("Respuesta:", response.text)
        else:
            st.warning("Por favor ingresa un texto.")

# Tab para Comentador de Código
with gemini_vision:
    # Tab para Comentador de Código
    st.title("Comentador de Código con Gemini")

     # Imagen de fondo
    st.markdown("""
    """, unsafe_allow_html=True)
    # Cargar la imagen original
    image_codigo = Image.open("./static/images/leguajes.jpg")

    # Redimensionar la imagen a 100x500 píxeles
    image_resized = image_codigo.resize((810, 300))  # (ancho, alto)

    # Mostrar la imagen redimensionada
    st.image(image_resized)

    ## Entrada directa de código
    st.subheader("Introduce tu código:")
    language_options = {
        "Python": ("python", ".py"),
        "JavaScript": ("javascript", ".js"),
        "Java": ("java", ".java"),
        "C++": ("cpp", ".cpp"),
        "HTML": ("html", ".html"),
        "Texto plano": ("plaintext", ".txt")
    }
    selected_language = st.selectbox("Selecciona el lenguaje:", list(language_options.keys()), index=0)
    code_input = st.text_area("Escribe o pega tu código aquí:", height=300, placeholder="Escribe tu código aquí...")

    if st.button("Generar Comentarios"):
        if code_input.strip() == "":
            st.error("Por favor, introduce algún código antes de generar comentarios.")
        else:
            with st.spinner("Procesando..."):
                try:
                    # Generación de comentarios utilizando la API de Gemini
                    prompt = f"Genera comentarios detallados para el siguiente código en {selected_language}:\n\n{code_input}"
                    response = model.generate_content(prompt)

                    # Mostrar el código comentado
                    commented_code = response.text

                    st.subheader("Código Comentado:")
                    st.code(commented_code, language=language_options[selected_language][0])

                    # Descargar archivo con la extensión adecuada
                    file_name = f"codigo_comentado{language_options[selected_language][1]}"
                    st.download_button(
                        label=f"Descargar Código Comentado ({file_name})",
                        data=commented_code,
                        file_name=file_name,
                        mime="text/plain"
                    )
                    st.success(f"Código comentado generado correctamente. Se descargará como {file_name}.")
                except Exception as e:
                    st.error(f"Error: {e}")


# # Tab para Gemini Eco
# with gemini_Eco:
#     st.header("Clasificador de Residuos")
#     datos_canecas = {
#         "reciclable": {"color": "blanco", "icono": "♻️", "descripcion": "Residuos reciclables como papel y plástico"},
#         "no reciclable": {"color": "negro", "icono": "⚫", "descripcion": "Residuos no reciclables como pañales"},
#         "orgánico": {"color": "verde", "icono": "🌱", "descripcion": "Residuos orgánicos como restos de comida"},
#     }
#     residuo = st.text_input("¿Qué quieres reciclar?")
#     if st.button("Clasificar"):
#         if residuo:
#             with st.spinner("Clasificando..."):
#                 try:
#                     prompt = f"Clasifica este residuo: {residuo} como reciclable, no reciclable u orgánico."
#                     categoria = model.generate_content(prompt).text.lower().strip()
#                     if categoria in datos_canecas:
#                         st.success(f"El residuo va en la caneca {datos_canecas[categoria]['color']}.")
#                     else:
#                         st.error("No se pudo clasificar el residuo.")
#                 except Exception as e:
#                     st.error(f"Error: {e}")
#         else:
#             st.warning("Por favor ingresa un residuo para clasificar.")

# Tab para Gemini Traveling
with gemini_Travel:
    st.header("Planificador de Viajes Personalizado")

    # Imagen de fondo
    st.markdown("""
    """, unsafe_allow_html=True)
    # Cargar la imagen original
    image_viaje = Image.open("./static/images/traveling.jpg")

    # Redimensionar la imagen a 100x500 píxeles
    image_resized = image_viaje.resize((810, 300))  # (ancho, alto)

    # Mostrar la imagen redimensionada
    st.image(image_resized)

    destino = st.text_input("Destino:")
    duracion = st.number_input("Duración en días:", min_value=1, step=1)
    actividades = st.text_area("Actividades preferidas (separadas por comas):")
    if st.button("Planificar Viaje"):
        with st.spinner("Planificando..."):
            try:
                prompt = f"Planifica un itinerario de {duracion} días para {destino} con actividades: {actividades}."
                itinerario = model.generate_content(prompt).text
                st.subheader("Itinerario:")
                st.write(itinerario)
                st.download_button("Descargar Itinerario", itinerario, "itinerario.txt")
            except Exception as e:
                st.error(f"Error: {e}")
