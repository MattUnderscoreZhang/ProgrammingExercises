import torch
from transformers import AutoTokenizer, AutoModel, AutoModelForSequenceClassification


def tokenize():
    checkpoint = "distilbert-base-uncased-finetuned-sst-2-english"
    tokenizer = AutoTokenizer.from_pretrained(checkpoint)
    text = [
        "I enjoy taking long walks along the beach with my dog.",
        "我非常爱我的狗。",
    ]
    tokens = tokenizer(text, padding=True, truncation=True, return_tensors="pt")
    print(tokens)
    token_strs = tokenizer.tokenize(text, return_tensors="pt")
    print(token_strs)
    return tokens


def model(tokens: torch.Tensor):
    checkpoint = "distilbert-base-uncased-finetuned-sst-2-english"
    model = AutoModel.from_pretrained(checkpoint)
    outputs = model(**tokens)
    print(outputs.last_hidden_state.shape)


def classification_model(tokens: torch.Tensor):
    checkpoint = "distilbert-base-uncased-finetuned-sst-2-english"
    model = AutoModelForSequenceClassification.from_pretrained(checkpoint)
    outputs = model(**tokens)
    print(outputs.logits.shape)
    print(model.config.id2label)
    return outputs


def torch_predictions(outputs):
    predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
    print(predictions)


if __name__ == "__main__":
    tokens = tokenize()
    model(tokens)
    outputs = classification_model(tokens)
    torch_predictions(outputs)
