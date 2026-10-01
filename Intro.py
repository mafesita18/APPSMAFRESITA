import streamlit as st

st.set_page_config(
    page_title="Portafolio Interfaces Multimodales",
    page_icon="🌸",
    layout="wide"
)

st.title("Portafolio de Interfaces Multimodales 🚀")
st.subheader("María Fernanda Cadavid Yepes")

st.markdown("""
¡Bienvenido al portafolio de aplicaciones interactivas e Inteligencia Artificial!

Usa el **menú lateral a la izquierda** para navegar y probar cada una de las aplicaciones desarrolladas desde la **Clase 6** hasta la **Clase 9**.
""")

with st.sidebar:
    st.info("Selecciona cualquier clase del menú para abrir la aplicación correspondiente.")
