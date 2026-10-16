from ui.api_client import api_client
import streamlit

home_page = streamlit.Page(
    page="pages/home.py",
    title="Início",
    url_path="/",
    default=True,
)

predict_single_page = streamlit.Page(
    "pages/predict_single.py",
    title="Predição Unitária",
    url_path="/predict_single",
)

predict_csv_page = streamlit.Page(
    "pages/predict_csv.py",
    title="Predição em Lote",
    url_path="/predict-csv",
)

navigation = streamlit.navigation(
    pages=[home_page, predict_single_page, predict_csv_page]
)

streamlit.set_page_config(
    page_title="Preditor de Churn GA4",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="expanded",
)

with streamlit.spinner("Verificando disponibilidade do modelo...", show_time=True):
    is_model_available = api_client.get_is_model_available()

if not is_model_available:
    streamlit.error(body="O modelo não está disponível. Tente novamente mais tarde.")

    streamlit.stop()

streamlit.title("Painel de Previsão de Churn GA4")
streamlit.divider()

navigation.run()

streamlit.divider()
streamlit.caption("Versão do modelo: v1.0.0 | Último retreino: Outubro/2026")
