import streamlit as st
from streamlit_drawable_canvas import st_canvas

st.title("Tablero para dibujo")

with st.sidebar:
    st.subheader("Propiedades del Tablero")
    
    st.subheader("Dimensiones del Tablero")
    st.write("Ancho del tablero:")
    canvas_width = 600
    
    canvas_height = 400
    st.write(canvas_width)
    st.write("Alto del tablero:")
    st.write(canvas_height)
    
    drawing_mode = st.selectbox(
        "Herramienta de Dibujo:",
        ("freedraw", "line", "rect", "circle", "transform", "polygon", "point"),
    )
    
    stroke_width = st.slider('Selecciona el ancho de línea', 1, 30, 15)
    
    stroke_color = st.color_picker("Color de trazo", "#FFFFFF")
    
    bg_color = st.color_picker("Color de fondo", "#000000")

canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_color=bg_color,
    height=canvas_height,
    width=canvas_width,
    drawing_mode=drawing_mode,
    key=f"canvas_{canvas_width}_{canvas_height}"
)
