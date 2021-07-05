from typing import NamedTuple, Callable


class Animal(NamedTuple):
    name: str
    speak: Callable[None, None]


def listen(animal: Animal) -> None:
    animal.speak()


def init_lion() -> None:
    return Animal("lion",
                  lambda: print("ROAR"))


def init_tiger() -> None:
    return Animal("tiger",
                  lambda: print("roar"))


def init_wolf() -> None:
    return Animal("wolf",
                  lambda: print("howl"))
