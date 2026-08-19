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

## Exemplo Prático de Funcionamento (RAG)

o PDF de FAQ contenha essa regra de atendimento:

"Pergunta: Como faço para trocar um produto com defeito?"

"Resposta da IA: Para casos que exigem reembolso ou resolução por falha de produto, a decisão depende primeiramente do Manual de Garantia de Produtos da BimBam Buy. Caso a garantia não se aplique, o caso pode seguir sob a política de devoluções, desde que exista elegibilidade por outra via."

---

## Status do Projeto
O projeto está atualmente implantado e rodando em uma instância da Oracle Cloud Infrastructure (OCI).

## Infraestrutura
* **Serviço:** Compute Instance (Ubuntu)
* **Provedor:** OCI (Oracle Cloud Infrastructure)

  Local URL: http://localhost:8501
  Network URL: http://10.0.0.236:8501
  External URL: http://163.176.107.149:8501
---

<img width="1765" height="923" alt="image" src="https://github.com/user-attachments/assets/da9e6017-dc81-46fa-ab06-e1e998849d4f" />





