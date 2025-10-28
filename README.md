# Lottus IA

`Lottus IA` é um assistente conversacional baseado em IA para bibliotecas escolares, capaz de:

* Classificar a intenção da pergunta do usuário.
* Consultar dados de um banco de dados quando necessário.
* Gerar respostas contextuais ou gerais, dependendo da intenção.
* Integrar-se com modelos de IA (como Gemini, OpenAI, Claude) via LangChain.

A aplicação é modular e configurável, permitindo alterar o modelo de IA e parâmetros diretamente pelo arquivo `.env`.

---

## 🔹 Funcionalidades

1. **Classificação de intenção**
   Identifica se a pergunta do usuário é:

   * Fora do contexto;
   * Conversa geral;
   * Consulta específica ao banco de dados.

2. **Consulta ao banco de dados**
   Para perguntas de consulta, a aplicação busca os dados necessários e gera a resposta apropriada.

3. **Geração de resposta com IA**
   Para perguntas fora do contexto ou conversas gerais, utiliza um modelo de IA para criar respostas inteligentes.

4. **Logs centralizados**
   Toda interação é registrada com `logger` para monitoramento e debugging.

---

## 🔹 Tecnologias

* **Python 3.10+**
* **LangChain** (`langchain.chat_models`, `langchain_core.prompts`)
* **dotenv** para variáveis de ambiente
* **Banco de dados** (via módulo `Banco` — MySQL ou similar)
* **Logging** personalizado via `logger`

---

## 🔹 Estrutura do projeto

```
project/
│
├── src/
│   ├── classificador.py           # Classifica a intenção da pergunta
│   ├── banco.py                   # Interface com o banco de dados
│   ├── chain_resposta.py          # Gera resposta final a partir dos dados
│   ├── prompts.py                 # Templates de prompts
│   └── logger.py                  # Configuração de logs
│
├── .env                           # Variáveis de ambiente
├── main.py                        # Ponto de entrada da aplicação
└── README.md
```

---

## 🔹 Configuração

1. Instale as dependências:

```bash
pip install -r requirements.txt
```

2. Configure o arquivo `.env` na raiz do projeto:

3. Inicie a aplicação com o comando 

```python
flask run
```

Fluxo de funcionamento:

1. Recebe a pergunta do usuário.
2. Classifica a intenção com `classificar_intencao`.
3. Se for conversa geral ou fora do contexto, gera resposta com prompt padrão.
4. Se for intenção de banco, consulta `Banco` e gera resposta com `gerar_resposta`.
5. Retorna a resposta final ao usuário.

---

## 🔹 Logs

Todas as interações são registradas usando o módulo `logger`:

```python
logger.info("Pergunta recebida: ...")
logger.info("Intenção classificada: ...")
logger.info("Dados retornados: ...")
```

---

## 🔹 Personalização

* Para adicionar novas intenções ou consultas ao banco, edite `classificador.py` e `banco.py`.
* Para criar novos templates de prompt, edite `prompts.py`.
* Para alterar o modelo de IA, configure no `.env`:

```
ANSWER_IA_MODEL=gemini-2.0-flash
ANSWER_IA_PROVIDER=google_genai
ANSWER_IA_TEMPERATURE=0.2
```




