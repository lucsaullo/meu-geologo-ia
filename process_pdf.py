# process_pdf.py

import os
from dotenv import load_dotenv
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS

# Carrega as variáveis de ambiente (sua chave da OpenAI)
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("A chave da API da OpenAI não foi encontrada. Verifique seu arquivo .env")

# 1. Carregar o PDF
print("Carregando o PDF...")
loader = PyPDFLoader("livro_geologia.pdf") # Coloque seu PDF na raiz do projeto
# O load_and_split() já extrai o texto e metadados (como a página)
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
# Isso pode demorar um pouco e pode custar alguns centavos na sua conta da OpenAI
db = FAISS.from_documents(docs, embeddings)

# 4. Salvar o banco de dados localmente
db.save_local("faiss_index")

print("\nProcessamento concluído! O índice FAISS foi salvo na pasta 'faiss_index'.")
