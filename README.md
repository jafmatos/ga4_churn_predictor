# GA4 Churn Predictor

Aplicação preditiva para antecipação de churn em e-commerce utilizando dados de eventos do Google Analytics 4 (BigQuery), com modelo desenvolvido em Scikit-Learn, microsserviço de inferência em FastAPI e interface interativa em Streamlit.

---

## Visão Geral

O objetivo do projeto é prever se usuários que compraram em um e-commerce em novembro e dezembro irão abandonar o site no mês seguinte (janeiro), sem registrar novas visitas ou interações. 

A solução integra todo o fluxo:
- Extração e agregação de eventos do BigQuery (`bigquery-public-data.ga4_obfuscated_sample_ecommerce`).
- Pipeline de pré-processamento, seleção de atributos e classificação com Scikit-Learn.
- API REST para predições unitárias, em lote e streaming de arquivos CSV.
- Interface analítica multipágina para testes e simulações.

---

## Tecnologias Utilizadas

- **Linguagem & Ambiente:** Python 3.14+, `uv`
- **Machine Learning & Dados:** Scikit-Learn, BigQuery, Pandas, PyArrow, Joblib
- **API Backend:** FastAPI, Uvicorn, Pydantic, Pydantic-Settings
- **Frontend:** Streamlit

---

## Instalação e Configuração

### 1. Clonar o repositório e instalar dependências

```bash
git clone https://github.com/jafmatos/ga4_churn_predictor.git
cd ga4_churn_predictor

# Cria o ambiente virtual e instala as dependências
uv sync
```

### 2. Configurar as variáveis de ambiente

O projeto utiliza dois arquivos de configuração baseados nos templates `.example`:

**API Backend (`.env`):**
```bash
cp .env.example .env
```
Edite o arquivo `.env` com suas configurações:
```env
API_TITLE="GA4 Churn Predictor API"
API_VERSION="1.0.0"
API_DESCRIPTION="API preditiva de churn para e-commerce GA4"
API_SECRET_KEY="sua_chave_secreta"
```

**Interface Streamlit (`.env.streamlit`):**
```bash
cp .env.streamlit.example .env.streamlit
```
Edite o arquivo `.env.streamlit`:
```env
API_BASE_URL="http://localhost:8000"
API_SECRET_KEY="sua_chave_secreta"
```

---

## Execução

### 1. Iniciar a API (FastAPI)

```bash
uv run uvicorn app.main:app --reload --port 8000
```

- Documentação Swagger: [http://localhost:8000/docs](http://localhost:8000/docs)
- Documentação ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### 2. Iniciar a Interface (Streamlit)

Em outro terminal:

```bash
uv run streamlit run src/ui/app.py
```

- Interface web: [http://localhost:8501](http://localhost:8501)

### 3. Re-treinar o modelo (Opcional)

Para executar o pipeline de treinamento e salvar uma nova versão do modelo:

```bash
uv run python -m ga4_churn_predictor.train
```

Para avaliar as métricas no conjunto de teste:

```bash
uv run python -m ga4_churn_predictor.evaluate
```

---

## Endpoints da API

Todas as rotas exigem autenticação via cabeçalho HTTP `X-API-Key`.

| Método | Rota | Descrição |
| :--- | :--- | :--- |
| `GET` | `/health` | Status da API e verificação do modelo carregado em memória |
| `GET` | `/data-sample/input` | Retorna uma amostra de teste para preenchimento de formulários |
| `POST` | `/predict/single` | Predição unitária para um único usuário |
| `POST` | `/predict/batch` | Predição em lote recebendo uma lista de usuários via JSON |
| `POST` | `/predict/csv` | Upload de arquivo `.csv`, retornando o arquivo processado via streaming |

### Exemplo de Requisição (`POST /predict/single`)

```bash
curl -X POST "http://localhost:8000/predict/single" \
     -H "Content-Type: application/json" \
     -H "X-API-Key: sua_chave_secreta" \
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

## Autor

Desenvolvido por **José Anselmo**  
- GitHub: [@jafmatos](https://github.com/jafmatos)  
- Email: [anselmojose297@gmail.com](mailto:anselmojose297@gmail.com)
