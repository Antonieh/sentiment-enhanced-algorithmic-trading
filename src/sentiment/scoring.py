from typing import Dict, List


LABEL_MAP = {
    "positive": "p_positive",
    "negative": "p_negative",
    "neutral": "p_neutral",
}


def scores_to_dict(model_output: List[Dict]) -> Dict[str, float]:
    """
    Convert FinBERT pipelines output into a standardized probability dictionary.
    Expected labels: positive, negative, neutral
    """
    result = {
        "p_positive": 0.0,
        "p_negative": 0.0,
        "p_neutral": 0.0,
    }

    for item in model_output:
        label = item["label"].lower()
        score = float(item["score"])

        if label in LABEL_MAP:
            result[LABEL_MAP[label]] = score

    return result


def article_sentiment_score(probabilities: Dict[str, float]) -> float:
    """
    Continuous article-level sentiment score in [-1, 1].
    """
    return probabilities["p_positive"] - probabilities["p_negative"]


def article_confidence(probabilities: Dict[str, float]) -> float:
    """
    Confidence is the highest class probability.
    """
    return max(
        probabilities["p_positive"],
        probabilities["p_negative"],
        probabilities["p_neutral"],
    )