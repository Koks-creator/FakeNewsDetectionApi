from dataclasses import dataclass, field
import json
import logging
import pickle
from typing import List
from fastapi import FastAPI
import tensorflow as tf
from keras.models import Sequential
import nltk


@dataclass
class CustomLogger:
    format: str = "%(asctime)s - %(name)s - %(levelname)s - Line: %(lineno)s - %(message)s"
    file_handler_format: logging.Formatter = logging.Formatter(format)
    log_file_name: str = "logs.txt"
    logger_name: str = __name__
    logger_log_level: int = logging.ERROR
    file_handler_log_level: int = logging.ERROR

    def create_logger(self) -> logging.Logger:
        logging.basicConfig(format=self.format)
        logger = logging.getLogger(self.logger_name)
        logger.setLevel(self.logger_log_level)

        file_handler = logging.FileHandler(self.log_file_name)
        file_handler.setLevel(self.logger_log_level)

        file_handler.setFormatter(self.file_handler_format)
        logger.addHandler(file_handler)

        return logger


@dataclass(frozen=True)
class Config:
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    DEBUG: bool = True
    MODEL_FOLDER: str = "model"
    MODEL_NAME: str = "FakeNewsModel.h5"
    TOKENIZER_NAME: str = "tokenizer.pkl"
    CLASSES: List[str] = field(default_factory=lambda: ["Fake", "Real"])
    MAX_SEQUENCE_LENGTH: int = 6000
    UVICORN_LOG_CONFIG_PATH: str = "uvicorn_log_config.json"


config = Config()

app_logger = CustomLogger(
    logger_name="Model",
    logger_log_level=logging.INFO
).create_logger()

app_logger.info("Preparing NLTK punkt model")
nltk.download('punkt')

app = FastAPI(debug=config.DEBUG, title="FakeNewsDetectionApi")

with open(config.UVICORN_LOG_CONFIG_PATH) as f:
    uvicorn_log_config = json.load(f)

app_logger.info(f"Loading tokenizer from: {config.MODEL_FOLDER}/{config.TOKENIZER_NAME}...")
with open(f"{config.MODEL_FOLDER}/{config.TOKENIZER_NAME}", "rb") as f:
    tokenizer = pickle.load(f)
app_logger.info("Tokenizer loaded")

app_logger.info(f"Loading model from: {config.MODEL_FOLDER}/{config.MODEL_NAME}...")
model: Sequential = tf.keras.models.load_model(f"{config.MODEL_FOLDER}/{config.MODEL_NAME}")
app_logger.info("Model loaded")

from FakeNewsDetection import routes
