from src.classificador import classificar_intencao
from src.banco import Banco
from src.chain_resposta import gerar_resposta
from src.prompts import (
    gerar_prompt_conversa_geral,
    gerar_prompt_fora_do_contexto,
)
from src.logger import logger


class AssistenteIA:
    def __init__(self):
        self.banco = Banco()

    def responder(self, pergunta: str) -> str:
        logger.info(f"Pergunta recebida: {pergunta}")

        intencao = classificar_intencao(pergunta)
        logger.info(f"Intenção classificada: {intencao}")

        if intencao == "fora_do_contexto":
            return gerar_prompt_fora_do_contexto(pergunta)

        elif intencao == "conversa_geral":
            return gerar_prompt_conversa_geral(pergunta)

        else:
            dados = self.banco.executar_intencao(intencao)
            logger.info(f"Dados retornados: {len(dados)} registros")

            if not dados:
                return "Não encontrei dados suficientes para responder à sua pergunta."

            return gerar_resposta(pergunta, intencao, dados)
