import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification


def padding_and_masks():
    checkpoint = 'distilbert-base-uncased-finetuned-sst-2-english'
    tokenizer = AutoTokenizer.from_pretrained(checkpoint)
    model = AutoModelForSequenceClassification.from_pretrained(checkpoint)

    print(model(torch.tensor([[200, 200, 200]])).logits)
    print(model(torch.tensor([[200, 200]])).logits)

    outputs = model(
        torch.tensor(
            [
                [200, 200, 200],
                [200, 200, tokenizer.pad_token_id],
            ]
        ),
        attention_mask=torch.tensor(
            [
                [1, 1, 1],
                [1, 1, 0],
            ]
        ),
    )
    print(outputs.logits)


def use_model():
    checkpoint = 'distilbert-base-uncased-finetuned-sst-2-english'
    tokenizer = AutoTokenizer.from_pretrained(checkpoint)
    model = AutoModelForSequenceClassification.from_pretrained(checkpoint)

    sequences = [
        "I've been waiting for a HuggingFace course my whole life.",
        "My dog Bella wrote a book, and is also the CEO of a Fortune-500 company.",
    ]

    input_tensors = tokenizer(sequences, padding=True, return_tensors='pt')
    outputs = model(input_tensors.input_ids, attention_mask=input_tensors.attention_mask)
    print(outputs.logits)


if __name__ == '__main__':
    # padding_and_masks()
    use_model()
