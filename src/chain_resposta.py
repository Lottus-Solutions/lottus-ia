from langchain_core.prompts import PromptTemplate
from langchain.chat_models import init_chat_model
from src.prompts import (
    gerar_prompt_conversa_geral,
    gerar_prompt_fora_do_contexto,
)

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

prompt = PromptTemplate(
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


prompt_conversa_geral = PromptTemplate(
    input_variables=["pergunta"],
    template="""
Você é uma assistente virtual simpática criada pela empresa Lottus, criada para interagir com os usuários de uma biblioteca escolar. 
Seu papel aqui é apenas conversar de forma educada e amigável com os usuários.

⚠️ Regras:
- Responda sempre em português.
- Seja simpática, educada e cordial.
- Se o usuário perguntar algo fora do escopo da biblioteca, não há problema – responda com educação, mas sem se aprofundar no assunto.

Usuário disse: "{pergunta}"

Responda com leveza e simpatia.
""",
)


prompt_fora_do_contexto = PromptTemplate(
    input_variables=["pergunta"],
    template="""
Você é uma assistente virtual da empresa Lottus, implementada exclusivamente para ajudar com dúvidas relacionadas a uma biblioteca escolar.

❌ O usuário fez uma pergunta fora do seu escopo de atuação.

Regras:
- Responda com educação, mas diga claramente que não pode ajudar com esse tipo de pergunta.
- Não tente inventar respostas ou mudar de assunto.
- Não responda perguntas sobre temas como receitas, esportes, política, tecnologia em geral ou assuntos pessoais.

Usuário perguntou: "{pergunta}"

Responda educadamente explicando que você só pode ajudar com assuntos da biblioteca escolar, sendo eles: Empréstimos, Catálogo, Turmas, Alunos.
""",
)


def gerar_resposta(pergunta: str, intencao: str, dados: list) -> str:
    if intencao == "fora_do_contexto":
        chain = prompt_fora_do_contexto | modelo
        resposta = chain.invoke(
            {"pergunta": pergunta}
        )
        return resposta.content.strip()

    elif intencao == "conversa_geral":
        chain = prompt_conversa_geral | modelo
        resposta = chain.invoke(
            {"pergunta": pergunta}
        )
        return resposta.content.strip()

    else:
        dados_str = (
        "\n".join([str(item) for item in dados[:10]])
        if dados
        else "Nenhum dado encontrado."
        )
        chain = prompt | modelo
        resposta = chain.invoke(
            {"pergunta": pergunta, "intencao": intencao, "dados": dados_str}
        )
        return resposta.content.strip()
