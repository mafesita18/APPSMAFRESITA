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

st.title('Tablero Inteligente')
st.sidebar.subheader("En esta aplicación veremos la capacidad de interpretar un boceto")

canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)", stroke_width=5,
    stroke_color="#000000", background_color='#FFFFFF',
    height=300, width=400, drawing_mode="freedraw", key="canvas_drawrecog",
)

ke = st.text_input('Ingresa tu Clave', type="password")

if canvas_result.image_data is not None and ke and st.button("Analiza la imagen"):
    openai.api_key = ke
    with st.spinner("Analizando..."):
        input_numpy_array = np.array(canvas_result.image_data)
        input_image = Image.fromarray(input_numpy_array.astype('uint8'), 'RGBA')
        input_image.save('img.png')
        base64_image = encode_image_to_base64("img.png")
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "Describe the image in spanish"},
                            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}}
                        ]
                    }
                ],
                max_tokens=500
            )
            st.write(response.choices[0].message.content)
        except Exception as e:
            st.error(f"Error al consultar la API: {e}")
            st.write(response.choices[0].message.content)
        except Exception as e:
            st.error(f"Error: {e}")
