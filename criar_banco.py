import os
import time
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()

pasta_pdfs = "meus_manuais"
pasta_banco = "banco_faiss"

os.makedirs(pasta_pdfs, exist_ok=True)

print(f"1. Lendo os PDFs da pasta '{pasta_pdfs}'...")
loader = PyPDFDirectoryLoader(pasta_pdfs)
documentos = loader.load()

if not documentos:
    print(f"\n[AVISO] Nenhum PDF encontrado na pasta '{pasta_pdfs}'!")
    exit()

print(f"-> Sucesso! {len(documentos)} páginas carregadas.")

print("\n2. Dividindo o texto em pedaços...")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150)
chunks = text_splitter.split_documents(documentos)
print(f"-> Texto dividido em {len(chunks)} blocos.")

print("\n3. Conectando ao Gemini e enviando em lotes seguros...")
embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

# Lotes de 15 blocos para garantir que fique bem abaixo do limite gratuito
tamanho_lote = 15
banco_vetorial = None

total_lotes = (len(chunks) + tamanho_lote - 1) // tamanho_lote

for i in range(0, len(chunks), tamanho_lote):
    lote = chunks[i:i + tamanho_lote]
    num_lote = (i // tamanho_lote) + 1
    print(f"Processando lote {num_lote} de {total_lotes}...")
    
    if banco_vetorial is None:
        banco_vetorial = FAISS.from_documents(lote, embeddings)
    else:
        banco_vetorial.add_documents(lote)
    
    # Pausa de 20 segundos entre os lotes para respeitar a cota do plano gratuito
    if i + tamanho_lote < len(chunks):
        print("Pausando 20 segundos para liberar a cota da API...")
        time.sleep(20)

print("\n4. Salvando a 'memória' no seu computador...")
banco_vetorial.save_local(pasta_banco)

print(f"\n SUCESSO! Banco de dados criado na pasta '{pasta_banco}'.")