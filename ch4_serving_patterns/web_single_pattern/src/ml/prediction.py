import os
import json
from typing import Dict, List
from logging import getLogger

import onnxruntime as rt
import numpy as np

from pydantic import BaseModel

logger = getLogger(__name__)


class Data(BaseModel):
    data: List[List[float]] = [[5.1, 3.5, 1.4, 0.2]]

class Classifier:
    def __init__(
        self,
        model_filepath: str,
        label_filepath: str,
    ):
        self.model_filepath: str = model_filepath
        self.label_filepath: str = label_filepath
        self.classifier = None
        self.label: Dict[str, str] = {}
        self.input_name: str = ""
        self.output_name: str = ""

        self.load_model()
        self.load_label()

    def load_model(self):
        logger.info(f"Load model in {self.model_filepath}")
        self.classifier = rt.InferenceSession(self.model_filepath)
        self.input_name = self.classifier.get_inputs()[0].name
        self.output_name = self.classifier.get_outputs()[0].name
        logger.info(f"initialized model")

    def load_label(self):
        logger.info(f"load label in {self.label_filepath}")
        with open(self.label_filepath, "r") as f:
            self.label = json.load(f)
        logger.info(f"label: {self.label}")

    def predict(self, data: List[List[int]]) -> np.ndarray:
        np_data = np.array(data).astype(np.float32)
        prediction = self.classifier.run(None, {self.input_name: np_data})
        output = np.array(list(prediction[1][0].values()))
        logger.info(f"predict proba {output}")
        return output


classifier = Classifier(
    model_filepath="./model/iris_svc.onnx",
    label_filepath="./model/label.json",
)
