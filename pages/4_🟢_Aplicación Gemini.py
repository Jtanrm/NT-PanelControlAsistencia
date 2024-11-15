import streamlit as st
import google.generativeai as genai
import google.ai.generativelanguage as glm
from dotenv import load_dotenv
from PIL import Image
import os
import io

load_dotenv()

import requests
import pandas as pd
import matplotlib.pyplot as plt
from streamlit_folium import folium_static
import folium
import base64

# Configura tu clave API de Google Gemini (obtén una clave API desde Google Cloud Platform)
API_KEY = os.environ.get("GOOGLE_API_KEY")
genai.configure(api_key=API_KEY)

st.image("../Google Gemini Logo.png", width=200)
st.write("")

gemini_pro, gemini_vision = st.tabs(["Gemini Pro", "Gemini Pro Vision"])

def main():
    pass

if __name__ == "__main__":
    main()

# st.title('Planificador de Viajes Personalizado')

# # Descripción explicativa de la aplicación
# descripcion = """
# ### Descripción de la Aplicación: Planificador de Viajes Personalizado

# ¡Bienvenidos a tu asistente de viajes inteligente! Esta aplicación está diseñada para ayudarte a planificar tu próximo viaje de manera fácil y rápida, adaptándose a tus intereses, presupuesto y preferencias. Aquí te explicamos qué puedes hacer con ella:

# 1. **Planificación Personalizada**: Al ingresar tu destino, actividades preferidas, duración del viaje, presupuesto y tipo de clima que te gustaría disfrutar, la aplicación utiliza inteligencia artificial (IA) para generar un itinerario perfecto para ti. Este itinerario incluye sugerencias de actividades y lugares recomendados que se ajustan a tus elecciones.

# 2. **Filtros Avanzados**: Además de la planificación básica, podrás seleccionar filtros adicionales como preferencias de comida, opciones de transporte y lugares turísticos específicos. Esto permite personalizar aún más tu experiencia, asegurando que tu viaje sea justo como lo imaginaste.

# 3. **Imágenes y Mapas Interactivos**: La aplicación también muestra una imagen del destino seleccionado para que tengas una mejor idea de lo que te espera. Además, ofrece mapas interactivos con puntos de interés recomendados, ayudándote a visualizar tu ruta y lugares destacados que no te puedes perder.

# 4. **Guardar Itinerarios**: Una vez que tengas tu itinerario generado, podrás descargarlo o guardarlo en formato PDF o como una lista de texto para llevarlo contigo y consultarlo durante tu viaje. 

# ¡Con esta herramienta, organizar tu aventura nunca fue tan fácil y divertido! Prepárate para explorar nuevos destinos con el apoyo de la tecnología y tu propio gusto personal.
# """

# # Mostrar la descripción en la aplicación
# st.markdown(descripcion)

# # Función para obtener sugerencias de viaje con Gemini
# def obtener_recomendaciones(destino, actividades, duracion, presupuesto, clima, comida, transporte, lugares):
#     prompt = f"Recomienda un itinerario de {duracion} días en {destino} para alguien que prefiere {', '.join(actividades)}, con un presupuesto de {presupuesto} COP, un clima {clima}, opciones de comida {', '.join(comida)}, transporte {transporte}, y visitando lugares como {lugares}."
    
#     # URL de la API de Gemini
#     url = "https://generativelanguage.googleapis.com/v1beta/models/gemini:generateText" 
    
#     headers = {'Content-Type': 'application/json',
#                'Authorization': f'Bearer {API_KEY}'}
    
#     data = {
#         "prompt": prompt,
#         "temperature": 0.7,  # Ajusta la creatividad de la respuesta
#         "max_output_tokens": 500,  # Limita la longitud del texto generado
#         "top_k": 40, # Ajusta la diversidad de la respuesta
#         "top_p": 0.95 # Ajusta la probabilidad de palabras usadas
#     }

#     try:
#         response = requests.post(url, headers=headers, json=data)
#         response.raise_for_status() # Maneja errores de red

#         if response.status_code == 200:
#             return response.json()["text"]
#         else:
#             st.error("Error al obtener recomendaciones. Intenta de nuevo más tarde.")
#             return None
#     except requests.exceptions.RequestException as e:
#         st.error(f"Error al conectar con la API: {e}")
#         return None

# # Función para mostrar un mapa interactivo
# def mostrar_mapa(lat, lon, lugares):
#     mapa = folium.Map(location=[lat, lon], zoom_start=12)
#     for lugar in lugares.split(","):
#         folium.Marker([lat, lon], tooltip=lugar.strip()).add_to(mapa)
#     folium_static(mapa)

# # Función para descargar el itinerario como archivo de texto
# def descargar_itinerario(itinerario_texto):
#     b64 = base64.b64encode(itinerario_texto.encode()).decode()
#     href = f'<a href="data:file/txt;base64,{b64}" download="itinerario.txt">Descargar Itinerario</a>'
#     st.markdown(href, unsafe_allow_html=True)

# # Título de la aplicación
# st.title('Planificador de Viajes Personalizado')

# # Entrada del usuario
# destino = st.text_input("¿A dónde quieres viajar?")
# actividades = st.multiselect("Selecciona tus intereses", ["Cultura", "Naturaleza", "Aventura", "Gastronomía"])
# duracion = st.slider("Duración del viaje (días)", 1, 30, 7)
# presupuesto = st.slider("Presupuesto (COP)", 100000, 10000000, 1000000, step=100000)
# clima = st.selectbox("Clima preferido", ["Cálido", "Frío", "Templado"])
# comida = st.multiselect("Preferencias de comida", ["Vegetariana", "Internacional", "Típica", "Comida rápida"])
# transporte = st.selectbox("Preferencias de transporte", ["Público", "Taxi", "Alquiler de auto"])
# lugares = st.text_area("Lugares turísticos específicos (separa por comas)")

# # Botón para obtener recomendaciones
# if st.button("Obtener Itinerario"):
#     if destino and actividades:
#         # Llamada a la API para obtener recomendaciones
#         recomendacion = obtener_recomendaciones(destino, actividades, duracion, presupuesto, clima, comida, transporte, lugares)
        
#         if recomendacion:
#             st.write("### Tu Itinerario Sugerido:")
#             st.write(recomendacion)
#             descargar_itinerario(recomendacion)  # Botón para descargar itinerario

#             # Simulación de coordenadas (reemplaza esto con coordenadas reales del destino)
#             lat, lon = 4.6097, -74.0817  # Ejemplo: Bogotá, Colombia
#             mostrar_mapa(lat, lon, lugares)  # Muestra el mapa interactivo
#     else:
#         st.warning("Por favor, completa todos los campos para obtener recomendaciones.")