from langchain_core.prompts import PromptTemplate

from langchain_core.prompts import PromptTemplate
from langchain.chat_models import init_chat_model

import os
from dotenv import load_dotenv

load_dotenv()

CLASSIFY_IA_MODEL = os.getenv("CLASSIFY_IA_MODEL", "gemini-2.0-flash")
CLASSIFY_IA_PROVIDER = os.getenv("CLASSIFY_IA_PROVIDER", "google_genai")
CLASSIFY_IA_TEMPERATURE = float(os.getenv("CLASSIFY_IA_TEMPERATURE", 0.2))

modelo = init_chat_model(
    model=CLASSIFY_IA_MODEL,
    temperature=CLASSIFY_IA_TEMPERATURE,
    model_provider=CLASSIFY_IA_PROVIDER,
)

prompt_template = PromptTemplate(
    input_variables=["pergunta"],
    template="""
Classifique a seguinte pergunta feita por uma bibliotecária em uma das intenções abaixo.
Se a pergunta não estiver relacionada ao contexto da biblioteca escolar, classifique como 'fora_do_contexto'.

Intenções possíveis:
- consultar_emprestimos_ativos
- consultar_emprestimos_atrasados
- consultar_emprestimos_devolucao_hoje
- consultar_emprestimos_devolucao_amanha
- livros_reservados
- livros_mais_lidos_por_turma
- livros_maior_demanda_semestre
- livros_totais
- alunos_sem_retirada_obrigatoria
- alunos_atrasos_frequentes
- alunos_em_atraso
- bonus_por_turma
- categorias_mais_emprestadas
- categorias_menos_procuradas
- livros_por_categoria
- categorias_aumento_emprestimos
- conversa_geral
- fora_do_contexto

Pergunta: {pergunta}

Responda apenas com a chave da intenção (ex: "consultar_emprestimos_ativos").
""",
)


def classificar_intencao(pergunta: str) -> str:
    chain = prompt_template | modelo
    resposta = chain.invoke({"pergunta": pergunta})
    return resposta.content.strip().lower()
