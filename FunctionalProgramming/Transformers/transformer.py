from __future__ import annotations
from typing import NamedTuple, Callable, List, Any


class Transformer(NamedTuple):
    params: NamedTuple
    transform: Callable[Transformer, Transformer]


def init_exponentiator(initial: float, multiplier: float) -> Transformer:
    class Params(NamedTuple):  # use of params?
        value: float
        multiplier: float

    def exponentiate(exponentiator: Transformer) -> Transformer:  # defining a function inside the init function?
        return Transformer(Params(exponentiator.params.value * exponentiator.params.multiplier,
                                  exponentiator.params.multiplier),
                           exponentiator.transform)

    return Transformer(Params(initial, multiplier),
                       exponentiate)


def init_expander(initial: List[Any]) -> Transformer:
    class Params(NamedTuple):
        chain: List[Any]
        chain_unit: List[Any]

    def expand(expander: Transformer) -> Transformer:
        return Transformer(Params(expander.params.chain + expander.params.chain_unit,
                                  expander.params.chain_unit),
                           expander.transform)

    return Transformer(Params(initial, initial),
                       expand)
