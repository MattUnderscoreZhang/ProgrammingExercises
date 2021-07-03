from typing import List
import math


Vector = List[float]


def vector_length(vector: Vector) -> float:
    return math.sqrt(sum([i**2 for i in vector]))


def test_vector_length():
    vector = [1, 2, 3, 4]
    length = vector_length(vector)
    assert(length == math.sqrt(30))
