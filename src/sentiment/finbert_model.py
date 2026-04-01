from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

MODEL_NAME = "ProsusAI/finbert"


def load_finbert_pipeline():
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)

    sentiment_pipeline = pipeline(
        "text-classification",
        model=model,
        tokenizer=tokenizer,
        top_k=None,
    )

    return sentiment_pipeline