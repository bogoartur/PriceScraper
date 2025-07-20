# 🚀 PriceScraper: Monitoramento de Preços Kabum com Telegram Bot

**PriceScraper** é uma solução automatizada para rastreamento de preços na [Kabum.com.br](https://www.kabum.com.br), integrada a um **bot do Telegram** para consultas e notificações em tempo real. Desenvolvido para demonstrar habilidades em **web scraping**, **persistência de dados** e **interação com APIs**, o PriceScraper é uma ferramenta eficiente para acompanhar o histórico e as flutuações de preços de produtos.

---

## 🌟 Funcionalidades Principais

- **Scraping de Preços**: Coleta dados de produtos e preços diretamente da Kabum.
- **Banco de Dados SQLite**: Armazenamento local eficiente com histórico de preços e o menor preço já registrado.
- **Bot do Telegram Integrado**: Interface amigável para consultas via comandos e buscas inline.
- **Atualização Inteligente**: Raspagem otimizada que busca novos preços apenas quando necessário.

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.x**
- [`requests`](https://pypi.org/project/requests/): Requisições HTTP
- [`beautifulsoup4`](https://pypi.org/project/beautifulsoup4/): Parseamento de HTML/JSON
- [`python-telegram-bot`](https://github.com/python-telegram-bot/python-telegram-bot): API para bots do Telegram
- **sqlite3**: Banco de dados leve e embutido no Python

---

## ⚙️ Configuração e Execução

### 1. Pré-requisitos

- Python 3.x instalado na máquina

### 2. Clonar o Repositório

```bash
git clone <URL_DO_SEU_REPOSITORIO>
cd PriceScraper  # Ou o nome da pasta clonada
```

### 3. Criar Ambiente Virtual e Instalar Dependências

```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
# ou venv\Scripts\activate  # Windows

pip install requests beautifulsoup4 python-telegram-bot
```

### 4. Configurar o Token do Bot do Telegram

Crie um arquivo chamado `token_telegram.txt` na raiz do projeto e insira o token do seu bot:

```
SEU_TOKEN_DO_TELEGRAM_AQUI
```

> ⚠️ Este arquivo está incluído no `.gitignore` e **não deve ser versionado**.

### 5. Inicializar o Banco de Dados

Execute o script para realizar o scraping inicial e popular o banco de dados (`produtos_kabum.db`):

```bash
python scraper.py
```

> ⏳ Esse processo pode levar alguns minutos, dependendo da quantidade de produtos.

### 6. Iniciar o Bot

Após a configuração inicial, inicie o bot:

```bash
python bot.py
```

---

## 🤖 Como Usar o Bot

- **Busca Inline**: Em qualquer chat do Telegram, digite `@SEU_USERNAME_DO_BOT` seguido do nome do produto.  
  _Exemplo_: `@ArturPM_bot monitor gamer`

- **Busca Direta (Chat Privado)**: Envie o nome de um produto diretamente para o bot.  
  O bot responderá com os produtos mais relevantes e seus preços.

---

> Projeto feito com 💻 por [Seu Nome].  
> Sinta-se à vontade para contribuir ou abrir issues!
