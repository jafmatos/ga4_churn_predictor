from app.services.ml_service import get_ml_service
from fastapi import Depends
from app.services.ml_service import MLService
from app.security import validate_api_key
from fastapi import Security
from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["Disponibilidade"])

@router.get("", dependencies=[Security(validate_api_key)])
def get_health_check(ml_service: MLService = Depends(get_ml_service)):
    return {"status": "ready" if ml_service.get_is_model_loaded() else "unavailable"}
