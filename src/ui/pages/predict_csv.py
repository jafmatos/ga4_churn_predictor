from ui.api_client import APIError
from ui.api_client import api_client
import streamlit

streamlit.header("Predição em Lote (CSV)")

with streamlit.form("predict_csv_form"):
    csv_file = streamlit.file_uploader(
        "Upload do arquivo CSV", type="csv", max_upload_size=10
    )

    form_submitted = streamlit.form_submit_button(
        "Gerar previsões", type="primary", width="stretch"
    )

if form_submitted:
    if csv_file is None:
        streamlit.error("Selecione um arquivo CSV")
    else:
        try:
            output_dataframe = api_client.predict_csv(csv_file.getvalue())

            streamlit.dataframe(output_dataframe, hide_index=True, width="stretch")
        except APIError as exception:
            streamlit.error(exception.message)
