import io
import pandas
from pandas import DataFrame
import httpx
from ui.config import API_BASE_URL
from ui.config import API_SECRET_KEY


class APIError(Exception):
    def __init__(self, message: str = "Erro desconhecido"):
        self.message = message

    def __str__(self):
        return self.message


class PredictSingleOutput:
    def __init__(
        self, predicao_classe: int, predicao_status: str, predicao_probabilidade: float
    ):
        self.predicao_classe = predicao_classe
        self.predicao_status = predicao_status
        self.predicao_probabilidade = predicao_probabilidade


class APIClient:
    def __init__(self, base_url: str = API_BASE_URL, secret_key: str = API_SECRET_KEY):
        self.base_url = base_url
        self.secret_key = secret_key

    def get_is_model_available(self) -> bool:
        try:
            response = httpx.get(
                f"{self.base_url}/health", headers={"X-API-KEY": self.secret_key}
            )

            response.raise_for_status()

            body = response.json()

            return body["status"] == "ready"
        except:
            return False

    def get_input_dataframe_sample(self, sample_size: int = 10) -> DataFrame:
        try:
            response = httpx.get(
                url=f"{self.base_url}/data-sample/input?sample_size={sample_size}",
                headers={"X-API-KEY": self.secret_key},
            )

            response.raise_for_status()

            buffer = io.StringIO(response.text)
            dataframe = pandas.read_csv(buffer, encoding="utf-8")
            buffer.close()

            return dataframe
        except httpx.HTTPStatusError as exception:
            response_json = exception.response.json()

            raise APIError(response_json["detail"])

    def predict_single(
        self,
        total_pedidos: float,
        receita_total_em_usd: float,
        ticket_medio_em_usd: float,
        recencia_dias: int,
        dias_desde_primeiro_pedido: int,
        tempo_relacionamento_dias: int,
        total_itens_comprados: int,
        total_interacoes_quinzena_1: int,
        total_interacoes_quinzena_2: int,
        total_interacoes_quinzena_3: int,
        total_interacoes_quinzena_4: int,
    ) -> PredictSingleOutput:
        try:
            response = httpx.post(
                url=f"{self.base_url}/predict/single",
                headers={"X-API-KEY": self.secret_key},
                json={
                    "total_pedidos": total_pedidos,
                    "receita_total_em_usd": receita_total_em_usd,
                    "ticket_medio_em_usd": ticket_medio_em_usd,
                    "recencia_dias": recencia_dias,
                    "dias_desde_primeiro_pedido": dias_desde_primeiro_pedido,
                    "tempo_relacionamento_dias": tempo_relacionamento_dias,
                    "total_itens_comprados": total_itens_comprados,
                    "total_interacoes_quinzena_1": total_interacoes_quinzena_1,
                    "total_interacoes_quinzena_2": total_interacoes_quinzena_2,
                    "total_interacoes_quinzena_3": total_interacoes_quinzena_3,
                    "total_interacoes_quinzena_4": total_interacoes_quinzena_4,
                },
            )

            response.raise_for_status()

            response_body = response.json()

            return PredictSingleOutput(
                predicao_classe=response_body["predicao_classe"],
                predicao_status=response_body["predicao_status"],
                predicao_probabilidade=response_body["predicao_probabilidade"],
            )
        except httpx.HTTPStatusError as exception:
            response_json = exception.response.json()

            raise APIError(response_json["detail"])

    def predict_csv(self, csv_file_bytes: bytes) -> DataFrame:
        try:
            response = httpx.post(
                url=f"{self.base_url}/predict/csv",
                headers={"X-API-KEY": self.secret_key},
                files={"upload_file": ("upload.csv", csv_file_bytes, "text/csv")},
            )

            response.raise_for_status()

            buffer = io.StringIO(response.text)
            dataframe = pandas.read_csv(buffer, encoding="utf-8")
            buffer.close()

            return dataframe
        except httpx.HTTPStatusError as exception:
            response_json = exception.response.json()

            raise APIError(response_json["detail"])


api_client = APIClient()
