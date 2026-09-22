from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
SQL_DIR = ROOT_DIR / "sql"
SQL_QUERY_PATH = SQL_DIR / "ga4_event_query.sql"
DATA_PATH = ROOT_DIR / "dataset" / "raw" / "users.parquet"
MODEL_PATH = ROOT_DIR / "models" / "churn_model.joblib"
GOOGLE_APPLICATION_CREDENTIALS = ROOT_DIR / "key" / "sandbox-508815-f247f95f91fe.json"
BIGQUERY_PROJECT_ID = "sandbox-508815"

TEST_SIZE = 0.2
RANDOM_STATE = 42

NUMERICAL_FEATURES = [
    "total_pedidos",
    "receita_total_em_usd",
    "ticket_medio_em_usd",
    "recencia_dias",
    "tempo_relacionamento_dias",
]

CATEGORICAL_FEATURES = []

TARGET_FEATURE = "churn"
