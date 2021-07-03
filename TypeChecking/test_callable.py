from typing import Callable, List
import math


def multiply(inputs: List[int]) -> int:
    return math.prod(inputs)


def run_doubled_inputs_function(func: Callable[[List[int]], int], inputs: List[int]) -> int:
    doubled_inputs = [i * 2 for i in inputs]
    return func(doubled_inputs)


inputs = [1, 2, 3]
print(multiply(inputs))
print(run_doubled_inputs_function(multiply, inputs))
