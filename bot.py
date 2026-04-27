import requests, os, smtplib
from bs4 import BeautifulSoup
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

url = "https://www.fundatec.org.br/portal/concursos/publicacoes_v2.php?concurso=986"
cabecalhos = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}
resposta = requests.get(url, headers=cabecalhos)
print(f"Status da resposta: {resposta.status_code}")
sopa_html = BeautifulSoup(resposta.text, 'html.parser')

publicacoes = sopa_html.find_all('a', class_='eventos')
primeira_pub = publicacoes[0]

titulo = primeira_pub.text
link = primeira_pub['href'.split("'")[1]  # Extrai o link corretamente

nome_do_arquivo = 'ultimo_titulo.txt'
email_remetente = 'gui.naumann@gmail.com'
email_destinatario = 'gui.naumann@gmail.com'
senha_app = os.getenv('SENHA_APP')  # Certifique-se de definir a variável de ambiente 'SENHA_APP' com a senha do aplicativo do Gmail

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
else:
    print("Nada novo hoje.")