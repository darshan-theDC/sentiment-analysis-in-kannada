import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

MODEL_PATH = r"sentiment_analysis_in_kannada\xlm_roberta_sentiment_model"
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class SentimentModel:
    """
    A class for handling sentiment analysis using a pre-trained model.
    """

    def __init__(self, model_path=MODEL_PATH):
        """
        Initialize the model and tokenizer.
        """
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_path)
        self.model.to(DEVICE)
        self.model.eval()

    def predict_sentiment(self, text):
        """
        Predict sentiment of the given text.
        Args:
            text (str): Input text for sentiment analysis.

        Returns:
            str: Sentiment ('Positive' or 'Negative').
        """
        inputs = self.tokenizer(
            text, return_tensors="pt", truncation=True, padding=True, max_length=512
        )
        inputs = {key: value.to(DEVICE) for key, value in inputs.items()}

        with torch.no_grad():
            outputs = self.model(**inputs)
            scores = outputs.logits.softmax(dim=-1)

        negative_score, positive_score = scores[0].tolist()
        sentiment = "Positive" if positive_score > negative_score else "Negative"
        return sentiment