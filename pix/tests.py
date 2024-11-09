from django.test import TestCase
from django.conf import settings
import os
from dotenv import load_dotenv
import requests
import base64

# Create your tests here.

load_dotenv()


def obter_access_token():
    """
    Função que faz a requisição para o endpoint OAuth para obter o access_token.
    Retorna o access_token obtido da resposta.
    """
    url = "https://pix-h.api.efipay.com.br/oauth/token"
    
    # Recuperando as credenciais do arquivo .env
    client_id = os.getenv("CLIENT_ID_HOMOLOGACAO")  # Defina CLIENT_ID no seu .env
    client_secret = os.getenv("CLIENT_SECRET_HOMOLOGACAO")  # Defina CLIENT_SECRET no seu .env
    cert_file = os.getenv("CERT_FILE_HOMOLOGACAO")


    if not client_id or not client_secret:
        raise ValueError("CLIENT_ID e CLIENT_SECRET devem estar definidos no arquivo .env.")

    # Dados necessários para a requisição OAuth
    data = {
        'grant_type': 'client_credentials',  # Tipo de grant
    }

    auth_value = f"{client_id}:{client_secret}"
    auth_base64 = base64.b64encode(auth_value.encode('utf-8')).decode('utf-8')

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f'Basic {auth_base64}'  # Cabeçalho de Autenticação Basic
    }

    try:
        # Fazendo a requisição POST para obter o token
        response = requests.post(url, data=data, headers=headers, cert=cert_file)
        response.raise_for_status()  # Levanta um erro se a requisição falhar
        
        # Extraindo o token da resposta JSON
        access_token = response.json().get('access_token')
        
        if not access_token:
            raise ValueError("Token de acesso não encontrado na resposta.")
        
        return access_token
    
    except requests.exceptions.RequestException as e:
        # Erro na requisição
        print(f"Erro ao fazer a requisição: {e}")
        raise

# Exemplo de uso da função

token = obter_access_token()
print(token)
