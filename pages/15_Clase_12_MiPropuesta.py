import os
import base64
import numpy as np
from PIL import Image
import streamlit as st
from streamlit_drawable_canvas import st_canvas
import openai

def encode_image_to_base64(image_path):
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
    except FileNotFoundError:
        return None

st.set_page_config(page_title='Generador de Criaturas Fantásticas 👾', page_icon='👾', layout='centered')
st.title("👾 Generador de Criaturas y Monstruos Fantásticos")

with st.sidebar:
    stroke_width = st.slider('Ancho del pincel', 1, 30, 5)
    stroke_color = st.color_picker('Color de trazo', '#000000')

canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)", stroke_width=stroke_width,
    stroke_color=stroke_color, background_color="#FFFFFF",
    height=320, width=450, drawing_mode="freedraw", key="canvas_monstruo",
)

ke = st.text_input('🔑 Ingresa tu OpenAI API Key:', type="password")

if canvas_result.image_data is not None and st.button("🚀 ¡Analizar Criatura!"):
    if not ke:
        st.warning("⚠️ Por favor ingresa tu OpenAI API Key.")
    else:
        openai.api_key = ke
        with st.spinner("⚡ Identificando especie..."):
            input_numpy_array = np.array(canvas_result.image_data)
            input_image = Image.fromarray(input_numpy_array.astype('uint8'), 'RGBA')
            input_image.save('boceto.png')
            base64_image = encode_image_to_base64("boceto.png")
            
            prompt_text = "Crea una ficha estilo Pokémon para esta criatura dibujada en español."
            
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": prompt_text},
                                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}}
                            ]
                        }
                    ],
                    max_tokens=600
                )
                st.success("¡Ficha Creada!")
                st.markdown(response.choices[0].message.content)
            except Exception as e:
                st.error(f"Error: {e}")
