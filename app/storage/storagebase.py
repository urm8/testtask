from __future__ import annotations

import abc
from collections import Iterable

from model import TaxBand


class StorageBase(metaclass=abc.ABCMeta):
    @property
    @abc.abstractmethod
    def tax_bands(self) -> Iterable[TaxBand]:
        ...
