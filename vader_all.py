import pandas as pd
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

nltk.download('vader_lexicon')

# Load the CSV file
file_path = 'comments.csv'
df = pd.read_csv(file_path)

# Assuming the column containing comments is named 'Text'
comments = df['Text'].astype(str)

# Initialize the VADER sentiment intensity analyzer
sia = SentimentIntensityAnalyzer()

# Function to get the sentiment scores
def get_sentiment_scores(text):
    return sia.polarity_scores(text)

# Calculate sentiment scores for each comment
sentiments = [get_sentiment_scores(comment) for comment in comments]

# Add sentiment scores to the DataFrame
df['sentiment_positive'] = [sentiment['pos'] for sentiment in sentiments]
df['sentiment_neutral'] = [sentiment['neu'] for sentiment in sentiments]
df['sentiment_negative'] = [sentiment['neg'] for sentiment in sentiments]
df['sentiment_compound'] = [sentiment['compound'] for sentiment in sentiments]

# Function to categorize sentiment
def categorize_sentiment(compound):
    if compound > 0.1:
        return 'Positive'
    elif compound < -0.1:
        return 'Negative'
    else:
        return 'Neutral'

# Categorize sentiment for each comment
df['sentiment'] = df['sentiment_compound'].apply(categorize_sentiment)

# Save the DataFrame with sentiment analysis to a new CSV file
output_file_path = 'vader_polarity_1.csv'
df.to_csv(output_file_path, index=False)
