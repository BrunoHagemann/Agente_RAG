import os
import uuid

from flask import Flask, jsonify, render_template, request, session

from rag_service import AgenteMercado

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", os.urandom(24))

# Quantos pares pergunta/resposta ficam disponíveis como contexto de
# conversa para o modelo (evita mandar um histórico gigante a cada chamada).
MAX_TURNOS_CONTEXTO = 6

# Histórico de conversa por sessão, mantido em memória do processo.
# Simples e suficiente para uma ferramenta interna com um servidor único.
HISTORICOS = {}


def _get_session_id():
    if "session_id" not in session:
        session["session_id"] = str(uuid.uuid4())
    return session["session_id"]


print("Inicializando o agente do Mercado Central 24h (pode levar alguns segundos)...")
agente = AgenteMercado()
print("Agente pronto. Servidor web disponível.")


@app.route("/")
def index():
    _get_session_id()
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    dados = request.get_json(force=True, silent=True) or {}
    pergunta = (dados.get("mensagem") or "").strip()

    if not pergunta:
        return jsonify({"erro": "Envie uma pergunta antes de enviar."}), 400

    session_id = _get_session_id()
    historico = HISTORICOS.setdefault(session_id, [])

    try:
        resultado = agente.responder(
            pergunta, historico=historico[-(MAX_TURNOS_CONTEXTO * 2):]
        )
    except Exception as exc:  # noqa: BLE001 - queremos reportar qualquer falha ao usuário
        return jsonify({"erro": f"Não foi possível consultar o agente: {exc}"}), 500

    historico.append(("human", pergunta))
    historico.append(("ai", resultado["resposta"]))

    return jsonify(resultado)


@app.route("/api/novo-chat", methods=["POST"])
def novo_chat():
    session_id = _get_session_id()
    HISTORICOS.pop(session_id, None)
    return jsonify({"ok": True})


if __name__ == "__main__":
    # host="0.0.0.0" permite acessar de outros computadores na rede interna,
    # por exemplo http://IP-DO-SERVIDOR:5000
    app.run(host="0.0.0.0", port=5000, debug=False)
