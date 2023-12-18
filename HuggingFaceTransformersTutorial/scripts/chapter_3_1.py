from datasets import DatasetDict, load_dataset
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification, DataCollatorWithPadding
from typing import cast


def train_model():
    checkpoint = "bert-base-uncased"
    tokenizer = AutoTokenizer.from_pretrained(checkpoint)
    model = AutoModelForSequenceClassification.from_pretrained(checkpoint)
    sequences = [
        "I've been waiting for a HuggingFace course my whole life.",
        "My dog has three PhDs.",
    ]
    batch = tokenizer(sequences, padding=True, truncation=True, return_tensors="pt")

    batch["labels"] = torch.tensor([1, 1])

    optimizer = torch.optim.AdamW(model.parameters())
    loss = model(**batch).loss
    loss.backward()
    optimizer.step()


def paraphrase_dataset():
    raw_datasets = load_dataset("glue", "mrpc")
    print(raw_datasets)
    print(raw_datasets["train"][0])
    print(raw_datasets["train"].features)


def tokenize_datasets():
    checkpoint = "bert-base-uncased"
    tokenizer = AutoTokenizer.from_pretrained(checkpoint)
    raw_datasets = load_dataset("glue", "mrpc")
    tokenized_datasets = raw_datasets.map(
        lambda examples: tokenizer(
            examples["sentence1"],
            examples["sentence2"],
            truncation=True,
            padding=False,  # will pad per-batch later rather than padding to dataset max
        ),
        batched=True,
    )
    print(tokenized_datasets)
    print(tokenized_datasets["train"][0])
    tokens = tokenizer.convert_ids_to_tokens(tokenized_datasets["train"][0]["input_ids"])
    print(tokens)
    return cast(DatasetDict, tokenized_datasets)


def collate_datasets(tokenized_datasets: DatasetDict):
    checkpoint = "bert-base-uncased"
    tokenizer = AutoTokenizer.from_pretrained(checkpoint)
    data_collator = DataCollatorWithPadding(tokenizer=tokenizer)
    sample_batch = tokenized_datasets["train"][:8]
    sample_batch = {
        key: value
        for key, value in sample_batch.items()
        if key not in ["idx", "sentence1", "sentence2"]
    }
    collated_batch = data_collator(sample_batch)
    print(collated_batch.keys())
    print(collated_batch.input_ids.shape)
    print(collated_batch.attention_mask.shape)
    print(collated_batch.token_type_ids.shape)
    print(collated_batch.labels.shape)


if __name__ == "__main__":
    # train_model()
    # paraphrase_dataset()
    tokenized_datasets = tokenize_datasets()
    collate_datasets(tokenized_datasets)
