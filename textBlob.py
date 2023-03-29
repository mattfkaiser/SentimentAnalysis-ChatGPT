import pandas as pd
from textblob import TextBlob

# Load the CSV file
file_path = 'comments.csv'
df = pd.read_csv(file_path)

# Assuming the column containing comments is named 'Text'
comments = df['Text'].astype(str)


# Function to get the sentiment polarity
def get_sentiment_polarity(text):
    return TextBlob(text).sentiment.polarity


# Calculate sentiment polarity for each comment
sentiments = []
for comment in comments:
    sentiment = get_sentiment_polarity(comment)
    sentiments.append(sentiment)

# Add sentiment polarity to the DataFrame
df['sentiment_polarity'] = sentiments


# Function to categorize sentiment
def categorize_sentiment(polarity):
    if polarity > 0.00:
        return 'Positive'
    elif polarity < -0.00:
        return 'Negative'
    else:
        return 'Neutral'


# Categorize sentiment for each comment
df['sentiment'] = df['sentiment_polarity'].apply(categorize_sentiment)

# Save the DataFrame with sentiment analysis to a new CSV file
output_file_path = 'reddit_comments_with_sentiments_neutral_0.csv'
df.to_csv(output_file_path, index=False)
