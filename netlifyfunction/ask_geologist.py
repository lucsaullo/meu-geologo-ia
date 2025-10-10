# Arquivo: netlify/functions/ask_geologist.py

import json
import os
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI

# A chave será lida da variável de ambiente que você configurará na Netlify.
# NUNCA escreva a chave diretamente aqui.
OPENAI_API_KEY = os.getenv("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")
INDEX_PATH = "faiss_index" # Caminho para o índice que o process_pdf.py criou

def handler(event, context):
    # Garante que a requisição da web é um 'POST'
    if event['httpMethod'] != 'POST':
        return {
            'statusCode': 405,
            'body': json.dumps({'error': 'Método não permitido'})
        }

    try:
        # Pega a pergunta que o usuário digitou, que vem no corpo da requisição
        body = json.loads(event['body'])
        question = body.get('question')
        if not question:
            return {'statusCode': 400, 'body': json.dumps({'error': 'Nenhuma pergunta foi fornecida'})}

        # Carrega o índice FAISS (é rápido, pois os cálculos pesados já foram feitos)
        # O allow_dangerous_deserialization=True é necessário para o FAISS com LangChain
        embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
        vectorstore = FAISS.load_local(INDEX_PATH, embeddings, allow_dangerous_deserialization=True)

        # Configura a cadeia de Pergunta e Resposta
        qa_chain = ConversationalRetrievalChain.from_llm(
            llm=ChatOpenAI(openai_api_key=OPENAI_API_KEY, model_name="gpt-3.5-turbo"),
            retriever=vectorstore.as_retriever(),
            return_source_documents=True
        )

        # Faz a pergunta à IA
        result = qa_chain({'question': question, 'chat_history': []})
        answer = result['answer']
        
        # Extrai o trecho e a página do documento fonte mais relevante
        # Às vezes pode não haver documentos fonte, então tratamos esse caso
        source_quote = "Nenhuma fonte encontrada."
        source_page = "N/A"
        if result['source_documents']:
            source_document = result['source_documents'][0]
            source_quote = source_document.page_content
            # O PyPDFLoader numera páginas a partir do 0, então somamos 1 para a leitura humana
            source_page = source_document.metadata.get('page', 'N/A')
            if isinstance(source_page, int):
                source_page += 1

        # Retorna a resposta final formatada em JSON para o frontend
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*' # Permite que qualquer site acesse (importante para o dev)
            },
            'body': json.dumps({
                'answer': answer,
                'source_quote': source_quote,
                'source_page': source_page
            })
        }

    except Exception as e:
        # Em caso de erro, retorna uma mensagem clara para ajudar na depuração
        print(f"Erro inesperado: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Ocorreu um erro interno no servidor.'})
        }
