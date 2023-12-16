from rich import print
from transformers import pipeline


def classifier_pipeline():
    classifier = pipeline("sentiment-analysis")
    classification = classifier(
        [
            "I'm so mad at my dog for being so cute.",
            "Happy that summer's over so I can finally cover up my blobby body.",
        ]
    )
    print(classification)


def zero_shot_classification_pipeline():
    classifier = pipeline("zero-shot-classification")
    classification = classifier(
        "Increase your focus with this one simple trick.",
        candidate_labels=["spam", "not spam"],
    )
    print(classification)


def text_generation_pipeline():
    generator = pipeline("text-generation", model="distilgpt2")
    generated_sentences = generator(
        "Bella the dog has decided to celebrate her birthday by doing the thing she loves best, ",
        max_length=50,
        num_return_sequences=5,
    )
    print(generated_sentences)


if __name__ == "__main__":
    # classifier_pipeline()
    # zero_shot_classification_pipeline()
    text_generation_pipeline()
