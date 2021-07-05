from typing import NamedTuple, List
import animal


class Zoo(NamedTuple):
    animals: List[animal.Animal]


def listen(zoo: Zoo) -> None:
    for my_animal in zoo.animals:  # should replace with map-reduce?
        animal.listen(my_animal)
