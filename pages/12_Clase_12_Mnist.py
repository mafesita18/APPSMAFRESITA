import os
import streamlit as st
import numpy as np
import tensorflow as tf
from tensorflow import keras
from PIL import Image
from streamlit_drawable_canvas import st_canvas

st.set_page_config(
    page_title="Detector de Dígitos MNIST",
    page_icon="✍️",
    layout="wide"
)

with st.sidebar:
    st.write(f"**TensorFlow:** {tf.__version__}")

st.title("✍️ Detección de Dígitos Escritos a Mano")
st.markdown("**Modelo CNN entrenado en Google Colab con MNIST**")

@st.cache_resource
def load_mnist_model():
    model_files = ['mnist_model.keras', 'mnist_model.h5']
    for model_path in model_files:
        if os.path.exists(model_path):
            try:
                model = keras.models.load_model(model_path)
                return model
            except Exception:
                continue
    return None

model = load_mnist_model()

st.write("### 🎨 Dibuja un dígito del 0 al 9")
col1, col2 = st.columns([2, 1])

with col1:
    canvas_result = st_canvas(
        fill_color="black", stroke_width=20, stroke_color="white",
        background_color="black", width=400, height=400,
        drawing_mode="freedraw", key="canvas_mnist",
    )

with col2:
    predict_btn = st.button("🔍 **Predecir**", type="primary", use_container_width=True)

if predict_btn and canvas_result.image_data is not None and model is not None:
    if np.max(canvas_result.image_data) == 0:
        st.warning("⚠️ Por favor, dibuja un dígito primero")
    else:
        with st.spinner("Analizando..."):
            image = Image.fromarray(canvas_result.image_data.astype("uint8")).convert("L")
            image_resized = image.resize((28, 28), Image.Resampling.LANCZOS)
            img_array = np.array(image_resized) / 255.0
            img_array = img_array.reshape(1, 28, 28, 1)
            prediction = model.predict(img_array, verbose=0)
            digit = np.argmax(prediction)
            confidence = np.max(prediction) * 100
        
        st.success(f"## 🎯 Dígito detectado: **{digit}**")
        st.metric("Confianza", f"{confidence:.1f}%")
