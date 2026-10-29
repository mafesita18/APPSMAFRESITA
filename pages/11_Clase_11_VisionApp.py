import os
import streamlit as st
import base64
from PIL import Image
import openai

def encode_image_to_base64(image_path):
    try:
        with open(image_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
            return encoded_image
    except FileNotFoundError:
        return None

st.set_page_config(page_title="Vision App", page_icon="👁️")
st.title("👁️ Análisis de Imágenes con Vision")

uploaded_file = st.file_uploader("Sube una imagen...", type=["jpg", "jpeg", "png"])
ke = st.text_input('Ingresa tu OpenAI API Key:', type="password")

if uploaded_file is not None and ke:
    openai.api_key = ke
    image = Image.open(uploaded_file)
    st.image(image, caption='Imagen subida', use_column_width=True)
    
    if st.button('Analizar Imagen'):
        with st.spinner('Analizando...'):
            image.save('temp_vision.png')
            base64_image = encode_image_to_base64('temp_vision.png')
            
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": "Describe esta imagen en detalle en español:"},
                                {
                                    "type": "image_url",
                                    "image_url": {"url": f"data:image/png;base64,{base64_image}"}
                                }
                            ]
                        }
                    ],
                    max_tokens=500
                )
                st.write(response.choices[0].message.content)
            except Exception as e:
                st.error(f"Error: {e}")
