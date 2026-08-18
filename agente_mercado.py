import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda

load_dotenv()

def iniciar_agente(nome_pasta_banco="banco_faiss"):
    print("1. Ligando o agente e carregando a memória dos PDFs...")

    
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    
    try:
        banco_vetorial = FAISS.load_local(
            nome_pasta_banco, 
            embeddings, 
            allow_dangerous_deserialization=True
        )
    except Exception as e:
        print(f"Erro ao carregar o banco de dados: {e}")
        print("Certifique-se de ter rodado a Fase 2 para criar a pasta 'banco_faiss'.")
        return None

    retriever = banco_vetorial.as_retriever(search_kwargs={"k": 4})

    print("2. Conectando ao cérebro do Google Gemini...")
   
    llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash", temperature=0)

    system_prompt = (
        """"Você é um assistente virtual corporativo especialista nos documentos da empresa.

        Sua tarefa é responder à pergunta do colaborador usando EXCLUSIVAMENTE as informações fornecidas no CONTEXTO abaixo.

        REGRAS OBRIGATÓRIAS:
        1. Responda apenas com fatos extraídos diretamente do contexto. Não invente ou presuma informações externas.
        2. Se o contexto não contiver a resposta exata, diga expressamente: "Não encontrei essa informação nos documentos disponíveis."
        3. Sempre cite a fonte (nome do arquivo e número da página) ao final ou ao longo da sua explicação."""
        "Contexto encontrado nos documentos:\n"
        "{context}"
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
    ])

    def responder(inputs):
        pergunta = inputs["input"]
        documentos = retriever.invoke(pergunta)
        contexto = "\n\n".join(doc.page_content for doc in documentos)

        resposta = llm.invoke([
            ("system", system_prompt.format(context=contexto)),
            ("human", pergunta),
        ])

        return {"answer": resposta.content}

    rag_chain = RunnableLambda(responder)

    return rag_chain

if __name__ == "__main__":
    agente = iniciar_agente()
    
    if agente:
        print("\n=================================")
        print("Digite 'sair' para encerrar.\n")
        
        while True:
            pergunta = input("Faça uma pergunta sobre os manuais: ")
            
            if pergunta.lower() in ['sair', 'exit', 'quit']:
                print("Encerrando o sistema...")
                break
                
            if pergunta.strip() == "":
                continue
                
            print("\nBuscando nos documentos e raciocinando...")
            
            # Invoca a chain com a pergunta do usuário
            resposta = agente.invoke({"input": pergunta})
            
            print(f"\nAgente: {resposta['answer']}")
            print("-" * 50)