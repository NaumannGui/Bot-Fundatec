import requests, os, smtplib, logging
from bs4 import BeautifulSoup
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Configuramos o formato do diário: vai mostrar a Hora, o Nível de gravidade e a Mensagem
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

senha_app = os.getenv('SENHA_APP')  # Certifique-se de definir a variável de ambiente 'SENHA_APP' com a senha do aplicativo do Gmail
chave_api = os.getenv('API_KEY')  # Certifique-se de definir a variável de ambiente 'API_KEY' com a chave do proxy
url = "https://www.fundatec.org.br/portal/concursos/publicacoes_v2.php?concurso=986"
novaURL = f"http://api.scraperapi.com?api_key={chave_api}&url={url}&render=true&country_code=br&premium=true"

nome_do_arquivo = 'ultimo_titulo.txt'
email_remetente = os.getenv('REMETENTE')  # Certifique-se de definir a variável de ambiente 'EMAIL_REMETENTE' com o email do remetente (pode ser o seu)
email_destinatario = os.getenv('DESTINATARIO')  # Certifique-se de definir a variável de ambiente 'EMAIL_DESTINATARIO' com o email do destinatário (pode ser o seu ou o dela)

try:
    resposta = requests.get(novaURL)
    logging.info(f"Status da resposta: {resposta.status_code}")  # Loga o status da resposta
    logging.info(f"Conteúdo da resposta: {resposta.text[:1000]}")  # Loga os primeiros 1000 caracteres do conteúdo para verificar se está correto
    resposta.raise_for_status() # Se o status for erro (ex: 404, 500), ele pula pro except na hora

    sopa_html = BeautifulSoup(resposta.text, 'html.parser')
    publicacoes = sopa_html.find_all('a', class_='eventos')

    primeira_pub = publicacoes[0]
    titulo = primeira_pub.text
    link = primeira_pub['href'].split("'")[1]  # Extrai o link corretamente

    # Criando o envelope
    mensagem = MIMEMultipart()
    mensagem['From'] = email_remetente
    mensagem['To'] = email_destinatario # Pode ser o seu ou o dela
    mensagem['Subject'] = "🔔 Novidade no Concurso da Fundatec!"

    corpo = f"O título da publicação é : {titulo}, disponível no link {link}"

    mensagem.attach(MIMEText(corpo, 'plain', 'utf-8'))

    # 1. Verifica se a memória já existe
    if os.path.exists(nome_do_arquivo):
        with open(nome_do_arquivo, 'r', encoding='utf-8') as arquivo:
            titulo_salvo = arquivo.read()
    else:
        # Se não existe (primeira vez), deixamos vazio
        titulo_salvo = ""

    # 2. Faz a comparação
    if titulo != titulo_salvo:
        with smtplib.SMTP('smtp.gmail.com', 587) as servidor:
            servidor.starttls()  # Ativa a criptografia/segurança
            servidor.login(email_remetente, senha_app)
            servidor.sendmail(email_remetente, email_destinatario, mensagem.as_string())
    
    # Atualiza a memória com o novo título
    with open(nome_do_arquivo, 'w', encoding='utf-8') as arquivo:
        arquivo.write(titulo)

except Exception as e:
        logging.error(f"Ocorreu um erro: {e}")  # Loga o erro para diagnóstico
        mensagem_erro = MIMEMultipart()
        mensagem_erro['From'] = email_remetente
        mensagem_erro['To'] = email_destinatario
        mensagem_erro['Subject'] = "⚠️ Erro ao buscar informações da Fundatec"
        corpo_erro = f"Ocorreu um erro ao tentar buscar as publicações. Detalhes do erro: {e}"
        mensagem_erro.attach(MIMEText(corpo_erro, 'plain', 'utf-8'))
        with smtplib.SMTP('smtp.gmail.com', 587) as servidor:
            servidor.starttls()
            servidor.login(email_remetente, senha_app)
            servidor.sendmail(email_remetente, email_destinatario, mensagem_erro.as_string())