from langchain_core.prompts import PromptTemplate
from langchain.chat_models import init_chat_model

import os
from dotenv import load_dotenv

load_dotenv()

ANSWER_IA_MODEL = os.getenv("ANSWER_IA_MODEL", "gemini-2.0-flash")
ANSWER_IA_PROVIDER = os.getenv("ANSWER_IA_PROVIDER", "google_genai")
ANSWER_IA_TEMPERATURE = float(os.getenv("ANSWER_IA_TEMPERATURE", 0.2))

modelo = init_chat_model(
    model=ANSWER_IA_MODEL,
    temperature=ANSWER_IA_TEMPERATURE,
    model_provider=ANSWER_IA_PROVIDER,
)

prompt_template = PromptTemplate(
    input_variables=["pergunta", "intencao", "dados"],
    template="""
Você é uma assistente virtual da empresa Lottus, criada para ajudar bibliotecárias
com dúvidas sobre a biblioteca escolar.

Regras:
1. Responda sempre em português, de forma educada, clara e direta.
2. Use exclusivamente os dados fornecidos abaixo.
3. Liste informações de forma organizada (por exemplo, nome do aluno, livro, data...).
4. Se os dados estiverem vazios, diga educadamente que não há informações.
5. Não invente respostas nem mencione temas fora da biblioteca.
6. Limite a resposta a 10 itens no máximo.
7. Se fizer sentido, indique as seções relevantes da plataforma:
   - [Empréstimos](http://localhost:5173/emprestimos)
   - [Catálogo](http://localhost:5173/catalogo)
   - [Turmas](http://localhost:5173/turmas)

Pergunta: {pergunta}

Dados disponíveis:
{dados}

Responda de forma natural, educada e informativa.
""",
)


def gerar_resposta(pergunta: str, intencao: str, dados: list) -> str:
    dados_str = (
        "\n".join([str(item) for item in dados[:10]])
        if dados
        else "Nenhum dado encontrado."
    )
    chain = prompt_template | modelo
    resposta = chain.invoke(
        {"pergunta": pergunta, "intencao": intencao, "dados": dados_str}
    )
    return resposta.content.strip()
