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

# Function to get the sentiment compound score
def get_sentiment_compound(text):
    return sia.polarity_scores(text)['compound']

# Calculate sentiment compound score for each comment
sentiments = []
for comment in comments:
    sentiment = get_sentiment_compound(comment)
    sentiments.append(sentiment)

# Add sentiment compound score to the DataFrame
df['sentiment_compound'] = sentiments

# Function to categorize sentiment
def categorize_sentiment(compound):
    if compound > 0.25:
        return 'Positive'
    elif compound < -0.25:
        return 'Negative'
    else:
        return 'Neutral'

# Categorize sentiment for each comment
df['sentiment'] = df['sentiment_compound'].apply(categorize_sentiment)

# Save the DataFrame with sentiment analysis to a new CSV file
output_file_path = 'vader_polarity_neutral_25.csv'
df.to_csv(output_file_path, index=False)
