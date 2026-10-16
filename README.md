# 🧠 GA4 Churn Predictor

> Sistema preditivo end-to-end para antecipação de churn em e-commerce utilizando dados brutos de eventos do **Google Analytics 4 (BigQuery)**, **Scikit-Learn**, **FastAPI** e interface analítica em **Streamlit**.

---

## 📌 Visão Geral do Projeto

Em e-commerce, o custo de aquisição de clientes (CAC) é frequentemente muito superior ao custo de retenção. O objetivo deste projeto é prever se usuários que compraram nos meses de novembro e dezembro de 2020 irão entrar em **churn** (abandono total da loja, sem nenhuma visita ou interação) durante o mês de janeiro de 2021.

O projeto foi construído em arquitetura modular (**Monorepo**), cobrindo todo o ciclo de vida do Machine Learning:
1. **Extração e Modelagem SQL:** Extração de eventos não estruturados do dataset público `bigquery-public-data.ga4_obfuscated_sample_ecommerce`.
2. **Engenharia de Atributos & Pipeline:** Enriquecimento temporal de interações por quinzenas e transformadores customizados integrados ao Scikit-Learn.
3. **Modelagem Supervisionada:** Treinamento, seleção de atributos com Informação Mútua e tuning de hiperparâmetros com `GridSearchCV`.
4. **Backend em API REST (FastAPI):** Microsserviço assíncrono para inferência unitária, em lote (JSON) e em streaming de arquivos CSV, com autenticação via `API-Key`.
5. **Frontend Interativo (Streamlit):** Dashboard multipágina para simulação de predições em tempo real e processamento em lote.

---

## 🏗️ Arquitetura da Solução

```mermaid
flowchart TD
    subgraph BigQuery ["Google Cloud BigQuery"]
        GA4[(GA4 Public E-commerce Data)]
        SQL[Query SQL com UNNEST de Eventos]
        GA4 --> SQL
    end

    subgraph PipelineML ["Pipeline de Machine Learning (Scikit-Learn)"]
        RAW[Raw Parquet Data]
        SQL --> RAW
        FT[Feature Transformer: Tendência Temporal & RFM]
        IM[SimpleImputer: Mediana]
        FS[SelectKBest: Mutual Information]
        HGB[HistGradientBoostingClassifier]
        
        RAW --> FT --> IM --> FS --> HGB
        HGB --> MODEL[(Modelo Treinado: churn_model.joblib)]
    end

    subgraph Backend ["API REST (FastAPI + Uvicorn)"]
        AUTH[Autenticação: X-API-Key]
        EP1["GET /health"]
        EP2["GET /data-sample/input"]
        EP3["POST /predict/single"]
        EP4["POST /predict/batch"]
        EP5["POST /predict/csv"]
        
        MODEL -.-> Backend
    end

    subgraph Frontend ["Interface Web (Streamlit)"]
        UI_HOME[Página Inicial: Contexto & Métricas]
        UI_SINGLE[Predição Unitária Interativa]
        UI_CSV[Predição em Lote via Upload CSV]
    end

    UI_SINGLE --> AUTH --> EP3
    UI_CSV --> AUTH --> EP5
    UI_HOME --> AUTH --> EP1 & EP2
```

---

## 📊 Estrutura do Repositório

```text
project_ga4_churn/
├── sql/
│   └── ga4_event_query.sql         # Extração dos eventos agregados no BigQuery
├── dataset/
│   ├── raw/                        # Base bruta exportada do BigQuery (Parquet)
│   └── processed/                  # Conjuntos de treino/teste e predições em CSV
├── models/
│   └── churn_model.joblib          # Pipeline completo treinado serializado
├── notebooks/
│   ├── eda_01.ipynb                # Análise exploratória de dados inicial
│   └── aprendendo_streamlit.ipynb  # Prototipação e testes de componentes
├── src/
│   ├── ga4_churn_predictor/        # Core de Machine Learning
│   │   ├── config.py               # Constantes, paths e definições de features
│   │   ├── data.py                 # Download do BigQuery e split treino/teste
│   │   ├── pipeline.py             # Feature engineering e pipeline Scikit-Learn
│   │   ├── train.py                # Treinamento com GridSearchCV e seleção de features
│   │   ├── evaluate.py             # Métricas de validação (ROC-AUC, F1, Recall)
│   │   └── predict.py              # Camada de inferência reutilizável
│   ├── app/                        # API REST com FastAPI
│   │   ├── config.py               # Configurações Pydantic via .env
│   │   ├── security.py             # Validação de API Key no cabeçalho
│   │   ├── main.py                 # Instância FastAPI, middlewares e exception handlers
│   │   ├── schemas/                # Schemas Pydantic de entrada e saída
│   │   ├── routers/                # Rotas: health, data e predict (single, batch, csv)
│   │   ├── services/               # Lógica de negócio (MLService e DataService)
│   │   └── dependencies/           # Injeção de dependências e validação de arquivos
│   └── ui/                         # Interface de Usuário com Streamlit
│       ├── app.py                  # Ponto de entrada com st.navigation
│       ├── config.py               # Conexão com o backend via .env.streamlit
│       ├── api_client.py           # Cliente HTTP com requests autenticado
│       └── pages/                  # Telas: Home, Predição Unitária e Lote
├── pyproject.toml                  # Configuração de projeto e dependências com uv
└── README.md                       # Documentação do projeto
```

---

## ⚙️ Engenharia de Features e Modelagem

### Destaque de Feature: `tendencia_interacoes`
Como o churn em e-commerce se manifesta pelo desengajamento gradual, as interações de navegação do usuário em novembro e dezembro foram agregadas em **4 quinzenas consecutivas**. Uma transformação customizada calcula o vetor de inclinação de engajamento do cliente:

$$\text{tendencia\_interacoes} = \frac{-3 \cdot Q_1 - 1 \cdot Q_2 + 1 \cdot Q_3 + 3 \cdot Q_4}{10}$$

* Usuários com engajamento recente em alta recebem pontuações fortemente positivas.
* Usuários que compraram no início e sumiram recebem valores negativos.
* Essa feature isolada foi selecionada pelo `SelectKBest` como o **maior preditor de retenção/churn** do modelo.

### Tratamento do Desbalanceamento
A base possui **~89% de taxa de churn** e apenas **~11% de retenção**. Para evitar o "paradoxo da acurácia" (onde o modelo simplesmente chuta a classe majoritária):
* O classificador utiliza ponderação de perda inversamente proporcional à frequência das classes (`class_weight="balanced"`).
* Otimização focada em **ROC-AUC** e **Recall da classe minoritária**, permitindo calibrar o limiar de decisão de negócio.

---

## 🚀 Como Executar o Projeto Localmente

### Pré-requisitos
* **Python 3.14+**
* Gerenciador de pacotes [`uv`](https://github.com/astral-sh/uv) (recomendado) ou `pip`

### 1. Clonar o repositório e instalar dependências
```bash
git clone https://github.com/jafmatos/ga4_churn_predictor.git
cd ga4_churn_predictor

# Cria o ambiente virtual e instala todas as dependências automaticamente
uv sync
```

### 2. Configurar as Variáveis de Ambiente
O projeto utiliza dois arquivos de configuração baseados em templates:

**Para o Backend (FastAPI):**
```bash
cp .env.example .env
```
Edite o arquivo `.env`:
```env
API_TITLE="GA4 Churn Predictor API"
API_VERSION="1.0.0"
API_DESCRIPTION="API preditiva de churn para e-commerce GA4"
API_SECRET_KEY="sua_chave_secreta_aqui"
```

**Para o Frontend (Streamlit):**
```bash
cp .env.streamlit.example .env.streamlit
```
Edite o arquivo `.env.streamlit`:
```env
API_BASE_URL="http://localhost:8000"
API_SECRET_KEY="sua_chave_secreta_aqui"
```

---

## 🖥️ Executando os Serviços

### Iniciar o Backend (FastAPI)
Em um terminal, execute:
```bash
uv run uvicorn app.main:app --reload --port 8000
```
* **Swagger UI (Documentação Interativa):** [http://localhost:8000/docs](http://localhost:8000/docs)
* **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)
* **Health Check:** `http://localhost:8000/health`

### Iniciar o Frontend (Streamlit)
Em outro terminal, execute:
```bash
uv run streamlit run src/ui/app.py
```
* **Interface Web:** [http://localhost:8501](http://localhost:8501)

---

## 📡 Endpoints da API

| Método | Endpoint | Descrição | Autenticação |
| :--- | :--- | :--- | :---: |
| `GET` | `/health` | Checagem de saúde da API e status do modelo em memória | Sim (`X-API-Key`) |
| `GET` | `/data-sample/input` | Retorna uma amostra de teste para preenchimento de testes | Sim (`X-API-Key`) |
| `POST` | `/predict/single` | Predição unitária para um usuário | Sim (`X-API-Key`) |
| `POST` | `/predict/batch` | Predição em lote recebendo uma lista JSON | Sim (`X-API-Key`) |
| `POST` | `/predict/csv` | Upload de arquivo `.csv`, retornando streaming com predições | Sim (`X-API-Key`) |

### Exemplo de Chamada (`/predict/single`)
```bash
curl -X POST "http://localhost:8000/predict/single" \
     -H "Content-Type: application/json" \
     -H "X-API-Key: sua_chave_secreta_aqui" \
     -d '{
       "total_pedidos": 1,
       "receita_total_em_usd": 45.0,
       "ticket_medio_em_usd": 45.0,
       "recencia_dias": 28,
       "dias_desde_primeiro_pedido": 28,
       "tempo_relacionamento_dias": 0,
       "total_itens_comprados": 2,
       "total_interacoes_quinzena_1": 0,
       "total_interacoes_quinzena_2": 15,
       "total_interacoes_quinzena_3": 0,
       "total_interacoes_quinzena_4": 0
     }'
```

**Resposta:**
```json
{
  "predicao_classe": 1,
  "predicao_probabilidade": 0.82,
  "predicao_status": "Churn"
}
```

---

## 🛠️ Tecnologias Utilizadas

* **Linguagem & Ambiente:** Python 3.14+, `uv`, Linux
* **Dados & BigQuery:** Google Cloud BigQuery, `google-cloud-bigquery`, `db-dtypes`, `pyarrow`, `pandas`
* **Machine Learning:** `scikit-learn` (HistGradientBoosting, FunctionTransformer, ColumnTransformer, SelectKBest, GridSearchCV), `joblib`
* **Backend:** `FastAPI`, `Uvicorn`, `Pydantic v2`, `pydantic-settings`, `python-dotenv`
* **Frontend:** `Streamlit`, `requests`
* **Análise Exploratória:** `matplotlib`, `seaborn`

---

## 👤 Autor

Desenvolvido por **José Anselmo**  
* GitHub: [@jafmatos](https://github.com/jafmatos)  
* Email: [anselmojose297@gmail.com](mailto:anselmojose297@gmail.com)
