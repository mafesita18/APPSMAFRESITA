import streamlit as st

st.set_page_config(
    page_title="Portafolio APPSMAFRESITA",
    page_icon="🌸",
    layout="wide"
)

st.title("🌸 Portafolio de Interfaces Multimodales — APPSMAFRESITA")
st.subheader("María Fernanda Cadavid Yepes")

st.markdown("""
¡Bienvenido al portafolio de aplicaciones interactivas e Inteligencia Artificial! 🚀

👈 **Instrucciones:** Puedes navegar y probar cada una de las herramientas seleccionándolas en el **menú lateral a la izquierda**.
""")

st.divider()

st.header("📚 Catálogo de Aplicaciones por Clase")

# Clase 6
with st.expander("📌 **CLASE 6: Interfaces e Interacción**", expanded=True):
    st.markdown("""
    * **Clase 6 Interfaces:** Primera aplicación desarrollada para poner a prueba componentes interactivos básicos y entradas de usuario en Streamlit.
    * **Clase 6 IMM1 (Hello Kitty):** Aplicación temática e interactiva con estética kawaii de Hello Kitty para conversión y reproducción de audio.
    """)

# Clase 7
with st.expander("📌 **CLASE 7: Procesamiento de Audio, Traducción y OCR**", expanded=True):
    st.markdown("""
    * **Traductor de Voz y Texto:** Traducción automática de frases y generación de audio sintético en diferentes idiomas.
    * **Reconocimiento OCR:** Extracción e identificación de texto a partir de imágenes cargadas o tomadas desde la cámara.
    * **OCR a Audio:** Lectura óptica de caracteres combinada con síntesis de voz para audiolibros y accesibilidad.
    """)

# Clase 8
with st.expander("📌 **CLASE 8: Procesamiento de Lenguaje Natural (PLN)**", expanded=True):
    st.markdown("""
    * **Nube de Palabras (WordCloud):** Visualización analítica de las palabras más frecuentes en textos o documentos.
    * **Explorador de Sentimientos:** Análisis de emociones en texto acompañado de animaciones interactivas.
    * **Buscador TF-IDF:** Sistema de búsqueda inteligente por relevancia y similitud coseno sobre documentos (.pdf, .txt, .csv).
    """)

# Clase 9
with st.expander("📌 **CLASE 9: Visión por Computador e Inteligencia Artificial**", expanded=True):
    st.markdown("""
    * **Detección de Objetos (YOLOv5):** Identificación y delimitación de objetos en tiempo real desde la cámara o imágenes.
    * **Clasificación con Teachable Machine:** Modelo de red neuronal entrenado para clasificación de imágenes y reconocimiento de gestos/posturas.
    """)

st.info("👈 Selecciona cualquiera de las aplicaciones en el panel de la izquierda para comenzar a interactuar.")
