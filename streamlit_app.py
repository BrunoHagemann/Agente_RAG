import os
import re
import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()

SYSTEM_PROMPT = (
    """"Você é um assistente virtual corporativo especialista nos documentos da empresa.

    Sua tarefa é responder à pergunta do colaborador usando EXCLUSIVAMENTE as informações fornecidas no CONTEXTO abaixo.

    REGRAS OBRIGATÓRIAS:
    1. Responda apenas com fatos extraídos diretamente do contexto. Não invente ou presuma informações externas.
    2. Se o contexto não contiver a resposta exata, diga expressamente: "Não encontrei essa informação nos documentos disponíveis."
    3. Sempre cite a fonte (nome do arquivo e número da página) ao final ou ao longo da sua explicação."""
    "Contexto encontrado nos documentos:\n"
    "{context}"
)

st.set_page_config(page_title="Assistente", page_icon="🛒")


@st.cache_resource(show_spinner="Carregando o banco de manuais e conectando ao Gemini...")
def carregar_agente():
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    banco = FAISS.load_local(
        "banco_faiss", embeddings, allow_dangerous_deserialization=True
    )
    retriever = banco.as_retriever(search_kwargs={"k": 4})
    llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash", temperature=0)
    return retriever, llm


def formatar_fontes(documentos):
    fontes = []
    for doc in documentos:
        caminho = doc.metadata.get("source", "desconhecido")
        pagina = doc.metadata.get("page")
        trecho = doc.page_content.strip().replace("\n", " ")
        if len(trecho) > 220:
            trecho = trecho[:220].rstrip() + "..."
        fontes.append(
            {
                "arquivo": os.path.basename(str(caminho)),
                "pagina": (pagina + 1) if isinstance(pagina, int) else "?",
                "trecho": trecho,
            }
        )
    return fontes


def limpar_resposta_llm(conteudo):
    """Extrai e limpa o texto do LLM para evitar vazamento de metadados e erros de Markdown."""
    # Se o conteúdo vier como lista de partes (comum em respostas com múltiplos blocos no LangChain/Gemini)
    if isinstance(conteudo, list):
        texto = "".join([str(p.get("text", p)) if isinstance(p, dict) else str(p) for p in conteudo])
    else:
        texto = str(conteudo)

    # 1. Remove dicionários/assinaturas de metadados internos que vazam no texto
    texto = re.sub(r"\{'signature':.*?\}" , "", texto)

    # 2. Garante que quebras de linha com marcadores ganhem o espaçamento duplo exigido pelo Markdown
    texto = texto.replace("\n*", "\n\n* ").replace("\n-", "\n\n- ")

    return texto.strip()


retriever, llm = carregar_agente()

st.title("BimBam Buy Responde")
st.caption("Assistente interno")

with st.sidebar:
    st.markdown("**Sobre**\n\nResponde com base nos manuais em `meus_manuais/`, indexados em `banco_faiss/`.")
    if st.button("Novo chat"):
        st.session_state.mensagens = []
        st.session_state.historico = []
        st.rerun()

if "mensagens" not in st.session_state:
    st.session_state.mensagens = []  # para exibição: [{role, content, fontes}]
if "historico" not in st.session_state:
    st.session_state.historico = []  # para o modelo: [(role, content)]

# Reexibe o histórico da conversa
for msg in st.session_state.mensagens:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("fontes"):
            with st.expander("📎 Fontes consultadas"):
                for f in msg["fontes"]:
                    st.markdown(f"**{f['arquivo']}** — página {f['pagina']}")
                    st.caption(f["trecho"])

pergunta = st.chat_input("Digite sua pergunta sobre os manuais...")

if pergunta:
    st.session_state.mensagens.append({"role": "user", "content": pergunta})
    with st.chat_message("user"):
        st.markdown(pergunta)

    with st.chat_message("assistant"):
        with st.spinner("Consultando os manuais..."):
            documentos = retriever.invoke(pergunta)
            contexto = "\n\n".join(doc.page_content for doc in documentos)

            mensagens_llm = [("system", SYSTEM_PROMPT.format(context=contexto))]
            mensagens_llm.extend(st.session_state.historico[-12:])  # últimos ~6 turnos
            mensagens_llm.append(("human", pergunta))

            resposta = llm.invoke(mensagens_llm)
            
            # Aplica o tratamento no texto retornado
            resposta_limpa = limpar_resposta_llm(resposta.content)
            fontes = formatar_fontes(documentos)

        st.markdown(resposta_limpa)
        if fontes:
            with st.expander("📎 Fontes consultadas"):
                for f in fontes:
                    st.markdown(f"**{f['arquivo']}** — página {f['pagina']}")
                    st.caption(f["trecho"])

    # Salva no histórico a resposta tratada e limpa
    st.session_state.historico.append(("human", pergunta))
    st.session_state.historico.append(("ai", resposta_limpa))
    st.session_state.mensagens.append(
        {"role": "assistant", "content": resposta_limpa, "fontes": fontes}
    )
    