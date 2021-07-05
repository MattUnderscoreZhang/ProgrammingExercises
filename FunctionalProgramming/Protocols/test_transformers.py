import transformer
from typing import List


def test_transformers():
    exponentiator_a = transformer.Exponentiator(1, 2)
    exponentiator_b = transformer.Exponentiator(1, 3)
    expander_a = transformer.Expander([1], [1])
    expander_b = transformer.Expander(['a', 'b'], ['a', 'b'])

    transformers = [exponentiator_a, exponentiator_b, expander_a, expander_b]
    assert(isinstance(transformers, List[transformer.Transformer]))

    for i in range(10):
        transformers = [transformer_i.transform(transformer_i) for transformer_i in transformers]
    for transformer_i in transformers:
        print(transformer_i)
