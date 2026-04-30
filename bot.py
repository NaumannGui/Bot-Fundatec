# 1. Bibliotecas nativas do Python
import os
import smtplib
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# 2. Bibliotecas externas
import requests
from bs4 import BeautifulSoup

# Configuração do diário (Logs)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Variáveis de ambiente e configurações
senha_app = os.getenv('SENHA_APP')
chave_api = os.getenv('API_KEY')
email_remetente = os.getenv('REMETENTE')
email_destinatario = os.getenv('DESTINATARIO')

url = "https://www.fundatec.org.br/portal/concursos/publicacoes_v2.php?concurso=986"
novaURL = f"http://api.scraperapi.com?api_key={chave_api}&url={url}&render=true&country_code=br&premium=true"
nome_do_arquivo = 'ultimo_titulo.txt'


# Função para enviar e-mail
def enviar_email(assunto, texto_corpo):
    mensagem = MIMEMultipart()
    mensagem['From'] = email_remetente
    mensagem['To'] = email_destinatario
    mensagem['Subject'] = assunto
    mensagem.attach(MIMEText(texto_corpo, 'plain', 'utf-8'))

    with smtplib.SMTP('smtp.gmail.com', 587) as servidor:
        servidor.starttls()
        servidor.login(email_remetente, senha_app)
        servidor.sendmail(email_remetente, email_destinatario, mensagem.as_string())
    logging.info(f"E-mail enviado com sucesso: {assunto}")


# Execução principal do robô
try:
    resposta = requests.get(novaURL)
    logging.info(f"Status da resposta: {resposta.status_code}")
    resposta.raise_for_status() 

    sopa_html = BeautifulSoup(resposta.text, 'html.parser')
    publicacoes = sopa_html.find_all('a', class_='eventos')

    primeira_pub = publicacoes[0]
    titulo = primeira_pub.text
    link = primeira_pub['href'].split("'")[1]

    # Verifica se a memória já existe
    if os.path.exists(nome_do_arquivo):
        with open(nome_do_arquivo, 'r', encoding='utf-8') as arquivo:
            titulo_salvo = arquivo.read()
    else:
        titulo_salvo = ""

    # Faz a comparação e usa a função de envio de e-mail se houver novidade
    if titulo != titulo_salvo:
        assunto = "🔔 Novidade no Concurso da Fundatec!"
        corpo = f"O título da publicação é: {titulo}\nDisponível no link: {link}"
        enviar_email(assunto, corpo)
        
        # Atualiza a memória
        with open(nome_do_arquivo, 'w', encoding='utf-8') as arquivo:
            arquivo.write(titulo)
        logging.info("Memória atualizada com o novo título.")
    else:
        logging.info("Nenhuma novidade encontrada nesta execução.")

except Exception as e:
    logging.error(f"Ocorreu um erro: {e}")
    assunto_erro = "⚠️ Erro ao buscar informações da Fundatec"
    corpo_erro = f"Ocorreu um erro ao tentar buscar as publicações.\nDetalhes do erro: {e}"
    enviar_email(assunto_erro, corpo_erro)