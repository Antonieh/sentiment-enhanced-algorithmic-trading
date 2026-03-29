from typing import Dict, List


def scores_to_dict(model_output: List[Dict]) -> Dict[str, float]:
    """
    Convert Hugging Face pipeline output into a clean probability dict.
    Expected labels: positive, negative, neutral
    """
    prob_dict = {"positive": 0.0, "negative": 0.0, "neutral": 0.0}

    for item in model_output:
        label = item["label"].lower()
        score = float(item["score"])
        prob_dict[label] = score

    return prob_dict


def article_sentiment_score(prob_dict: Dict[str, float]) -> float:
    """
    Article-level score:
    s = p_pos - p_neg
    """
    return prob_dict["positive"] - prob_dict["negative"]