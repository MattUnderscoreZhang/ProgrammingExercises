from typing import NamedTuple, Callable


class Animal(NamedTuple):  # centralized location for type definitions?
    name: str
    speak: Callable[None, None]  # note function does not take Animal as an input


def listen(animal: Animal) -> None:
    animal.speak()  # attaching function to object?


def init_lion() -> None:  # initialization method is reasonable?
    return Animal("lion",
                  lambda: print("ROAR"))


def init_tiger() -> None:
    return Animal("tiger",
                  lambda: print("roar"))


def init_wolf() -> None:
    return Animal("wolf",
                  lambda: print("howl"))
