from ga4_churn_predictor.config import DATA_PATH
import pandas
from ga4_churn_predictor.config import PROCESSED_DATA_DIR


class DataService:
    def __init__(self):
        pass

    def load_x_test_data(self) -> pandas.DataFrame:
        return pandas.read_csv(PROCESSED_DATA_DIR / "x_test.csv")

    def load_raw_data(self) -> pandas.DataFrame:
        return pandas.read_parquet(DATA_PATH)


data_service = DataService()

def get_data_service() -> DataService:
    return data_service
