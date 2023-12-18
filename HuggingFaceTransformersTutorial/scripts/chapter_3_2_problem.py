from datasets import load_dataset
from transformers import AutoModelForSequenceClassification, AutoTokenizer, DataCollatorWithPadding


if __name__ == "__main__":
    dataset = load_dataset("glue", "sst2")
    checkpoint = "bert-base-uncased"
    tokenizer = AutoTokenizer.from_pretrained(checkpoint)
    model = AutoModelForSequenceClassification.from_pretrained(checkpoint)

    tokenized_dataset = dataset.map(
        lambda example: tokenizer(
            example["sentence"],
            truncation=True,
        ),
        batched=True,
    )
    batch_size = 8
    sample_batch = tokenized_dataset["train"][:batch_size]

    data_collator = DataCollatorWithPadding(tokenizer=tokenizer)
    cleaned_sample_batch = {
        key: value
        for key, value in sample_batch.items()
        if key not in ["idx", "sentence"]
    }
    collated_batch = data_collator(cleaned_sample_batch)
    print(collated_batch.keys())
    print(collated_batch.input_ids.shape)
    print(collated_batch.attention_mask.shape)
    print(collated_batch.token_type_ids.shape)
    print(collated_batch.labels.shape)
