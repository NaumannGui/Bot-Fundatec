# 🤖 Bot de Monitoramento Fundatec (Web Scraping)

**Propósito:** Ficar por dentro de novas publicações de um concurso e sair na frente dos demais candidatos. Este bot foi desenvolvido para buscar automaticamente qualquer nova publicação na página da banca e enviar uma notificação por e-mail, disponibilizando o título e o link direto de acesso ao conteúdo.

## ✨ Funcionalidades (Features)

*   ⏱️ **Monitoramento Contínuo:** O bot roda de forma 100% autônoma na nuvem através do GitHub Actions, checando o site da banca duas vezes ao dia.
*   🛡️ **Bypass de Segurança Avançado:** Utiliza a inteligência do ScraperAPI com IPs residenciais brasileiros para passar despercebido pelos sistemas de bloqueio da Amazon (AWS WAF).
*   📧 **Alertas Inteligentes por E-mail:** Compara a última publicação com a memória interna e envia um e-mail com o link direto apenas quando encontra uma novidade real.
*   🚨 **Resiliência e Relatórios:** Possui tratamento de erros completo. Se o site da Fundatec cair, o bot envia um "e-mail de socorro" e registra tudo em um diário de bordo (Logging) profissional.

## 🛠️ Tecnologias Utilizadas

*   **Python:** Linguagem principal do script.
*   **Bibliotecas de Scraping:** `requests` para fazer as requisições web e `BeautifulSoup` (bs4) para varrer e extrair os dados do HTML.
*   **Bibliotecas Nativas:** `smtplib` e `email.mime` para estruturar e disparar as notificações, além de `logging` para o registro de atividades.
*   **GitHub Actions:** Plataforma de automação na nuvem usada para agendar o robô (`cron`) e rodar o código de forma gratuita e invisível.
*   **ScraperAPI:** Serviço de proxy residencial utilizado para contornar o AWS WAF (Firewall) e acessar o site com um IP brasileiro limpo.

## ⚙️ Como Funciona

**A Automação na Nuvem (GitHub Actions):**
O projeto fica hospedado no GitHub, onde configuramos um *workflow* (`main.yml`) que executa automaticamente 2x ao dia. O servidor do GitHub cria uma máquina virtual Linux temporária, instala o Python e as bibliotecas necessárias, e baixa o código do repositório. Após rodar o script principal, se houver atualizações na "memória" do robô, ele faz um *push* automático de volta para o repositório salvando o novo arquivo e, em seguida, a máquina virtual é limpa e desligada.

**A Lógica do Robô (bot.py):**
O script importa as bibliotecas e acessa as variáveis de ambiente sensíveis (senhas e chaves) armazenadas de forma segura no *Secrets* do GitHub. Para acessar a página da Fundatec sem ser bloqueado, o bot monta uma URL utilizando o ScraperAPI com o parâmetro "premium", o que garante o uso de IPs residenciais brasileiros, burlando o WAF (Firewall) da AWS.

**Extração e Notificação:**
Uma vez com o HTML em mãos, o bot busca a tag e a classe específicas (`eventos`) e extrai o título e o link da publicação **mais recente**. Ele então compara esse título com o que está salvo em seu bloco de notas interno (`ultimo_titulo.txt`). 
*   **Se houver novidade:** Ele aciona o servidor SMTP do Gmail, envia um alerta completo para o usuário e atualiza o bloco de notas.
*   **Se algo der errado:** O código inteiro está protegido por um sistema de tratamento de erros. Se o site cair ou a estrutura mudar, o bot envia um "e-mail de socorro" com os detalhes técnicos da falha e registra o evento em seu diário de bordo (Logging).