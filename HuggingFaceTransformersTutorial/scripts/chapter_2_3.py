from transformers import BertConfig, BertModel


def randomly_initialize_model():
    config = BertConfig()
    model = BertModel(config)
    return model


def load_model():
    model = BertModel.from_pretrained("bert-base-cased")
    return model


def save_model(model: BertModel):
    model.save_pretrained("my_local_bert")


if __name__ == "__main__":
    # model = randomly_initialize_model()
    # model = load_model()
    # save_model(model)
