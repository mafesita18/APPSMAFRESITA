import os
import base64
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import streamlit as st
from streamlit_drawable_canvas import st_canvas
from openai import OpenAI
import openai

def encode_image_to_base64(image_path):
    try:
        with open(image_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
            return encoded_image
    except FileNotFoundError:
        return "Error: La imagen no se encontró en la ruta especificada."

st.title('Tablero Inteligente')
with st.sidebar:
    st.subheader("Acerca de:")
    st.subheader("En esta aplicación veremos la capacidad que ahora tiene una máquina de interpretar un boceto")

st.subheader("Dibuja el boceto en el panel y presiona el botón para analizarla")

drawing_mode = "freedraw"
stroke_width = st.sidebar.slider('Selecciona el ancho de línea', 1, 30, 5)
stroke_color = "#000000" 
bg_color = '#FFFFFF'

canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_color=bg_color,
    height=300,
    width=400,
    drawing_mode=drawing_mode,
    key="canvas_drawrecog",
)

ke = st.text_input('Ingresa tu Clave', type="password")

analyze_button = st.button("Analiza la imagen", type="secondary")

if canvas_result.image_data is not None and ke and analyze_button:
    os.environ['OPENAI_API_KEY'] = ke
    api_key = ke

    with st.spinner("Analizando ..."):
        input_numpy_array = np.array(canvas_result.image_data)
        input_image = Image.fromarray(input_numpy_array.astype('uint8'), 'RGBA')
        input_image.save('img.png')
        
        base64_image = encode_image_to_base64("img.png")
            
        prompt_text = "Describe the image in spanish"
        
        try:
            client = OpenAI(api_key=api_key)
            full_response = ""
            message_placeholder = st.empty()
            
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt_text},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{base64_image}",
                                },
                            },
                        ],
                    }
                ],
                max_tokens=500,
            )
            
            if response.choices[0].message.content is not None:
                full_response += response.choices[0].message.content
                message_placeholder.markdown(full_response)
                
        except Exception as e:
            st.error(f"An error occurred: {e}")
else:
    if not ke and analyze_button:
        st.warning("Por favor ingresa tu API key.")
