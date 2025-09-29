# process_pdf.py

import os
import requests # Biblioteca para fazer o download
from dotenv import load_dotenv
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("A chave da API da OpenAI não foi encontrada. Verifique seu arquivo .env")

# --- CONFIGURAÇÃO DO DOWNLOAD ---
PDF_URL = "https://drive.google.com/uc?id=1TcMDmuq4R8LXrTMKSaqx88pQOPUTomNm"
PDF_LOCAL_PATH = "livro_geologia.pdf"

# --- ETAPA DE DOWNLOAD ---
print(f"Baixando o PDF de: {PDF_URL}")
try:
    response = requests.get(PDF_URL, stream=True)
    response.raise_for_status()  # Verifica se a requisição foi bem-sucedida

    with open(PDF_LOCAL_PATH, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f"PDF salvo localmente em: {PDF_LOCAL_PATH}")
except requests.exceptions.RequestException as e:
    print(f"Erro ao baixar o PDF: {e}")
    exit() # Encerra o script se o download falhar

# --- O RESTO DO SCRIPT CONTINUA IGUAL ---

# 1. Carregar o PDF (o arquivo que acabamos de baixar)
print("Carregando o PDF...")
loader = PyPDFLoader(PDF_LOCAL_PATH)
documents = loader.load()
print(f"O PDF foi carregado. Total de {len(documents)} páginas.")

# 2. Dividir em Chunks
print("Dividindo o texto em chunks...")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
docs = text_splitter.split_documents(documents)
print(f"Texto dividido em {len(docs)} chunks.")

# 3. Criar os Embeddings e o Banco Vetorial FAISS
print("Criando embeddings e o banco de dados vetorial...")
embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
db = FAISS.from_documents(docs, embeddings)

# 4. Salvar o banco de dados localmente
db.save_local("faiss_index")
print("\nProcessamento concluído! O índice FAISS foi salvo na pasta 'faiss_index'.")
