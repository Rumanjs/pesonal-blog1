"""
ai_utils.py — AI / ML Utility Functions
-----------------------------------------
This module provides two Natural Language Processing (NLP) features:

1. **Sentiment Analysis** (using TextBlob)
   - Computes a polarity score from -1.0 (very negative) to +1.0 (very positive).
   - Maps the score to a human-readable label: Positive, Negative, or Neutral.

2. **Keyword Extraction** (using RAKE — Rapid Automatic Keyword Extraction)
   - Identifies the most important multi-word phrases from the text.
   - Returns the top-5 keywords ranked by relevance score.

How it works:
─────────────
• TextBlob wraps the Pattern library and uses a pre-trained sentiment lexicon
  to assign polarity scores to words, then averages them over the entire text.
• RAKE splits the text at stopwords and punctuation, builds a word co-occurrence
  matrix, and scores each candidate phrase by the sum of word degree / frequency.

These lightweight techniques require no model training and work out of the box,
making them ideal for educational projects and quick prototyping.
"""

from textblob import TextBlob
from rake_nltk import Rake


# ── Sentiment Analysis ─────────────────────────────────────────────────────


def analyze_sentiment(text: str) -> tuple:
    """
    Analyze the sentiment of the given text.

    Args:
        text (str): The blog post content to analyze.

    Returns:
        tuple: (label, score)
            - label (str): 'Positive', 'Negative', or 'Neutral'
            - score (float): Polarity score between -1.0 and 1.0

    Example:
        >>> analyze_sentiment("I love machine learning!")
        ('Positive', 0.5)
    """
    # Create a TextBlob object from the input text
    blob = TextBlob(text)

    # Extract the polarity score (ranges from -1.0 to +1.0)
    polarity = round(blob.sentiment.polarity, 4)

    # Map the numerical score to a readable label
    if polarity > 0.1:
        label = "Positive"
    elif polarity < -0.1:
        label = "Negative"
    else:
        label = "Neutral"

    return label, polarity


# ── Keyword Extraction ─────────────────────────────────────────────────────


def extract_keywords(text: str, top_n: int = 5) -> list:
    """
    Extract the top-N keywords / key-phrases from the given text using RAKE.

    Args:
        text (str): The blog post content to process.
        top_n (int): Number of top keywords to return (default: 5).

    Returns:
        list[str]: A list of the most relevant keywords / phrases.

    Example:
        >>> extract_keywords("Deep learning models use neural networks for classification.")
        ['deep learning models', 'neural networks', 'classification']
    """
    # Initialize RAKE with default English stopwords
    rake = Rake()

    # Feed the text to the RAKE algorithm
    rake.extract_keywords_from_text(text)

    # Get ranked phrases (highest score first)
    ranked_phrases = rake.get_ranked_phrases()

    # Return only the top N phrases
    return ranked_phrases[:top_n]
