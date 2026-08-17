# Imagem do Assistente do Mercado Central 24h (chat web + RAG)
FROM python:3.11-slim

# Dependências de sistema mínimas (algumas libs Python compilam nativamente
# em certas arquiteturas, ex. ARM/Ampere da OCI Always Free).
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Instala dependências primeiro (aproveita cache do Docker em rebuilds)
COPY requirements.txt requirements.txt
COPY chat_web/requirements_web.txt chat_web/requirements_web.txt
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir -r chat_web/requirements_web.txt

# Copia o código do projeto (RAG + chat web).
# banco_faiss/, meus_manuais/ e .env ficam FORA da imagem (ver .dockerignore)
# e são fornecidos em tempo de execução via volume/env_file — assim dá para
# atualizar o banco vetorial sem rebuildar a imagem.
COPY agente_mercado.py criador_vetores.py criar_banco.py leitor_pdf.py ./
COPY chat_web/ chat_web/

EXPOSE 8000

# Roda a partir de dentro de chat_web/ para que "from rag_service import ..."
# funcione sem ajustes extras (o Gunicorn adiciona o cwd ao sys.path).
CMD ["sh", "-c", "cd chat_web && exec gunicorn --bind 0.0.0.0:8000 --workers 2 --timeout 120 app:app"]
