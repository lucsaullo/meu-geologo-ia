# Arquivo: api/ask_geologist.py

# --- Bloco de correção para o sqlite3 ---
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import json
import os
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI

OPENAI_API_KEY = os.getenv("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")
CHROMA_PATH = "chroma_index"

def handler(event, context):
    if event['httpMethod'] != 'POST':
        return {'statusCode': 405, 'body': json.dumps({'error': 'Método não permitido'})}

    try:
        body = json.loads(event['body'])
        question = body.get('question')
        if not question:
            return {'statusCode': 400, 'body': json.dumps({'error': 'Nenhuma pergunta foi fornecida'})}

        # Carrega o índice ChromaDB do disco
        embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
        vectorstore = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)

        qa_chain = ConversationalRetrievalChain.from_llm(
            llm=ChatOpenAI(openai_api_key=OPENAI_API_KEY, model_name="gpt-3.5-turbo"),
            retriever=vectorstore.as_retriever(),
            return_source_documents=True
        )

        result = qa_chain({'question': question, 'chat_history': []})
        answer = result['answer']
        
        source_quote = "Nenhuma fonte encontrada."
        source_page = "N/A"
        if result['source_documents']:
            source_document = result['source_documents'][0]
            source_quote = source_document.page_content
            source_page = source_document.metadata.get('page', 'N/A')
            if isinstance(source_page, int):
                source_page += 1

        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({
                'answer': answer,
                'source_quote': source_quote,
                'source_page': source_page
            })
        }
    except Exception as e:
        print(f"Erro inesperado: {e}")
        return {'statusCode': 500, 'body': json.dumps({'error': 'Ocorreu um erro interno no servidor.'})}
