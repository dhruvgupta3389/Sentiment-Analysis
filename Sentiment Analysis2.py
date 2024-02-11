import json
import os
import joblib
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer


#nltk.download('vader_lexicon')

# Initialize the SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()

# Define a mapping of short forms to full sentiments
short_form_mapping = {
    "pos": "positive",
    "neg": "negative",
    "neu": "neutral",
}

# Initialize an empty dictionary to store user feedback
user_feedback = {}

# Load user feedback from the existing file (if the file exists)
try:
    with open("user_feedback.json", "r") as feedback_file:
        user_feedback = json.load(feedback_file)
except FileNotFoundError:
    pass

while True:
    # Prompt the user for input
    text = input("Enter a text for sentiment analysis (or type 'exit' to quit): ")

    if text.lower() == 'exit':
        break  # Exit the loop if the user types 'exit'

    if text in user_feedback:
        # If the text has been corrected before, use the corrected sentiment
        corrected_sentiment = user_feedback[text]
        print(f"Predicted sentiment: {corrected_sentiment} (based on user feedback)")
    else:
        # Perform sentiment analysis using nltk's SentimentIntensityAnalyzer
        sentiment_scores = sia.polarity_scores(text)
        
        # Determine sentiment based on the compound score
        compound_score = sentiment_scores["compound"]
        if compound_score > 0.05:
            predicted_sentiment = "positive"
        elif compound_score < -0.05:
            predicted_sentiment = "negative"
        else:
            predicted_sentiment = "neutral"

        print(f"Predicted sentiment: {predicted_sentiment}")

    # Ask the user for feedback using short forms
    feedback = input("Is the predicted sentiment correct? (yes/no): ").lower()
    
    if feedback == 'no':
        # If the user believes the sentiment is wrong, ask for the correct sentiment using short forms
        correct_sentiment = input("Please provide the correct sentiment (pos/neg/neu): ").lower()
        if correct_sentiment in short_form_mapping:
            # Store the correct sentiment in user feedback for the current run
            user_feedback[text] = short_form_mapping[correct_sentiment]

# Display user feedback from the current session
print("User Feedback from Current Session:")
for text, sentiment in user_feedback.items():
    print(f"Text: {text} - Correct Sentiment: {sentiment}")

# Merge user feedback and save it to the user_feedback file
with open("user_feedback.json", "w") as feedback_file:
    json.dump(user_feedback, feedback_file)
