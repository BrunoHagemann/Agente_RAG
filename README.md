#Assistente Virtual Corporativo com IA (RAG)

Este é um projeto de Inteligência Artificial desenvolvido com **Python**, **LangChain** e **OpenAI/Gemini** que funciona como um assistente corporativo baseado em documentos internos (RAG - Retrieval-Augmented Generation). O agente lê manuais em PDF e responde dúvidas dos funcionários com base exclusiva nas informações fornecidas.

---

## Tecnologias Utilizadas
* **Python 3.11+**
* **LangChain**
* **FAISS**
* **Google Gemini / OpenAI**

---

## Como Executar o Projeto

1. Clonar ou abrir o projeto e ativar o ambiente virtual
Abra a pasta do projeto no VS Code e ative o ambiente virtual no terminal:

```
.venv\Scripts\Activate
```

2. Configurar as Chaves de API
Crie um arquivo chamado .env na raiz do projeto e insira a sua chave da API (Gemini ou OpenAI):

```
GOOGLE_API_KEY=sua_chave_aqui

OPENAI_API_KEY=sua_chave_aqui
```

3. Adicionar os Manuais
Coloque os arquivos PDF que a IA deve aprender dentro da pasta meus_manuais/.

4. Gerar o Banco de Dados (Memória da IA)
Execute o script de criação do banco vetorial:

```
python criar_banco.py
```
5. Iniciar o Chat com o Agente
Com o banco gerado, inicie o assistente:

```
python agente_mercado.py
```

---

6 . Rodar o servidor

```
python chat_web/app.py
```

Acessar o chat

No seu próprio computador: 
```
http://localhost:5000`
```

---

## Exemplo Prático de Funcionamento (RAG)

o PDF de FAQ contenha essa regra de atendimento:

"Pergunta: Como faço para trocar um produto com defeito?"

"Resposta da IA: O cliente tem até 7 dias corridos após a compra para realizar a troca na recepção, apresentando o cupom fiscal e o produto na embalagem original."

---

## Status do Projeto
O projeto está atualmente implantado e rodando em uma instância da Oracle Cloud Infrastructure (OCI).

[![OCI](https://img.shields.io/badge/Hosted%20on-Oracle%20Cloud-F80000?style=for-the-badge&logo=oracle&logoColor=white)]()

## Infraestrutura
* **Serviço:** Compute Instance (Ubuntu)
* **Provedor:** OCI (Oracle Cloud Infrastructure)

* acesso em  http://0.0.0.0:8000
* http://163.176.107.149:8000/

<img width="1360" height="103" alt="image" src="https://github.com/user-attachments/assets/95166e05-6520-4c80-abca-2c930349dcb3" />

<img width="1361" height="710" alt="image" src="https://github.com/user-attachments/assets/f5426b62-fe93-40a7-bd62-0dd9a3a33545" />

<img width="1525" height="352" alt="image" src="https://github.com/user-attachments/assets/1b9e505b-b39a-44e1-89ec-a0a4c1e8f85e" />


