
import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pypdf

# ---------------------------------------------------------
# CONFIGURACIÓN DE PÁGINA Y ESTILOS
# ---------------------------------------------------------
st.set_page_config(
    page_title="Buscador Inteligente TF-IDF 🔍",
    page_icon="🔍",
    layout="wide"
)

st.markdown("""
    <style>
    /* Ocultar elementos predeterminados */
    .block-container {padding-top: 2rem !important; padding-bottom: 2rem !important;}

    /* Fondo principal */
    .stApp {
        background-color: #F8F9FA;
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }

    /* Titular */
    .title-text {
        color: #2D3748;
        font-weight: 800;
        font-size: 2.2rem;
        margin-bottom: 0px;
    }
    
    .subtitle-text {
        color: #718096;
        font-size: 1.05rem;
        margin-bottom: 25px;
    }

    /* Botón de acento llamativo */
    .stButton>button {
        background-color: #FF6B6B !important;
        color: white !important;
        border-radius: 12px !important;
        padding: 12px 24px !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        border: none !important;
        box-shadow: 0px 4px 12px rgba(255, 107, 107, 0.3) !important;
        transition: all 0.2s ease-in-out !important;
        width: 100%;
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0px 6px 16px rgba(255, 107, 107, 0.4) !important;
    }

    /* Tarjetas de resultados */
    .result-card {
        background-color: #FFFFFF;
        border-radius: 14px;
        padding: 18px;
        border-left: 5px solid #FF6B6B;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.03);
        margin-bottom: 12px;
    }

    /* Campo de texto e inputs */
    .stTextArea textarea, .stTextInput input {
        border-radius: 12px !important;
        border: 1.5px solid #E2E8F0 !important;
    }

    /* File uploader personalizado */
    [data-testid="stFileUploader"] {
        border: 2px dashed #CBD5E0;
        border-radius: 14px;
        padding: 10px;
        background-color: #FFFFFF;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# FUNCIONES AUXILIARES DE PROCESAMIENTO
# ---------------------------------------------------------
def process_uploaded_file(uploaded_file):
    documents = []
    if uploaded_file is not None:
        file_ext = uploaded_file.name.split('.')[-1].lower()
        if file_ext == 'txt':
            content = uploaded_file.read().decode('utf-8')
            documents = [line.strip() for line in content.split('\n') if line.strip()]
        elif file_ext == 'pdf':
            pdf_reader = pypdf.PdfReader(uploaded_file)
            for page in pdf_reader.pages:
                text = page.extract_text()
                if text:
                    lines = [line.strip() for line in text.split('\n') if line.strip()]
                    documents.extend(lines)
        elif file_ext == 'csv':
            df = pd.read_csv(uploaded_file)
            first_text_col = df.select_dtypes(include=['object']).columns
            if len(first_text_col) > 0:
                documents = df[first_text_col[0]].dropna().astype(str).tolist()
    return documents

# ---------------------------------------------------------
# ENCABEZADO Y MÉTRICAS (Nielsen #1: Visibilidad)
# ---------------------------------------------------------
st.markdown('<h1 class="title-text">🔍 Buscador Inteligente TF-IDF</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle-text">Analiza documentos y encuentra las respuestas más relevantes usando Similitud Coseno.</p>', unsafe_allow_html=True)

# ---------------------------------------------------------
# ESTRUCTURA EN DOS COLUMNAS
# ---------------------------------------------------------
col_left, col_right = st.columns([1.1, 0.9], gap="large")

with col_left:
    st.markdown("### 📄 1. Fuente de Datos")
    
    tab_input, tab_file = st.tabs(["✍️ Escribir Texto", "📁 Adjuntar Archivo (.txt, .pdf, .csv)"])
    
    default_docs = (
        "El perro ladra fuerte en el parque.\n"
        "El gato maúlla suavemente durante la noche.\n"
        "El perro y el gato juegan juntos en el jardín.\n"
        "Los niños corren y se divierten en el parque.\n"
        "La música suena muy alta en la fiesta.\n"
        "Los pájaros cantan hermosas melodías al amanecer."
    )
    
    documents = []
    
    with tab_input:
        raw_text = st.text_area("Ingresa un documento por línea:", value=default_docs, height=180)
        if raw_text:
            documents = [line.strip() for line in raw_text.split('\n') if line.strip()]

    with tab_file:
        uploaded_file = st.file_uploader("Arrastra tu archivo aquí para convertirlo a colección TF-IDF", type=['txt', 'pdf', 'csv'])
        if uploaded_file:
            uploaded_docs = process_uploaded_file(uploaded_file)
            if uploaded_docs:
                documents = uploaded_docs
                st.success(f"¡Archivo procesado con éxito! ({len(documents)} líneas detectadas)")
            else:
                st.warning("No se pudo extraer texto legible del archivo.")

    st.markdown("### ❓ 2. Consulta")
    user_query = st.text_input("Escribe tu pregunta o palabras clave:", value="¿Dónde juegan el perro y el gato?")

    # Botón con color de acento
    btn_search = st.button("🚀 Analizar Similitud TF-IDF")

with col_right:
    st.markdown("### 💡 Preguntas Sugeridas")
    
    # Preguntas rápidas para hacer clic e interactuar de inmediato
    col_q1, col_q2 = st.columns(2)
    with col_q1:
        if st.button("🐕 ¿Dónde juegan el perro y el gato?"):
            user_query = "¿Dónde juegan el perro y el gato?"
        if st.button("🎵 ¿Dónde suena la música alta?"):
            user_query = "¿Dónde suena la música alta?"
    with col_q2:
        if st.button("🏃 ¿Qué hacen los niños en el parque?"):
            user_query = "¿Qué hacen los niños en el parque?"
        if st.button("🐦 ¿Cuándo cantan los pájaros?"):
            user_query = "¿Cuándo cantan los pájaros?"

    st.write("---")

    # ---------------------------------------------------------
    # PROCESAMIENTO TF-IDF Y RESULTADOS
    # ---------------------------------------------------------
    if documents and user_query:
        # Cálculo de TF-IDF
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(documents)
        query_vector = vectorizer.transform([user_query])
        
        # Similitud Coseno
        similarities = cosine_similarity(query_vector, tfidf_matrix).flatten()
        
        # Formatear resultados
        results_df = pd.DataFrame({
            'Documento': documents,
            'Similitud': similarities
        }).sort_values(by='Similitud', ascending=False)

        st.markdown("### 🎯 Resultados más Relevantes")
        
        top_results = results_df.head(3)
        for idx, row in top_results.iterrows():
            score_percentage = int(row['Similitud'] * 100)
            st.markdown(f"""
                <div class="result-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <strong style="color: #2D3748; font-size: 1.05rem;">{row['Documento']}</strong>
                        <span style="background-color: #FFE3E3; color: #FF6B6B; font-weight: 700; padding: 4px 10px; border-radius: 20px; font-size: 0.85rem;">
                            {score_percentage}% coincidencia
                        </span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

        with st.expander("📊 Ver tabla completa de métricas TF-IDF"):
            st.dataframe(results_df, use_container_width=True)
