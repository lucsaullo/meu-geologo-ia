# Arquivo: process_pdf.py

import os
import requests
from dotenv import load_dotenv
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS

# Carrega as variáveis de ambiente. No deploy da Netlify, ele lerá a chave que configuramos lá.
load_dotenv()
OPENAI_API_KEY = os.getenv("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")

if not OPENAI_API_KEY:
    # Esta verificação é mais útil para testes locais, mas é uma boa prática mantê-la.
    print("ERRO: A chave da API da OpenAI não foi encontrada!")
    exit()

# --- CONFIGURAÇÃO DO DOWNLOAD (com o seu link já convertido) ---
PDF_URL = "https://drive.google.com/uc?id=1TcMDmuq4R8LXrTMKSaqx88pQOPUTomNm"
PDF_LOCAL_PATH = "livro_geologia.pdf"

# --- ETAPA DE DOWNLOAD ---
print(f"Iniciando o download do PDF de: {PDF_URL}")
try:
    response = requests.get(PDF_URL, stream=True)
    response.raise_for_status()  # Verifica se a requisição (GET) foi bem-sucedida

    with open(PDF_LOCAL_PATH, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f"PDF salvo com sucesso em: {PDF_LOCAL_PATH}")
except requests.exceptions.RequestException as e:
    print(f"FATAL: Erro ao baixar o PDF: {e}")
    exit() # Encerra o script se o download falhar para não continuar o build

# --- ETAPAS DE PROCESSAMENTO DA IA ---

# 1. Carregar o PDF (o arquivo que acabamos de baixar)
print("Carregando o documento PDF...")
loader = PyPDFLoader(PDF_LOCAL_PATH)
documents = loader.load()
print(f"PDF carregado. Contém {len(documents)} páginas.")

# 2. Dividir o texto em Chunks
print("Dividindo o texto em pedaços (chunks)...")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
docs = text_splitter.split_documents(documents)
print(f"Texto dividido em {len(docs)} chunks.")

# 3. Criar os Embeddings e o Banco de Dados Vetorial (FAISS)
print("Iniciando a criação dos embeddings e do índice vetorial (isso pode levar um momento)...")
embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
db = FAISS.from_documents(docs, embeddings)

# 4. Salvar o banco de dados localmente para uso futuro
db.save_local("faiss_index")
print("\nProcessamento concluído com sucesso! O índice 'faiss_index' foi criado.")
