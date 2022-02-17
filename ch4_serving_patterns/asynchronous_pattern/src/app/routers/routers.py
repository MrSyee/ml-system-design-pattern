import base64
import io
import uuid
from typing import Dict

from logging import getLogger

from fastapi import APIRouter, BackgroundTasks
from PIL import Image
from src.app.backend import background_job, store_data_job
from src.app.backend.data import Data


logger = getLogger(__name__)
router = APIRouter()


@router.get("/health")
def health() -> Dict[str, str]:
    return {"health": "ok"}


@router.post("/predict")
def predict(data: Data, background_tasks: BackgroundTasks) -> Dict[str, str]:
    image = base64.b64decode(str(data.image_data))
    io_bytes = io.BytesIO(image)
    data.image_data = Image.open(io_bytes)
    job_id = str(uuid.uuid4())[:6]
    # Background에서 redis에 큐를 등록
    background_job.save_data_job(
        data=data.image_data,
        job_id=job_id,
        background_tasks=background_tasks,
        enqueue=True,
    )
    return {"job_id": job_id}

@router.get("/job/{job_id}")
def prediction_result(job_id: str) -> Dict[str, Dict[str, str]]:
    result = {job_id: {"prediction": ""}}
    data = store_data_job.get_data_redis(job_id)
    result[job_id]["prediction"] = data
    return result
