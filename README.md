# LlamaIndex AG POC

Este projeto é uma prova de conceito (PoC) de um bot de Discord com integração à LlamaIndex, que permite responder perguntas em **português do Brasil** com base em documentos locais. A IA assume o papel de **um professor universitário especializado em Algoritmos Genéticos**.

A IA é construída utilizando:
- **LlamaIndex** com armazenamento vetorial persistente em **ChromaDB**
- Embeddings do modelo **`intfloat/multilingual-e5-large`** via **HuggingFace**
- **Groq** como LLM para geração de respostas rápidas e precisas
- Um **bot no Discord** para interação com usuários

---

## 🧠 Funcionalidade principal

O usuário envia uma pergunta no Discord via comando `/pergunta`, e a IA responde com base nos documentos inseridos na pasta `files/`.

A IA possui um _prompt de sistema_ que instrui o modelo a responder de forma didática, acadêmica e em português, sempre com clareza e base no contexto fornecido para aprendizado de inteligência. Veja o exemplo abaixo:

<img src="https://github.com/user-attachments/assets/b1003c03-4030-4712-a4b2-804e1d88ca26" width="65%" alt="Exemplo de utilização">

---

## 📁 Estrutura do projeto

```

├── .env.example         # Exemplo de variáveis de ambiente
├── main.py              # Script principal com a lógica do bot e da IA
├── requirements.txt     # Dependências do projeto
├── README.md            # Você está aqui :)
├── files/               # Documentos que alimentam o LlamaIndex
│   └── .gitignore       # Ignora todos os arquivos exceto o próprio .gitignore
├── .gitignore           # Ignora ambientes, IDEs e arquivos de build

````

---

## 🚀 Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/llamaindex-ag-poc.git
cd llamaindex-ag-poc
````

### 2. Crie o ambiente virtual e instale as dependências

```bash
python -m venv .venv
source .venv/bin/activate       # Linux/macOS
.\.venv\Scripts\activate        # Windows

pip install -r requirements.txt
```

### 3. Configure o arquivo `.env`

Crie um arquivo `.env` na raiz com base no `.env.example`:

```bash
cp .env.example .env
```

Preencha as variáveis com suas credenciais reais:

```
HUGGING_API_KEY=...
GROQ_API_KEY=...
DISCORD_BOT_TOKEN=...
```

### 4. Adicione documentos à pasta `files/`

Coloque arquivos de texto ou PDF dentro da pasta `files/`, eles serão processados automaticamente na primeira execução para gerar os embeddings.

Esse processo pode demorar dependendo da quantidade de arquivos. No meu caso, com cerca de 745 nodes, o tempo médio de processamento foi de 40 minutos a 1 hora. Esse prazo pode variar conforme as especificações da sua máquina.

### 5. Execute o bot

```bash
python main.py
```

---

## 🤖 Como obter as credenciais

### 🔑 HuggingFace (HUGGING\_API\_KEY)

1. Acesse: [https://huggingface.co](https://huggingface.co)
2. Crie uma conta (ou faça login)
3. Vá em **Settings > Access Tokens**
4. Clique em **New token**, defina um nome e selecione permissão “**Read**”
5. Copie o token gerado e adicione ao `.env` como `HUGGING_API_KEY`

---

### ⚡ Groq (GROQ\_API\_KEY)

1. Acesse: [https://console.groq.com/](https://console.groq.com/)
2. Crie uma conta ou faça login
3. Vá em **API Keys**
4. Gere uma nova chave de API
5. Copie e cole no seu `.env` como `GROQ_API_KEY`

---

### 🎮 Discord (DISCORD\_BOT\_TOKEN)

1. Acesse o [Discord Developer Portal](https://discord.com/developers/applications)
2. Clique em **"New Application"**
3. Dê um nome e vá em **"Bot" > Add Bot**
4. Vá em **"Bot" > Token** e clique em **"Reset Token"**
5. Copie o token e adicione no `.env` como `DISCORD_BOT_TOKEN`
6. Vá em **"OAuth2" > URL Generator**

   * Selecione **scopes**: `bot` e `applications.commands`
   * Em **bot permissions**, marque `Send Messages` e `Use Slash Commands`
   * Gere o link e use-o para adicionar o bot ao seu servidor

---

## ✅ Comandos disponíveis no Discord

| Comando     | Descrição                                 |
| ----------- | ----------------------------------------- |
| `/pergunta` | Envie uma pergunta baseada nos documentos |

---

## 🧪 Exemplo de uso

**Comando:**

```
/pergunta ag: O que é crossover em algoritmos genéticos?
```

**Resposta:**

> O crossover é uma operação genética inspirada na reprodução biológica que combina partes de dois indivíduos para gerar um novo...

---

## 📌 Observações

* O índice é salvo em `chroma.db/` para persistência entre execuções.
* Novos arquivos adicionados a `files/` só serão indexados se o diretório estiver vazio ou for excluído manualmente.

---

## 🛠️ Tecnologias utilizadas

* Python
* LlamaIndex
* ChromaDB
* HuggingFace Transformers
* Groq
* Discord API (via discord.py)
* .env (via python-dotenv)

---

## 📄 Licença

Este projeto é apenas uma Prova de Conceito (PoC) para fins de estudo. Nenhuma parte deste projeto foi feita para uso comercial.
