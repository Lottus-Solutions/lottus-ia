from flask import Flask, request, jsonify
from flask_cors import CORS
from src.assistente import AssistenteIA
from src.logger import logger

# Inicializa o app Flask
app = Flask(__name__)
CORS(app)

# Inicializa o assistente
assistente = AssistenteIA()


@app.route("/ia/perguntar", methods=["POST"])
def perguntar():
    """Endpoint principal para perguntas ao assistente."""
    try:
        body = request.get_json()
        pergunta = body.get("pergunta")

        if not pergunta:
            logger.warning("⚠️ Requisição sem campo 'pergunta'.")
            return jsonify({"erro": "Campo 'pergunta' é obrigatório."}), 400

        logger.info(f"🧠 Pergunta recebida: {pergunta}")
        resposta = assistente.responder(pergunta)
        logger.info(f"💬 Resposta gerada com sucesso.")

        return jsonify({"resposta": resposta})

    except Exception as e:
        logger.exception(f"❌ Erro ao processar pergunta: {e}")
        return jsonify({"erro": "Erro interno ao processar a pergunta."}), 500


@app.route("/ia", methods=["GET"])
def health_check():
    """Rota simples de status."""
    return jsonify({"status": "ok", "mensagem": "Assistente IA rodando 🚀"}), 200


if __name__ == "__main__":
    logger.info("🚀 Iniciando servidor Flask...")
    app.run(host="0.0.0.0", port=5000, debug=True)
