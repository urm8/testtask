from __future__ import annotations
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Any

P_INF = Decimal("Inf")


@dataclass(frozen=True)
class TaxBand:
    lower: Decimal
    upper: Decimal
    rate: Decimal


@dataclass
class Tax:
    amount: Decimal = field(default_factory=Decimal)
    rate: Decimal | None = None
    details: list["Tax"] | str | dict[str, Any] | None = None
