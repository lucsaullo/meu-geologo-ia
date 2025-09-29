# process_pdf.py (versão modificada)

import os
import requests # Importe a nova biblioteca
from dotenv import load_dotenv
from langchain.document_loaders import PyPDFLoader
# ... resto dos imports

load_dotenv()
# ...

PDF_URL = "https://drive.google.com/uc?id=SEU_ID_AQUI" # <-- COLOQUE SEU LINK DIRETO AQUI
PDF_LOCAL_PATH = "livro_geologia.pdf"

# --- INÍCIO DA MODIFICAÇÃO ---
print("Baixando o PDF do armazenamento externo...")
response = requests.get(PDF_URL)
response.raise_for_status() # Garante que o download funcionou
with open(PDF_LOCAL_PATH, "wb") as f:
    f.write(response.content)
print("Download do PDF concluído.")
# --- FIM DA MODIFICAÇÃO ---

# 1. Carregar o PDF (agora o arquivo local que acabamos de baixar)
print("Carregando o PDF...")
loader = PyPDFLoader(PDF_LOCAL_PATH)
# ... o resto do script continua exatamente igual
