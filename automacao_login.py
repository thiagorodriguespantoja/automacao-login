import requests
import time
import random
from fake_useragent import UserAgent

def login(username, password):
    cookies = {}
    headers = {}
    
    # Configurando os dados de login
    json_data = {
        'id': '5801',  # Verifique se este ID é o correto para o site
        'values': {
            'Captcha_input': '',  # Ajuste conforme necessário
            'multichannel': '',   # Ajuste conforme necessário
            'password': password,
        },
        'fingerprint': '',  # Verifique se isso é necessário
    }

    # Simulação de comportamento humano
    time.sleep(random.uniform(2, 5))
    headers['User-Agent'] = UserAgent().random

    # Criando uma sessão para persistir cookies
    session = requests.Session()
    
    # Fazendo a requisição de login
    response = session.post('https://onabet.com/api/client/clients:login-with-form', cookies=cookies, headers=headers, json=json_data)

    # Verificação de status e tratamento de erros
    if response.status_code == 200:
        # Verificar se o login foi bem-sucedido pelo conteúdo da resposta
        if "success" in response.text:  # Ajuste isso para verificar sucesso real
            print("Login bem-sucedido!")
        else:
            print("Erro no login: Verifique suas credenciais.")
    else:
        print("Erro no login:", response.text)

# Chamada da função login
login("seu_usuario", "sua_senha")
