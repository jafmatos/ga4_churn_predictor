from ui.api_client import api_client
import streamlit
import pandas


@streamlit.cache_data(show_spinner=False)
def load_sample_data(sample_size: int = 10) -> pandas.DataFrame:
    return api_client.get_input_dataframe_sample(sample_size=sample_size)


streamlit.header("Visão Geral do Modelo")
streamlit.markdown(
    """
    Este painel apresenta o sistema preditivo de **Churn (evasão de clientes)** treinado a partir de 
    eventos comportamentais reais do **Google Analytics 4 (GA4)** via **Google BigQuery**.
    
    O objetivo é identificar antecipadamente clientes com alto risco de inatividade, 
    permitindo intervenções automatizadas de retenção e marketing direcionado.
    """
)

col1, col2 = streamlit.columns(2)

col1.metric(
    label="ROC-AUC Médio (k=5)",
    value="69.32%",
    delta="+3.52%",
    delta_color="green",
    help="Validação cruzada estratificada em 5 folds com busca sistemática de hiperparâmetros.",
)
col2.metric(
    label="Latência de Inferência",
    value="~10 ms",
    help="Tempo médio de resposta por requisição unitária no backend FastAPI.",
)

streamlit.metric(
    label="Algoritmo",
    value="HistGradientBoosting",
    help="Gradient Boosted Trees com pesos balanceados e discretização em histogramas.",
)

streamlit.divider()

streamlit.subheader("Amostra dos Dados de Entrada")


@streamlit.fragment(parallel=True)
def render_data_samples():
    with streamlit.spinner("Carregando amostras de dados...", show_time=True):
        sample_dataframe = load_sample_data()

        with streamlit.expander("Amostra unitária (JSON)"):
            streamlit.json(sample_dataframe.sample(n=1).to_dict(orient="records")[0])

        with streamlit.expander("Amostra em lote (JSON)"):
            streamlit.json(sample_dataframe.sample(n=10).to_dict(orient="records"))

        with streamlit.expander("Amostra em lote (CSV)"):
            streamlit.dataframe(sample_dataframe.sample(n=10), hide_index=True)


render_data_samples()