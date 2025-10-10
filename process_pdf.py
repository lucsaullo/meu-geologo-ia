# Arquivo: process_pdf.py

# --- Bloco de correção para o sqlite3 ---
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
import os
import requests
import chromadb
from dotenv import load_dotenv
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma

load_dotenv()
OPENAI_API_KEY = os.getenv("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")

if not OPENAI_API_KEY:
    print("ERRO: A chave da API da OpenAI não foi encontrada durante o build!")
    exit(1) # Sai com código de erro para falhar o build

PDF_URL = "https://drive.google.com/uc?id=1TcMDmuq4R8LXrTMKSaqx88pQOPUTomNm"
PDF_LOCAL_PATH = "livro_geologia.pdf"
CHROMA_PATH = "chroma_index"

print(f"Iniciando o download do PDF de: {PDF_URL}")
try:
    response = requests.get(PDF_URL, stream=True)
    response.raise_for_status()
    with open(PDF_LOCAL_PATH, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f"PDF salvo com sucesso em: {PDF_LOCAL_PATH}")
except requests.exceptions.RequestException as e:
    print(f"FATAL: Erro ao baixar o PDF: {e}")
    exit(1)

print("Carregando o documento PDF...")
loader = PyPDFLoader(PDF_LOCAL_PATH)
documents = loader.load()
print(f"PDF carregado. Contém {len(documents)} páginas.")

print("Dividindo o texto em pedaços (chunks)...")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
docs = text_splitter.split_documents(documents)
print(f"Texto dividido em {len(docs)} chunks.")

print("Iniciando a criação dos embeddings e do índice ChromaDB...")
embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
# Cria o banco de dados ChromaDB a partir dos documentos e o salva no disco
db = Chroma.from_documents(
    docs, embeddings, persist_directory=CHROMA_PATH
)
print("\nProcessamento concluído com sucesso! O índice 'chroma_index' foi criado.")
