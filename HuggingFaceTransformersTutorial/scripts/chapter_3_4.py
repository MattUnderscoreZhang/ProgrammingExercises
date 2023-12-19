from accelerate import Accelerator, notebook_launcher
from datasets import load_dataset
import evaluate
import torch
from torch.optim import AdamW
from torch.utils.data import DataLoader
from tqdm.auto import tqdm
from transformers import (
    AutoTokenizer,
    DataCollatorWithPadding,
    AutoModelForSequenceClassification,
    get_scheduler,
)


def train():
    checkpoint = "bert-base-uncased"
    tokenizer = AutoTokenizer.from_pretrained(checkpoint)
    data_collator = DataCollatorWithPadding(tokenizer=tokenizer)
    model = AutoModelForSequenceClassification.from_pretrained(checkpoint, num_labels=2)
    accelerator = Accelerator()

    raw_datasets = load_dataset("glue", "mrpc")
    metric = evaluate.load("glue", "mrpc")

    tokenized_datasets = raw_datasets.map(
        lambda examples: tokenizer(
            examples["sentence1"],
            examples["sentence2"],
            truncation=True,
        ),
        batched=True,
    )
    tokenized_datasets = tokenized_datasets.remove_columns(
        ["sentence1", "sentence2", "idx"]
    )
    tokenized_datasets = tokenized_datasets.rename_column("label", "labels")
    tokenized_datasets.set_format("torch")

    train_dataloader = DataLoader(
        tokenized_datasets["train"],
        shuffle=True,
        batch_size=8,
        collate_fn=data_collator,
    )
    eval_dataloader = DataLoader(
        tokenized_datasets["validation"],
        batch_size=8,
        collate_fn=data_collator,
    )
    optimizer = AdamW(model.parameters(), lr=5e-5)
    train_dataloader, eval_dataloader, model, optimizer = accelerator.prepare(
        train_dataloader, eval_dataloader, model, optimizer,
    )

    n_epochs = 3
    n_training_steps = n_epochs * len(train_dataloader)
    lr_scheduler = get_scheduler(
        "linear",
        optimizer=optimizer,
        num_warmup_steps=0,
        num_training_steps=n_training_steps,
    )
    progress_bar = tqdm(range(n_training_steps))

    model.train()
    for _ in range(n_epochs):
        for batch in train_dataloader:
            predictions = model(**batch)
            loss = predictions.loss
            accelerator.backward(loss)

            optimizer.step()
            lr_scheduler.step()
            optimizer.zero_grad()
            progress_bar.update(1)

    model.eval()
    for batch in eval_dataloader:
        with torch.no_grad():
            predictions = model(**batch)

        logits = predictions.logits
        predictions = torch.argmax(logits, dim=-1)
        metric.add_batch(predictions=predictions, references=batch["labels"])
    prediction_metrics = metric.compute()
    print(prediction_metrics)


if __name__ == "__main__":
    notebook_launcher(train)
