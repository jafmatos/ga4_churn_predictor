from ui.api_client import APIError
from ui.api_client import api_client
import streamlit


@streamlit.cache_data(max_entries=1, ttl=3600)
def get_input_dataframe_sample(sample_size: int = 1) -> dict[str, any]:
    sample_dataframe = api_client.get_input_dataframe_sample(sample_size=sample_size)
    sample_dict_list = sample_dataframe.to_dict(orient="records")

    return sample_dict_list[0]


streamlit.header("Predição Unitária (JSON)")

if streamlit.session_state.get("form_values", None) is None:
    streamlit.session_state["form_values"] = {}

if streamlit.button("Preencher com amostra de testes"):
    sample = get_input_dataframe_sample(sample_size=1)

    streamlit.session_state["form_values"] = sample


with streamlit.form("predict_single_form", clear_on_submit=False, enter_to_submit=True):
    form_values: dict[str, any] = streamlit.session_state.get("form_values", {})

    row_1_cols = streamlit.columns(4)

    total_pedidos = row_1_cols[0].number_input(
        "Total de pedidos",
        min_value=1,
        step=1,
        placeholder="Total de pedidos",
        required=True,
        value=form_values.get("total_pedidos", None),
    )
    receita_total_em_usd = row_1_cols[1].number_input(
        "Receita total",
        min_value=0.00,
        step=0.01,
        placeholder="Receita total em dólares",
        required=True,
        value=form_values.get("receita_total_em_usd", None),
    )
    ticket_medio_em_usd = row_1_cols[2].number_input(
        "Ticket médio",
        min_value=0.00,
        step=0.01,
        placeholder="Ticket médio em dólares",
        required=True,
        value=form_values.get("ticket_medio_em_usd", None),
    )
    total_itens_comprados = row_1_cols[3].number_input(
        "Itens comprados",
        min_value=0,
        step=1,
        placeholder="Total de itens comprados",
        required=True,
        value=form_values.get("total_itens_comprados", None),
    )

    row_2_cols = streamlit.columns(2)

    recencia_dias = row_2_cols[0].number_input(
        "Recência em dias",
        min_value=0,
        step=1,
        placeholder="Recência em dias",
        required=True,
        value=form_values.get("recencia_dias", None),
    )
    tempo_relacionamento_dias = row_2_cols[1].number_input(
        "Tempo de relacionamento",
        min_value=0,
        step=1,
        placeholder="Tempo de relacionamento em dias",
        required=True,
        value=form_values.get("tempo_relacionamento_dias", None),
    )

    dias_desde_primeiro_pedido = streamlit.number_input(
        "Dias desde o primeiro pedido",
        min_value=0,
        step=1,
        placeholder="Dias desde o primeiro pedido",
        required=True,
        value=form_values.get("dias_desde_primeiro_pedido", None),
    )

    row_4_cols = streamlit.columns(2)

    total_interacoes_quinzena_1 = row_4_cols[0].number_input(
        "Interações quinzena 1",
        min_value=0,
        step=1,
        placeholder="Total de interações na primeira quinzena",
        required=True,
        value=form_values.get("total_interacoes_quinzena_1", None),
    )
    total_interacoes_quinzena_2 = row_4_cols[1].number_input(
        "Interações quinzena 2",
        min_value=0,
        step=1,
        placeholder="Total de interações na segunda quinzena",
        required=True,
        value=form_values.get("total_interacoes_quinzena_2", None),
    )

    row_5_cols = streamlit.columns(2)

    total_interacoes_quinzena_3 = row_5_cols[0].number_input(
        "Interações quinzena 3",
        min_value=0,
        step=1,
        placeholder="Total de interações na terceira quinzena",
        required=True,
        value=form_values.get("total_interacoes_quinzena_3", None),
    )
    total_interacoes_quinzena_4 = row_5_cols[1].number_input(
        "Interações quinzena 4",
        min_value=0,
        step=1,
        placeholder="Total de interações na quarta quinzena",
        required=True,
        value=form_values.get("total_interacoes_quinzena_4", None),
    )

    form_submitted = streamlit.form_submit_button(
        "Gerar previsão", type="primary", width="stretch"
    )

if form_submitted:
    try:
        output = api_client.predict_single(
            total_pedidos=total_pedidos,
            receita_total_em_usd=receita_total_em_usd,
            ticket_medio_em_usd=ticket_medio_em_usd,
            total_itens_comprados=total_itens_comprados,
            recencia_dias=recencia_dias,
            tempo_relacionamento_dias=tempo_relacionamento_dias,
            dias_desde_primeiro_pedido=dias_desde_primeiro_pedido,
            total_interacoes_quinzena_1=total_interacoes_quinzena_1,
            total_interacoes_quinzena_2=total_interacoes_quinzena_2,
            total_interacoes_quinzena_3=total_interacoes_quinzena_3,
            total_interacoes_quinzena_4=total_interacoes_quinzena_4,
        )

        if output.predicao_status == "Churn":
            streamlit.warning("Este cliente tem alta probabilidade de churn.")
        else:
            streamlit.success("Este cliente tem baixa probabilidade de churn.")

        col_1, col_2 = streamlit.columns(2)

        col_1.metric(
            "Probabilidade de Churn",
            value=f"{output.predicao_probabilidade:.0%}",
        )

        col_2.metric(
            "Status do Usuário",
            value=output.predicao_status,
        )

    except APIError as exception:
        streamlit.error(str(exception))
