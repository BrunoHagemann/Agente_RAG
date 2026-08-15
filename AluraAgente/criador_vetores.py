import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()

def criar_banco_vetorial(chunks, nome_pasta_destino="banco_faiss"):
    print("3. Conectando ao Google Gemini para gerar os Embeddings")
    
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    
    print("4. Convertendo os textos em vetores e salvando no FAISS ")
    
    vector_store = FAISS.from_documents(chunks, embeddings)
    
    vector_store.save_local(nome_pasta_destino)
    
    print(f"Sucesso! Banco de dados vetorial salvo na pasta '{nome_pasta_destino}'.")
    return vector_store

if __name__ == "__main__":
    from leitor_pdf import preparar_documentos 
    
    pasta_pdfs = "meus_manuais"
    
    print("--- INICIANDO PROCESSAMENTO DOS MANUAIS DO MERCADO CENTRAL 24H ---")
    
    meus_chunks = preparar_documentos(pasta_pdfs)
    
    if meus_chunks:
        banco = criar_banco_vetorial(meus_chunks)