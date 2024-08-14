import requests
import time
import random
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

def selenium_login():
    # Recuperando credenciais das variáveis de ambiente
    username = os.getenv('ONABET_USERNAME')
    password = os.getenv('ONABET_PASSWORD')

    if not username or not password:
        print("Erro: Usuário ou senha não fornecidos.")
        return None

    # Configurar as opções do Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Rodar em modo headless (sem janela)
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Caminho para o driver do Chrome
    service = Service(executable_path='/caminho/para/chromedriver')  # Substitua pelo caminho para o chromedriver

    # Inicializar o driver do navegador
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Acessar a página de login
        driver.get('https://onabet.com/login')

        # Encontrar os campos de entrada de usuário e senha e inserir as credenciais
        driver.find_element(By.ID, 'username').send_keys(username)
        driver.find_element(By.ID, 'password').send_keys(password)
        driver.find_element(By.ID, 'login_button').click()  # Substitua pelo seletor correto

        # Capturar cookies e headers após o login
        cookies = {cookie['name']: cookie['value'] for cookie in driver.get_cookies()}
        headers = {'User-Agent': driver.execute_script("return navigator.userAgent;")}

        # Verificar se o login foi bem-sucedido
        if "dashboard" in driver.current_url:
            print("Login bem-sucedido!")
            return cookies, headers
        else:
            print("Erro no login: Verifique suas credenciais.")
            return None

    finally:
        # Fechar o navegador
        driver.quit()

def send_api_request(cookies, headers):
    # Recuperando credenciais das variáveis de ambiente
    password = os.getenv('ONABET_PASSWORD')

    # Configurando os dados de login para a API
    json_data = {
        'id': '5801',  # Verifique se este ID é o correto para o site
        'values': {
            'Captcha_input': '',  # Ajuste conforme necessário
            'multichannel': '',   # Ajuste conforme necessário
            'password': password,
        },
        'fingerprint': '',  # Verifique se isso é necessário
    }

    # Criando uma sessão para persistir cookies
    session = requests.Session()

    # Adicionar cookies à sessão
    session.cookies.update(cookies)

    # Fazendo a requisição de login
    response = session.post('https://onabet.com/api/client/clients:login-with-form', headers=headers, json=json_data)

    # Verificação de status e tratamento de erros
    if response.status_code == 200:
        if "success" in response.text:  # Ajuste isso para verificar sucesso real
            print("Login bem-sucedido na API!")
            return response
        else:
            print("Erro no login: Verifique suas credenciais.")
            return None
    else:
        print("Erro no login:", response.text)
        return None

def generate_curl_command(cookies, headers, json_data):
    curl_command = "curl -X POST 'https://onabet.com/api/client/clients:login-with-form' \\\n"
    for key, value in headers.items():
        curl_command += f"  -H '{key}: {value}' \\\n"
    for key, value in cookies.items():
        curl_command += f"  --cookie '{key}={value}' \\\n"
    curl_command += f"  -d '{json.dumps(json_data)}'"
    return curl_command

def save_to_json(response):
    # Salvar a resposta da API em um arquivo JSON
    with open('response.json', 'w') as json_file:
        json.dump(response.json(), json_file, indent=4)

def main():
    # Realizar login via Selenium para contornar proteções
    login_data = selenium_login()

    if login_data:
        cookies, headers = login_data

        # Realizar requisição API usando cookies e headers obtidos via Selenium
        response = send_api_request(cookies, headers)

        if response:
            # Gerar comando curl
            json_data = {
                'id': '5801',
                'values': {
                    'Captcha_input': '',
                    'multichannel': '',
                    'password': os.getenv('ONABET_PASSWORD'),
                },
                'fingerprint': '',
            }
            curl_command = generate_curl_command(cookies, headers, json_data)
            print("\nComando cURL gerado:\n")
            print(curl_command)

            # Salvar resposta da API em arquivo JSON
            save_to_json(response)

if __name__ == "__main__":
    main()

