from decimal import Decimal
from typing import Any

import orjson
from flask import Flask


def default(obj: object) -> str:
    if isinstance(obj, Decimal):
        return str(obj)
    raise TypeError


class _Decoder:
    def __init__(self, **kwargs) -> None:
        self.options = kwargs

    def decode(self, obj: str) -> dict[Any, Any]:
        return orjson.loads(obj)


class _Encoder:
    def __init__(self, **kwargs) -> None:
        self.options = kwargs

    def encode(self, obj: dict[Any, Any]) -> str:
        return orjson.dumps(obj, default=default).decode("utf-8")


def setup(app: Flask) -> Flask:
    """
    mutate app, so it uses orjson as default json decoder/encoder
    :param app: Flask app to mutate
    :return: mutated flask app
    """
    app.json_decoder = _Decoder
    app.json_encoder = _Encoder
    return app
