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


if __name__ == "__main__":
    classifier_pipeline()
