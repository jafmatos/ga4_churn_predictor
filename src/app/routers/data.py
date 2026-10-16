from fastapi import Query
import io
from fastapi import Depends
from fastapi import Security
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from app.services.data_service import DataService
from app.services.data_service import get_data_service
from app.security import validate_api_key

router = APIRouter(prefix="/data-sample", tags=["Dados"])


@router.get("/input", dependencies=[Security(validate_api_key)])
def get_input_data_sample(
    data_service: DataService = Depends(get_data_service),
    sample_size: int = Query(
        default=10, ge=1, le=100, description="Tamanho da amostra de dados"
    ),
):
    dataframe = data_service.load_x_test_data().sample(n=sample_size, random_state=42)

    buffer = io.BytesIO()
    dataframe.to_csv(buffer, index=False, encoding="utf-8")
    buffer.seek(0)

    return StreamingResponse(
        content=buffer,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=x_test_sample.csv"},
    )
