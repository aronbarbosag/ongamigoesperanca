import os
import base64
import requests
from dotenv import load_dotenv
from pix.models import Pagamento
from django.http import Http404
from pix.forms import PagamentoForm
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

# Carregando variáveis de ambiente
load_dotenv(override=True)
GERENCIANET_PIX_KEY = os.getenv("GERENCIANET_PIX_KEY")


def index(request):
    return render(request, "app/index.html", {"idBody": " "})


def sobre(request):
    return render(request, "app/sobre.html", {"idBody": "sobre"})


def transparencia(request):
    return render(request, "app/transparencia.html", {"idBody": "transparencia"})


def voluntariado(request):
    return render(request, "app/voluntariado.html", {"idBody": "voluntariado"})


def contato(request):
    return render(request, "app/contato.html", {"idBody": "contato"})

@csrf_exempt
def doacao(request):
    if request.method == 'POST':
        
        return processar_formulario(request)
        
    else:
        form = PagamentoForm()
        return render(request, "app/doacao.html", {"idBody": "doacao", "form": form})

def processar_formulario(request):
    form = PagamentoForm(request.POST)
    if form.is_valid():
        valor = form.cleaned_data.get('valor', None)  # Use o get() para garantir que não seja None
        
        if valor == "custom":  # Caso o valor personalizado esteja selecionado
            valor = request.POST.get("valor_personalizado", None)
        
        try:
            if valor is not None:
                valor = float(valor)  # Garantir que o valor seja um número
            else:
                raise ValueError("Valor não informado.")
        except ValueError:
            form.add_error("valor", "Informe um número válido para o valor da doação.")
            print('valueerror no except valuerror')
            return render(request, 'pix/formulario_pagamento.html', {'form': form})

        # Agora que o valor está validado como float, salve o pagamento
        pagamento = form.save(commit=False)
        pagamento.valor = valor  # Define o valor como float
        pagamento.save()

        # O restante do processamento
        try:
            access_token = obter_access_token()
            payload = criar_payload(pagamento)
            cobranca_data = enviar_requisicao_cobranca(payload, access_token)

            pagamento.txid = cobranca_data.get('txid')
            pagamento.id_loc = cobranca_data.get('loc', {}).get('id')
            pagamento.save()

            detalhes_data = obter_detalhes_cobranca(pagamento.id_loc, access_token)
            pagamento.qr_code = detalhes_data.get('qrcode')
            pagamento.link_visualizacao = detalhes_data.get('linkVisualizacao')
            pagamento.imagem_qrcode = detalhes_data.get('imagemQrcode')
            pagamento.status = "pendente"
            pagamento.save()

            # Exibindo os dados no modal
            return render(request, 'app/doacao.html', {
                'form': form,
                'qr_code': pagamento.qr_code,
                'link_visualizacao': pagamento.link_visualizacao,
                'imagem_qrcode': pagamento.imagem_qrcode,
                'id_loc': pagamento.id_loc,
                'status': pagamento.status
            })
        except Exception as e:
            return render(request, 'pix/erro.html', {'erro': str(e)})

    # Se houver erros no formulário, exibe-os na página
    return render(request, 'pix/formulario_pagamento.html', {'form': form})

def obter_access_token():
    """
    Função que faz a requisição para o endpoint OAuth para obter o access_token.
    Retorna o access_token obtido da resposta.
    """
    url = "https://pix-h.api.efipay.com.br/oauth/token"

    # Recuperando as credenciais do arquivo .env
    client_id = os.getenv("CLIENT_ID_HOMOLOGACAO")
    client_secret = os.getenv("CLIENT_SECRET_HOMOLOGACAO")
    cert_file = os.getenv("CERT_FILE_HOMOLOGACAO")

    if not client_id or not client_secret:
        raise ValueError("CLIENT_ID e CLIENT_SECRET devem estar definidos no arquivo .env.")

    # Dados necessários para a requisição OAuth
    data = {
        'grant_type': 'client_credentials',
    }

    auth_value = f"{client_id}:{client_secret}"
    auth_base64 = base64.b64encode(auth_value.encode('utf-8')).decode('utf-8')

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f'Basic {auth_base64}'
    }

    try:
        response = requests.post(url, data=data, headers=headers, cert=cert_file)
        response.raise_for_status()

        access_token = response.json().get('access_token')
        if not access_token:
            raise ValueError("Token de acesso não encontrado na resposta.")
        return access_token

    except requests.exceptions.RequestException as e:
        raise Exception(f"Erro ao fazer a requisição do token: {e}")

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
        response = requests.post(url, json=payload, headers=headers, cert=cert_file, timeout=30)
        response.raise_for_status()
        # print(f"Resposta da cobrança: {response.json()}")
        return response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Erro na requisição de cobrança: {e}")


def obter_detalhes_cobranca(id_loc, access_token):
    """Obtém os detalhes da cobrança pelo id_loc."""
    detalhes_url = f"https://pix-h.api.efipay.com.br/v2/loc/{id_loc}/qrcode"
    headers = {'Authorization': f'Bearer {access_token}'}
    cert_file = os.getenv("CERT_FILE_HOMOLOGACAO")

    try:
        response = requests.get(detalhes_url, headers=headers, cert=cert_file, timeout=20)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Erro ao obter detalhes da cobrança: {e}")


def sucesso(request, id_loc):
    try:
        pagamento = Pagamento.objects.get(id_loc=id_loc)
    except Pagamento.DoesNotExist:
        raise Http404("Pagamento não encontrado.")

    return render(request, 'pix/sucesso.html', {'pagamento': pagamento})


def eventos(request):
    return render(request, "app/eventos.html", {"idBody": "eventos"})


def area_restrita(request):
    return render(request, "app/area-restrita.html", {"idBody": "area-restrita"})


def custom_404(request, exception):
    return render(request, "app/404.html", {"idBody": "doacao"})
