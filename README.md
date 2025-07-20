🚀 PriceScraper: Monitoramento de Preços Kabum com Telegram Bot
Este projeto é uma solução automatizada para rastreamento de preços na Kabum.com.br, integrando um bot do Telegram para consultas e notificações em tempo real. Desenvolvido para demonstrar capacidades de web scraping, persistência de dados e interação com APIs de bot, o PriceScraper oferece uma ferramenta eficiente para acompanhar o histórico e as flutuações de preços de produtos.

🌟 Funcionalidades Principais
Scraping de Preços: Coleta dados de produtos e preços diretamente da Kabum.com.br.

Banco de Dados SQLite: Armazenamento local e eficiente de informações de produtos, incluindo preço atual e o menor preço já registrado.

Telegram Bot Integrado: Interface amigável para usuários consultarem preços de produtos via comandos e buscas inline.

Atualização Inteligente de Preços: Otimização nas chamadas de scraping, buscando novos preços na Kabum apenas quando os dados no banco de dados estão desatualizados.

🛠️ Tecnologias Utilizadas
Python 3.x: Linguagem de programação principal.

requests: Biblioteca para requisições HTTP.

BeautifulSoup4: Para parsear e extrair dados de HTML/JSON.

python-telegram-bot: Framework para desenvolvimento do bot.

sqlite3: Módulo nativo do Python para interação com banco de dados SQLite.

⚙️ Configuração e Execução
Para configurar e rodar o projeto em seu ambiente local, siga os passos abaixo:

1. Pré-requisitos
Certifique-se de ter o Python 3.x instalado em sua máquina.

2. Clonar o Repositório
Bash

git clone <URL_DO_SEU_REPOSITORIO>
cd PriceScraper # Ou o nome do seu diretório clonado
3. Instalar Dependências
É altamente recomendável utilizar um ambiente virtual:

Bash

python -m venv venv
source venv/bin/activate  # macOS/Linux
# ou venv\Scripts\activate no Windows
Instale as bibliotecas Python necessárias:

Bash

pip install requests beautifulsoup4 python-telegram-bot
4. Configurar o Token do Telegram Bot
Crie um arquivo chamado token_telegram.txt na raiz do projeto e insira o token do seu bot do Telegram neste arquivo.

Exemplo de token_telegram.txt:

SEU_TOKEN_DO_TELEGRAM_AQUI
Importante: Este arquivo já está no .gitignore e não deve ser versionado. Mantenha seu token seguro.

5. Inicializar o Banco de Dados
Execute o script scraper.py uma primeira vez para popular o banco de dados produtos_kabum.db com dados iniciais. Este processo pode levar alguns minutos, dependendo da quantidade de categorias a serem raspadas.

Bash

python scraper.py
6. Iniciar o Bot do Telegram
Após a configuração e inicialização do banco de dados, você pode iniciar o bot:

Bash

python bot.py
Seu bot estará online e pronto para interagir no Telegram.

🤖 Como Usar o Bot
Pesquisa Inline: Em qualquer chat do Telegram, digite @SEU_USERNAME_DO_BOT (substitua pelo username real do seu bot, ex: @ArturPM_bot) seguido do nome do produto para uma busca rápida e resultados diretos.

Pesquisa no Chat Privado: Envie o nome do produto diretamente para o bot no chat privado para receber uma lista dos produtos mais relevantes encontrados.
