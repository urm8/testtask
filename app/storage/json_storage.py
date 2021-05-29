from __future__ import annotations

from decimal import Decimal

import orjson
from pathlib import Path
from dataclasses import fields
from functools import cached_property, lru_cache
from typing import Any, Iterable

from model import TaxBand
from storage.storagebase import StorageBase


class JSONStorage(StorageBase):
    def __init__(self, fp: str | Path) -> None:
        self.fp = Path(fp).resolve()

    @cached_property
    def tax_bands(self) -> Iterable[TaxBand]:
        raw_bands = _load_tax_bands(self.fp)
        fields_ = fields(TaxBand)
        return [
            TaxBand(**{f.name: self._as_decimal(band[f.name]) for f in fields_})
            for band in raw_bands
        ]

    @staticmethod
    def _as_decimal(value) -> Decimal | None:
        if value is not None:
            return Decimal(value)


@lru_cache(32)
def _load_tax_bands(fp: Path) -> list[dict[str, Any]]:
    with open(fp) as fin:
        return orjson.loads(fin.read())
