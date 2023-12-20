from datasets import load_dataset
import evaluate
import numpy as np
from transformers import (
    AutoTokenizer,
    TrainingArguments,
    AutoModelForSequenceClassification,
    Trainer,
    EvalPrediction,
)
from typing import cast


def compute_metrics(predictions: EvalPrediction) -> dict:
    metric = evaluate.load("glue", "mrpc")
    prediction_labels = np.argmax(predictions.predictions, axis=1)
    return cast(
        dict,
        metric.compute(predictions=prediction_labels, references=predictions.label_ids)
    )


if __name__ == "__main__":
    checkpoint = "bert-base-uncased"
    tokenizer = AutoTokenizer.from_pretrained(checkpoint)
    model = AutoModelForSequenceClassification.from_pretrained(checkpoint, num_labels=2)

    raw_datasets = load_dataset("glue", "mrpc")
    tokenized_datasets = raw_datasets.map(
        lambda examples: tokenizer(
            examples["sentence1"],
            examples["sentence2"],
            truncation=True,
        ),
        batched=True,
    )

    trainer = Trainer(
        model=model,
        args=TrainingArguments(
            "huggingface_push_to_hub_tutorial",
            evaluation_strategy="epoch",
            push_to_hub=True,
        ),
        train_dataset=tokenized_datasets["train"],
        eval_dataset=tokenized_datasets["validation"],
        tokenizer=tokenizer,
        compute_metrics=compute_metrics,
    )
    trainer.train()
    trainer.push_to_hub()

    predictions = trainer.predict(tokenized_datasets["validation"])
    prediction_metrics = compute_metrics(predictions)
    print(prediction_metrics)
