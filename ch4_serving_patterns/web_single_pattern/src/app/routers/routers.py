import uuid
from typing import Dict, List

from logging import getLogger

from fastapi import APIRouter
from src.ml.prediction import Data, classifier

logger = getLogger(__name__)
router = APIRouter()

@router.get("/health")
def health() -> Dict[str, str]:
    return {"health": "ok"}

@router.get("/predict/test")
def predict_test() -> Dict[str, List[float]]:
    job_id = str(uuid.uuid4())
    prediction = []
    logger.info(f"prediction test {job_id}: {prediction}")
    return {"prediction": prediction}

@router.post("/predict")
def predict(data: Data) -> Dict[str, List[float]]:
    job_id = str(uuid.uuid4())
    logger.info(f"data")
    prediction = classifier.predict(data.data)
    prediction_list = list(prediction)
    logger.info(f"prediction {job_id}: {prediction_list}")
    return {"prediction": prediction_list}
