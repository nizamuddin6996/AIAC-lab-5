def simple_sentiment_analysis():
    """
    Reads a review from the keyboard and outputs whether it is a Positive or Negative review.
    If positive and negative cues are tied or absent, resolves in favor of Positive when ties,
    otherwise Negative when no cues detected.
    """
    positive_words = {"good", "great", "excellent", "happy", "love", "wonderful", "positive", "amazing", "fantastic", "enjoyed", "liked", "best"}
    negative_words = {"bad", "terrible", "poor", "sad", "hate", "awful", "negative", "worst", "boring", "dislike", "disappointed", "horrible"}

    review = input("Type your review and press Enter: ").strip()
    words = set(word.strip(".,!?").lower() for word in review.split())

    pos_count = len(words & positive_words)
    neg_count = len(words & negative_words)

    if pos_count == 0 and neg_count == 0:
        print("The review is Negative.")
    elif pos_count >= neg_count:
        print("The review is Positive.")
    else:
        print("The review is Negative.")

if __name__ == "__main__":
    simple_sentiment_analysis()
