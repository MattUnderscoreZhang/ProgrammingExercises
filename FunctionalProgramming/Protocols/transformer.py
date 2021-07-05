from __future__ import annotations
from typing import Protocol, NamedTuple, List, Any


class Transformer(Protocol):
    params: NamedTuple

    def transform(self, transformer: Transformer) -> Transformer: ...


class Exponentiator(NamedTuple):
    value: float
    multiplier: float

    def transform(self, exponentiator: Transformer) -> Transformer:
        return Exponentiator(exponentiator.value * exponentiator.multiplier,
                             exponentiator.multiplier)


class Expander(NamedTuple):
    chain: List[Any]
    chain_unit: List[Any]

    def transform(self, expander: Transformer) -> Transformer:
        return Expander(expander.chain + expander.chain_unit,
                        expander.chain_unit)
