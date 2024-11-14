import os
import requests
import json
from docx import Document
from dotenv import load_dotenv

# Carregar variáveis de ambiente do .env
load_dotenv()

api_key = os.getenv('AZURE_TRANSLATOR_KEY')
endpoint = os.getenv('AZURE_TRANSLATOR_ENDPOINT')
region = 'your-region'  # Substitua pela sua região Azure

def read_docx(file_path):
    """Ler o conteúdo do arquivo .docx e retornar como texto."""
    doc = Document(file_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

def translate_text(text, to_language='pt'):
    """Traduz o texto usando a API do Azure Translator."""
    path = '/translate'
    constructed_url = endpoint + path

    headers = {
        'Ocp-Apim-Subscription-Key': api_key,
        'Ocp-Apim-Subscription-Region': region,
        'Content-type': 'application/json'
    }

    params = {
        'api-version': '3.0',
        'to': to_language
    }

    body = [{
        'text': text
    }]

    response = requests.post(constructed_url, params=params, headers=headers, json=body)
    response.raise_for_status()

    translated_text = response.json()[0]['translations'][0]['text']
    return translated_text

def apply_glossary(text, glossary_path='glossary.json'):
    """Aplica um glossário de termos técnicos para garantir precisão terminológica."""
    with open(glossary_path, 'r', encoding='utf-8') as file:
        glossary = json.load(file)

    for term, translation in glossary.items():
        text = text.replace(term, translation)
    return text

def translate_docx(file_path, to_language='pt'):
    """Ler, traduz e aplicar glossário no conteúdo de um arquivo .docx."""
    original_text = read_docx(file_path)
    translated_text = translate_text(original_text, to_language)
    final_text = apply_glossary(translated_text)
    return final_text

# Teste da função de tradução com glossário
if __name__ == '__main__':
    translated_content = translate_docx('input.docx', to_language='pt')
    print("Conteúdo traduzido com glossário aplicado:\n", translated_content)
