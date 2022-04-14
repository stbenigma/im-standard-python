import re

lang_pattern = re.compile(r'^\*..\* (.+)')


def strip_translation_meta_data(value: str) -> str:
    match = lang_pattern.match(value)
    if match:
        value = match.groups(1)[0]

    if value.startswith('**'):
        value = value[2:]

    if value.startswith('*'):
        value = value[1:]

    return value


class Translator:

    def __init__(self, default_language: str = 'en'):
        self.default_language = default_language

    def tr(self, item, lang: str = None):
        if lang is None:
            lang = self.default_language
        res = self.inner_tr(item, lang)
        if isinstance(res, dict):
            res = self.tr(res, lang)
        if isinstance(res, list):
            result = []
            for e in res:
                result.append(self.tr(e, lang))
            return result
        assert res is None or isinstance(res, str), f"Result is of type {type(res)}"
        return strip_translation_meta_data(res)

    @staticmethod
    def inner_tr(item, lang) -> str:
        if isinstance(item, str):
            return item
        if isinstance(item, dict) and len(item) > 0:
            translation = item.get(lang)
            if translation is not None:
                return translation
            else:
                return next(iter(item.values()))
        return ''
