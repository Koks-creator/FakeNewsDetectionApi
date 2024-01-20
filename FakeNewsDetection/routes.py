import json
from fastapi import HTTPException
from newspaper import Article
from nltk import word_tokenize

from FakeNewsDetection import app, model, config, app_logger
from FakeNewsDetection.schemas import PredictionRequest, PredictionResponse, UrlPredictionRequest
from FakeNewsDetection.utils import DataCleaning, prepare_for_model


data_cleaning = DataCleaning()


@app.get("/")
async def is_alive() -> dict:
    return {"msg": "Hello, I am alive"}


@app.get("/model_summary")
async def get_model_summary() -> dict:
    string_list = []
    model.summary(print_fn=lambda x: string_list.append(x))
    short_model_summary = "\n".join(string_list)

    return {"Summary": short_model_summary}


@app.get("/model_languages")
async def get_model_langs() -> dict:
    return {"ModelLanguages": ["english"]}


@app.post("/predict_from_text", response_model=PredictionResponse)
async def predict_from_text(text: PredictionRequest) -> PredictionResponse:
    app_logger.info("Preparing for predict_from_text")
    cleaned_text = data_cleaning.clean(text=text.text)
    sequence = prepare_for_model(cleaned_text)

    app_logger.info("Making prediction for predict_from_text")
    prediction = int(model.predict(sequence).round().squeeze())
    class_name = config.CLASSES[prediction]
    return PredictionResponse(class_id=prediction, class_name=class_name)


@app.post("/predict_from_url", response_model=PredictionResponse)
async def predict_from_url(url_predict_req: UrlPredictionRequest) -> PredictionResponse:
    app_logger.info("Scraping article for predict_from_url")
    article = Article(url_predict_req.article_url)
    article.download()
    article.parse()

    app_logger.info("Preparing for predict_from_url")
    if article.text:
        cleaned_text = data_cleaning.clean(text=article.text)

        if url_predict_req.trim:
            cleaned_text = cleaned_text[:config.MAX_SEQUENCE_LENGTH]
        else:
            if len(word_tokenize(cleaned_text)) > config.MAX_SEQUENCE_LENGTH:
                raise HTTPException(status_code=413, detail=f"Article is too large, max sequence length is "
                                                            f"{config.MAX_SEQUENCE_LENGTH}, you can set trim flag to "
                                                            f"true in order to fit in max sequence length.")
        sequence = prepare_for_model(cleaned_text)

        app_logger.info("Making prediction for predict_from_url")
        prediction = int(model.predict(sequence).round().squeeze())
        class_name = config.CLASSES[prediction]

        return PredictionResponse(class_id=prediction, class_name=class_name)
    else:
        raise HTTPException(status_code=400, detail=f"Article is empty.")
