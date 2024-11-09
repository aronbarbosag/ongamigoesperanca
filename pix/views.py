import os
import base64
import requests
from .models import Pagamento
from django.http import Http404
from .forms import PagamentoForm
from dotenv import load_dotenv
from django.shortcuts import render, redirect

load_dotenv(override=True)

GERENCIANET_PIX_KEY = os.getenv("GERENCIANET_PIX_KEY")


def processar_cobranca_pix(request):
    """
    Função principal que coordena todo o processo de criação de cobrança Pix.
    Chama as funções auxiliares para:
    - Processar o formulário.
    - Criar o payload da cobrança.
    - Enviar a requisição de criação de cobrança.
    - Obter os detalhes da cobrança (QR Code).

    Retorna uma resposta HTTP ou redirecionamento.
    """
    if request.method != 'POST':
        form = PagamentoForm()
        return render(request, 'pix/formulario_pagamento.html', {'form': form})

    form = PagamentoForm(request.POST)
    if not form.is_valid():
        return render(request, 'pix/formulario_pagamento.html', {'form': form})

    # Salvando o pagamento inicial
    pagamento = form.save()

    try:
        # Obter o access_token
        access_token = obter_access_token()

        # Criar e enviar a cobrança
        payload = criar_payload(pagamento)
        cobranca_data = enviar_requisicao_cobranca(payload, access_token)

        # Atualiza pagamento com dados de txid e id_loc
        pagamento.txid = cobranca_data.get('txid')
        pagamento.id_loc = cobranca_data.get('loc', {}).get('id')
        pagamento.save()

        # Obter detalhes da cobrança (QR Code)
        detalhes_data = obter_detalhes_cobranca(pagamento.id_loc, access_token)
        pagamento.qr_code = detalhes_data.get('qrCode')
        pagamento.link_visualizacao = detalhes_data.get('linkVisualizacao')
        pagamento.imagem_qrcode = detalhes_data.get('imagemQrcode')
        pagamento.status = "pendente"
        pagamento.save()

        # Redireciona para a página de sucesso
        return redirect('pix:sucesso', id_loc=pagamento.id_loc)

    except Exception as e:
        return render(request, 'pix/erro.html', {'erro': str(e)})


def obter_access_token():
    """
    Função que faz a requisição para o endpoint OAuth para obter o access_token.
    Retorna o access_token obtido da resposta.
    """
    url = "https://pix-h.api.efipay.com.br/oauth/token"

    # Recuperando as credenciais do arquivo .env
    # Defina CLIENT_ID no seu .env
    client_id = os.getenv("CLIENT_ID_HOMOLOGACAO")
    # Defina CLIENT_SECRET no seu .env
    client_secret = os.getenv("CLIENT_SECRET_HOMOLOGACAO")
    cert_file = os.getenv("CERT_FILE_HOMOLOGACAO")

    if not client_id or not client_secret:
        raise ValueError(
            "CLIENT_ID e CLIENT_SECRET devem estar definidos no arquivo .env.")

    # Dados necessários para a requisição OAuth
    data = {
        'grant_type': 'client_credentials',  # Tipo de grant
    }

    auth_value = f"{client_id}:{client_secret}"
    auth_base64 = base64.b64encode(auth_value.encode('utf-8')).decode('utf-8')

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        # Cabeçalho de Autenticação Basic
        'Authorization': f'Basic {auth_base64}'
    }

    try:
        # Fazendo a requisição POST para obter o token
        response = requests.post(
            url, data=data, headers=headers, cert=cert_file)
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


def formatar_valor(valor):
    """Formata o valor para garantir que tenha 2 casas decimais."""
    return "{:.2f}".format(valor)


def criar_payload(pagamento):
    """Cria o payload para a solicitação de cobrança."""
    valor_formatado = formatar_valor(pagamento.valor)
    return {
        "calendario": {"expiracao": 3600},
        "devedor": {"cpf": pagamento.cpf, "nome": pagamento.nome},
        "valor": {"original": str(valor_formatado)},
        "chave": GERENCIANET_PIX_KEY,
        "solicitacaoPagador": "Informe o número ou identificador do pedido."
    }


def enviar_requisicao_cobranca(payload, access_token):
    """Envia a solicitação de criação de cobrança e retorna a resposta."""
    url = "https://pix-h.api.efipay.com.br/v2/cob"
    headers = {'Authorization': f'Bearer {access_token}'}
    cert_file = os.getenv("CERT_FILE_HOMOLOGACAO")

    try:
        response = requests.post(
            url, json=payload, headers=headers, cert=cert_file, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Erro na requisição de cobrança: {e}")


def obter_detalhes_cobranca(id_loc, access_token):
    """Obtém os detalhes da cobrança pelo id_loc."""
    detalhes_url = f"https://pix-h.api.efipay.com.br/v2/loc/{id_loc}/qrcode"
    headers = {'Authorization': f'Bearer {access_token}'}
    cert_file = os.getenv("CERT_FILE_HOMOLOGACAO")

    try:
        response = requests.get(
            detalhes_url, headers=headers, cert=cert_file, timeout=20)
        response.raise_for_status()

        return response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Erro ao obter detalhes da cobrança: {e}")


def processar_formulario(request):
    """Processa o formulário de pagamento e cria a cobrança Pix."""
    form = PagamentoForm(request.POST)
    if form.is_valid():
        pagamento = form.save()
        payload = criar_payload(pagamento)

        try:
            cobranca_data = enviar_requisicao_cobranca(payload)
            pagamento.txid = cobranca_data.get('txid')
            pagamento.id_loc = cobranca_data.get('loc', {}).get('id')
            pagamento.save()

            detalhes_data = obter_detalhes_cobranca(pagamento.id_loc)
            pagamento.qr_code = detalhes_data.get('qrcode')
            pagamento.link_visualizacao = detalhes_data.get('linkVisualizacao')
            pagamento.imagem_qrcode = detalhes_data.get('imagemQrcode')
            pagamento.status = "pendente"
            pagamento.save()

            return redirect('pix:sucesso', id_loc=pagamento.id_loc)
        except Exception as e:
            return render(request, 'pix/erro.html', {'erro': str(e)})

    return render(request, 'pix/formulario_pagamento.html', {'form': form})


def gerar_cobranca_pix(request):
    """Controlador principal para gerar cobrança Pix."""
    if request.method == 'POST':
        return processar_formulario(request)
    else:
        form = PagamentoForm()
        return render(request, 'pix/formulario_pagamento.html', {'form': form})


def sucesso(request, id_loc):
    try:
        # Tentando buscar o pagamento pelo id_loc (como CharField)
        # Usando loc_id para recuperar o pagamento
        pagamento = Pagamento.objects.get(id_loc=id_loc)
    except Pagamento.DoesNotExist:
        # Caso o pagamento não seja encontrado, exibe erro
        raise Http404("Pagamento não encontrado.")

    return render(request, 'pix/sucesso.html', {'pagamento': pagamento})
