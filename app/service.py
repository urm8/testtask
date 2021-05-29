from __future__ import annotations

from decimal import Decimal

from model import Tax
from storage.storagebase import StorageBase


class Service:
    def __init__(self, storage: StorageBase) -> None:
        self.storage = storage

    def get_tax_amount(self, annual_income: Decimal, details: bool) -> Tax:
        """:returns tax amount for given :param annual_income: with tax rate found in datasource"""
        tax = Tax()
        remainder = annual_income

        for band in self.storage.tax_bands:
            if remainder <= 0.001:
                break
            upper = band.upper or Decimal('Inf')
            taxable_part = remainder
            if annual_income > upper:
                taxable_part = remainder - (annual_income - band.upper)
            remainder -= taxable_part
            tax_amount = self.get_tax(taxable_part, tax_rate=band.rate)
            tax.amount += tax_amount

            if details:
                tax.details = tax.details or []
                tax.details.append(Tax(amount=tax_amount, rate=band.rate, details={
                    'amount': taxable_part,
                    'range': f"[{band.lower}:{upper}]"
                }))
        return tax

    @staticmethod
    def get_tax(income: Decimal, tax_rate: Decimal) -> Decimal:
        """
        extracts the tax amount from given :param income: and :param tax_rate:

        not sure if this is correct, but I couldn't find legal instructions on how to round pound prices,
        so fallback to simple arithmetical rules here
        """
        return (income * tax_rate / 100).quantize(Decimal(".01"))
