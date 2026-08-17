import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()

SYSTEM_PROMPT = (
    "Você é o assistente virtual corporativo do 'Mercado Central 24h', "
    "um supermercado moderno de operação contínua (24/7) focado em eficiência, "
    "delivery e no programa de fidelidade 'Cliente VIP Central'.\n\n"
    "Seu trabalho é responder perguntas dos funcionários baseando-se EXCLUSIVAMENTE "
    "nos documentos fornecidos no contexto abaixo.\n\n"
    "Regras estritas:\n"
    "1. Se a resposta não estiver no contexto, responda: 'Desculpe, não encontrei essa "
    "informação nos manuais do Mercado Central 24h.' Não invente informações ou datas.\n"
    "2. Seja claro, educado e direto.\n"
    "3. Sempre que relevante, cite a política ou o manual correspondente.\n\n"
    "Contexto encontrado nos documentos:\n"
    "{context}"
)


class AgenteMercado:
    """Encapsula o agente RAG do Mercado Central 24h para uso via API web.

    Mantém o banco vetorial e o modelo carregados em memória (carregados uma
    única vez, na inicialização do servidor) e expõe um método `responder`
    que devolve a resposta em texto junto com as fontes usadas, para que a
    interface web possa exibi-las ao usuário.
    """

    def __init__(self, nome_pasta_banco: str = "banco_faiss", k: int = 4):
        print("Carregando embeddings e banco vetorial...")
        self.embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

        self.banco_vetorial = FAISS.load_local(
            nome_pasta_banco,
            self.embeddings,
            allow_dangerous_deserialization=True,
        )
        self.retriever = self.banco_vetorial.as_retriever(search_kwargs={"k": k})

        print("Conectando ao modelo Gemini...")
        self.llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash", temperature=0)

    def _formatar_fontes(self, documentos):
        fontes = []
        for doc in documentos:
            caminho = doc.metadata.get("source", "desconhecido")
            pagina = doc.metadata.get("page", None)
            trecho = doc.page_content.strip().replace("\n", " ")
            if len(trecho) > 220:
                trecho = trecho[:220].rstrip() + "..."
            fontes.append(
                {
                    "arquivo": os.path.basename(str(caminho)),
                    # PyPDFDirectoryLoader é 0-indexado; exibimos a página "humana"
                    "pagina": (pagina + 1) if isinstance(pagina, int) else None,
                    "trecho": trecho,
                }
            )
        return fontes

    def responder(self, pergunta: str, historico=None):
        """Responde a `pergunta` usando o contexto recuperado do FAISS.

        `historico` é uma lista opcional de tuplas (role, conteudo), onde
        role é "human" ou "ai", representando as últimas trocas da conversa
        (usada para o modelo entender perguntas de acompanhamento como
        "e no caso de troca sem cupom?").
        """
        documentos = self.retriever.invoke(pergunta)
        contexto = "\n\n".join(doc.page_content for doc in documentos)

        mensagens = [("system", SYSTEM_PROMPT.format(context=contexto))]
        if historico:
            mensagens.extend(historico)
        mensagens.append(("human", pergunta))

        resposta = self.llm.invoke(mensagens)

        return {
            "resposta": resposta.content,
            "fontes": self._formatar_fontes(documentos),
        }
