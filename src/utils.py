import os

from googletrans import Translator as GTranslator
from deepl import Translator as DTranslator


from src.exceptions import MissingDotenvVar


def get_env_var(key: str):
    if (var := os.getenv(key)) is not None:
        return var
    raise MissingDotenvVar(f'В .env отсутствует переменная {key}')


def detect_lang(translator, text: str):
    if isinstance(translator, GTranslator):
        return translator.detect(text).lang
    elif isinstance(translator, DTranslator):
        raise NotImplementedError(f'Поддержка DeepL ещё не реализована')
    else:
        raise Exception(f'Unknown translator is passed: {translator.__class__}')
