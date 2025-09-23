import os
import tempfile

import streamlit as st

from decouple import config

from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings


os.environ['OPENAI_API_KEY'] = config('OPENAI_API_KEY')
persist_directory = 'db'

st.set_page_config(
    page_title='Chat PyGPT',
    page_icon='📄',
)
st.header('🤖 Chat com seus documentos (RAG)')

with st.sidebar:
    st.header('Upload de arquivos 📄')
    uploaded_files = st.file_uploader(
        label='Faça o upload de arquivos PDF',
        type=['pdf'],
        accept_multiple_files=True,
    )

    model_options = [
            'gpt-3.5-turbo',
            'gpt-4',
            'gpt-4-turbo',
            'gpt-4o-mini',
            'gpt-4o',
        ]
    selected_model = st.sidebar.selectbox(
            label='Selecione o modelo LLM',
            options=model_options,
        )
    
question = st.chat_input('Como posso ajudar?')
st.chat_message("user").write(question)

