from transformers import AutoTokenizer


def tokenize():
    tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")
    tokens = tokenizer("Hello world!")
    print(tokens)
    return tokens


def split_tokenize():
    tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")
    tokens = tokenizer.tokenize("Using a transformer network is simple! Doghouse, doggy, laptop, dumbwaiter, net, nettle, network, networkblahsdfsf.")
    print(tokens)
    ids = tokenizer.convert_tokens_to_ids(tokens)
    print(ids)
    return ids


def decode(tokens: list[int]):
    decoder = AutoTokenizer.from_pretrained("bert-base-cased")
    decoded = decoder.decode(tokens)
    print(decoded)
    return decoded


if __name__ == "__main__":
    # tokens = tokenize()
    tokens = split_tokenize()
    decode(tokens)
