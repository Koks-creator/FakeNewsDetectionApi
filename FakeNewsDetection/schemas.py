import re
from pydantic import BaseModel, field_validator, constr
from nltk import word_tokenize

from FakeNewsDetection import config


class PredictionRequest(BaseModel):
    text: constr(min_length=1)

    @field_validator("text")
    def validate_text(cls, value):
        num_words = len(word_tokenize(value))

        if num_words > config.MAX_SEQUENCE_LENGTH:
            raise ValueError(f"Maximum words number is {config.MAX_SEQUENCE_LENGTH}")
        return value


class PredictionResponse(BaseModel):
    class_id: int
    class_name: str


class UrlPredictionRequest(BaseModel):
    article_url: constr(min_length=1)
    trim: bool = True

    @field_validator("article_url")
    def validate_article_url(cls, value):
        url_pattern = re.compile(
            r'^(https?):\/\/'  # protocol (http, https, ftp)
            r'([a-zA-Z0-9.-]+)'  # domain
            r'(\.[a-zA-Z]{2,})'  # top-level domain (TLD)
            r'(\/\S*)?$'  # path
        )

        if not bool(re.match(url_pattern, value)):
            raise ValueError("Provided url is not a valid url")
        return value
