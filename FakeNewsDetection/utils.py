from dataclasses import dataclass
import re
import string
import numpy as np
from keras.preprocessing.sequence import pad_sequences

from FakeNewsDetection import tokenizer, config


@dataclass
class DataCleaning:

    @staticmethod
    def remove_html_tags(raw_text: str) -> str:
        cleanr = re.compile("<.*?>")
        cleantext = re.sub(cleanr, '', raw_text)
        return cleantext

    @staticmethod
    def remove_url(text: str) -> str:
        url_pattern = re.compile(r"http[s]?://\S+.\S+.\S+")
        return url_pattern.sub(r"", text)

    @staticmethod
    def remove_punct(text: str) -> str:
        translator = str.maketrans("", "", string.punctuation)
        return text.translate(translator)

    @staticmethod
    def remove_non_ascii(text: str) -> str:
        pattern = re.compile(r"[^\x00-\x7f][ ]?")
        return pattern.sub(r"", text)

    def clean(self, text: str) -> str:
        text = self.remove_html_tags(text)
        text = self.remove_url(text)
        text = self.remove_punct(text)
        text = self.remove_non_ascii(text)

        return text


def prepare_for_model(text: str) -> np.array:
    text_array = np.array([text])
    tokenized_text = tokenizer.texts_to_sequences(text_array)
    data = pad_sequences(tokenized_text,
                         maxlen=config.MAX_SEQUENCE_LENGTH,
                         padding="pre",
                         truncating="pre")

    return data
