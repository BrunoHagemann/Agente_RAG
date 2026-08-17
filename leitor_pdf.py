import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

def preparar_documentos(caminho_pasta):
    print(f"1. Lendo os PDFs da pasta: '{caminho_pasta}'...")
    
    loader = PyPDFDirectoryLoader(caminho_pasta)
    documentos = loader.load()
    
    if not documentos:
        print("Nenhum PDF encontrado!")
        return []
        
    print(f"Sucesso! {len(documentos)} páginas carregadas no total.")


    # chunk_size: Quantidade de caracteres por pedaço
    # chunk_overlap: Quantidade de caracteres que se sobrepõem entre o pedaço atual e o próximo 
    print("2. Dividindo o texto em partes menores para a IA")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    
    chunks = text_splitter.split_documents(documentos)
    print(f"O texto foi dividido em {len(chunks)} pedaços (chunks).")
    
    return chunks

if __name__ == "__main__":
    # Nome da pasta onde PDFs devem estar
    pasta_pdfs = "meus_manuais"
    
    os.makedirs(pasta_pdfs, exist_ok=True)
    
    meus_chunks = preparar_documentos(pasta_pdfs)