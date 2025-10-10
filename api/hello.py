# Arquivo: netlify/functions/hello.py
import json

def handler(event, context):
    print("A função hello foi chamada!")
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Olá, mundo! A função simples funcionou!'})
    }
