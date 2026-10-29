import os
import base64
import streamlit as st
from openai import OpenAI

def encode_image(image_file):
    return base64.b64encode(image_file.getvalue()).decode("utf-8")

st.title("Análisis de Imagen:🤖🏞️")

ke = st.text_input('Ingresa tu Clave', type="password")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])

if uploaded_file:
    with st.expander("Image", expanded=True):
        st.image(uploaded_file, caption=uploaded_file.name, use_container_width=True)

show_details = st.toggle("Pregunta algo específico sobre la imagen", value=False)

additional_details = ""
if show_details:
    additional_details = st.text_area(
        "Adiciona contexto de la imagen aquí:",
        disabled=not show_details
    )

analyze_button = st.button("Analiza la imagen", type="secondary")

if analyze_button:
    if not ke:
        st.warning("Por favor ingresa tu API key.")
    elif not uploaded_file:
        st.warning("Please upload an image.")
    else:
        with st.spinner("Analizando ..."):
            try:
                client = OpenAI(api_key=ke)
                base64_image = encode_image(uploaded_file)
            
                prompt_text = "Describe what you see in the image in spanish"
            
                if show_details and additional_details:
                    prompt_text += f"\n\nAdditional Context Provided by the User:\n{additional_details}"
            
                messages = [
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt_text},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            },
                        ],
                    }
                ]
            
                full_response = ""
                message_placeholder = st.empty()
                for completion in client.chat.completions.create(
                    model="gpt-4o",
                    messages=messages,   
                    max_tokens=1200,
                    stream=True
                ):
                    if completion.choices[0].delta.content is not None:
                        full_response += completion.choices[0].delta.content
                        message_placeholder.markdown(full_response + "▌")
                        
                message_placeholder.markdown(full_response)
            
            except Exception as e:
                st.error(f"An error occurred: {e}")
