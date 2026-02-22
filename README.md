# Sistema de Ingestão e Busca RAG (Retrieval-Augmented Generation)

Este projeto implementa uma solução de RAG para busca semântica e chat sobre documentos PDF, utilizando **PostgreSQL** com a extensão **pgvector** como banco de dados vetorial, e **LangChain** para a orquestração da IA.

## 🚀 Como Executar a Solução

Siga os passos abaixo para configurar e rodar o projeto em sua máquina.

### 1. Pré-requisitos

*   **Docker** e **Docker Compose** instalados.
*   **Python 3.10+** instalado.
*   Uma chave de API do **Google Gemini** (ou OpenAI, se preferir).

### 2. Configuração do Ambiente

1.  Crie um arquivo `.env` na raiz do projeto baseado no `.env.example`:
    ```bash
    cp .env.example .env
    ```
2.  Abra o arquivo `.env` e preencha as variáveis necessárias:
    *   `GOOGLE_API_KEY`: Sua chave do Google Cloud.
    *   `DATABASE_URL`: A URL de conexão com o banco (padrão: `postgresql+psycopg://postgres:postgres@localhost:5432/rag`).
    *   `PDF_PATH`: O caminho absoluto para o arquivo PDF que deseja ingerir.
    *   `MODEL_PROVIDER`: Define qual provedor usar (`gemini` ou `openai`).

### 3. Multi-Provedor (Factory Pattern)

```markdown
O projeto utiliza o **Pattern Factory** em `src/utils.py` para permitir a troca fácil de provedores de IA. A escolha do provedor é definida por um parâmetro com valor padrão no código. Para alternar entre Google Gemini e OpenAI, basta alterar o valor desse parâmetro conforme necessário.

*   **Gemini**: Requer `GOOGLE_API_KEY` e usa o modelo `text-embedding-004`.
*   **OpenAI**: Requer `OPENAI_API_KEY` e usa o modelo `text-embedding-3-small`.
```

> **Nota:** Se você trocar o provedor após já ter feito uma ingestão, será necessário limpar o banco de dados (passo 3 com `docker compose down -v`), pois as dimensões dos vetores de embedding variam entre os provedores.

### 4. Subir o Banco de Dados

Utilize o Docker Compose para subir o PostgreSQL com pgvector:

```bash
docker-compose up -d
```
*Isso iniciará o banco de dados e habilitará automaticamente a extensão `vector`.*

### 5. Instalar Dependências

Recomenda-se o uso de um ambiente virtual:

```bash
python -m venv venv
source venv/bin/activate  # No Linux/macOS
# ou
.\venv\Scripts\activate  # No Windows

pip install -r requirements.txt
```

### 6. Ingestão de Dados

Para processar o PDF definido no `.env` e salvar os vetores no banco de dados, execute:

```bash
python src/ingest.py
```

### 7. Executar o Chat

Após a ingestão, você pode interagir com o documento através do terminal:

```bash
python src/chat.py
```

Para encerrar o chat, basta digitar **`sair`**, **`exit`** ou **`quit`** a qualquer momento.

## 📂 Estrutura do Projeto

*   `src/ingest.py`: Script responsável por carregar o PDF, dividir em pedaços (chunks) e armazenar os embeddings no PostgreSQL.
*   `src/search.py`: Contém a lógica de busca por similaridade e construção do prompt com contexto.
*   `src/chat.py`: Interface de linha de comando para interação com o usuário.
*   `src/utils.py`: Fábricas para inicialização dos modelos de LLM e Embeddings.
*   `docker-compose.yml`: Configuração da infraestrutura do banco de dados.

## 🛠️ Tecnologias Utilizadas

*   **LangChain**: Framework para desenvolvimento de aplicações baseadas em LLMs.
*   **PostgreSQL + pgvector**: Banco de dados relacional com suporte a busca vetorial.
*   **Google Gemini API**: Modelos de linguagem e embeddings (configurado por padrão).
*   **PyPDF**: Para extração de texto de arquivos PDF.

---
*Este projeto faz parte do desafio técnico para o MBA em Engenharia de Software com IA - Full Cycle.*