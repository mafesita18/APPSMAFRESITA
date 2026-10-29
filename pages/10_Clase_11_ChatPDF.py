import os
import platform
import traceback
import streamlit as st
from PIL import Image
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain

# Configuración de la app
st.title('Generación Aumentada por Recuperación (RAG) 💬')
st.write("Versión de Python:", platform.python_version())

# Cargar y mostrar imagen si existe
try:
    image = Image.open('Chat_pdf.png')
    st.image(image, width=350)
except Exception as e:
    st.warning(f"No se pudo cargar la imagen: {e}")

# Información lateral
with st.sidebar:
    st.subheader("Este Agente te ayudará a realizar análisis sobre el PDF cargado")

# API Key
ke = st.text_input('Ingresa tu Clave de OpenAI', type="password")
if ke:
    os.environ['OPENAI_API_KEY'] = ke
else:
    st.warning("Por favor ingresa tu clave de API de OpenAI para continuar")

# Subir PDF
pdf = st.file_uploader("Carga el archivo PDF", type="pdf")

# Procesar PDF
if pdf is not None and ke:
    try:
        pdf_reader = PdfReader(pdf)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        
        st.info(f"Texto extraído: {len(text)} caracteres")
        
        text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=500,
            chunk_overlap=20,
            length_function=len
        )
        chunks = text_splitter.split_text(text)
        st.success(f"Documento dividido en {len(chunks)} fragmentos")
        
        embeddings = OpenAIEmbeddings()
        knowledge_base = FAISS.from_texts(chunks, embeddings)
        
        st.subheader("Escribe qué quieres saber sobre el documento")
        user_question = st.text_area(" ", placeholder="Escribe tu pregunta aquí...")
        
        if user_question:
            docs = knowledge_base.similarity_search(user_question)
            llm = OpenAI(temperature=0, model_name="gpt-4o-mini-2024-07-18")
            chain = load_qa_chain(llm, chain_type="stuff")
            
            response = chain.run(input_documents=docs, question=user_question)
            
            st.markdown("### Respuesta:")
            st.markdown(response)
                
    except Exception as e:
        st.error(f"Error al procesar el PDF: {str(e)}")
        st.error(traceback.format_exc())
elif pdf is not None and not ke:
    st.warning("Por favor ingresa tu clave de API de OpenAI para continuar")
else:
    st.info("Por favor carga un archivo PDF para comenzar")
