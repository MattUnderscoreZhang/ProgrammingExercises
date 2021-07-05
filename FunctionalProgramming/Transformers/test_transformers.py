import transformer


def test_transformers():
    exponentiator_a = transformer.init_exponentiator(1, 2)
    exponentiator_b = transformer.init_exponentiator(1, 3)
    expander_a = transformer.init_expander([1])
    expander_b = transformer.init_expander(['a', 'b'])

    transformers = [exponentiator_a, exponentiator_b, expander_a, expander_b]

    for i in range(10):
        transformers = [transformer_i.transform(transformer_i) for transformer_i in transformers]
    for transformer_i in transformers:
        print(transformer_i.params)
