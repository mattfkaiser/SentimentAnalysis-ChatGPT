# Program that uses NRCLex to rate emotions associated with comments in comments.csv

import pandas as pd
import nltk
from nrclex import NRCLex

# Load the CSV file
file_path = 'G:\SentimentAnalysis-ChatGPT\LearnProgrammingComments.xlsx'
df = pd.read_excel(file_path)

# Assuming the column containing comments is named 'Text'
comments = df['Text'].astype(str)

# Function to get the emotion ratings
def get_emotion_ratings(text):
    return NRCLex(text).affect_frequencies

# Calculate emotion ratings for each comment
emotions = []
for comment in comments:
    emotion = get_emotion_ratings(comment)
    emotions.append(emotion)

# Add emotion ratings to the DataFrame
df['emotions'] = emotions

# Save the DataFrame with emotion ratings to a new CSV file
output_file_path = 'nrc_emotions_LearnProgramming.csv'
df.to_csv(output_file_path, index=False)

# Function to categorize emotion
def categorize_emotion(emotions):
    if emotions['positive'] > emotions['negative']:
        return 'Positive'
    elif emotions['positive'] < emotions['negative']:
        return 'Negative'
    else:
        return 'Neutral'
    
# Categorize emotion for each comment
df['emotion'] = df['emotions'].apply(categorize_emotion)

# Save the DataFrame with emotion analysis to a new CSV file
output_file_path = 'nrc_emotions_categorized_LearnProgramming.csv'
df.to_csv(output_file_path, index=False)

# Function to get the top emotion
def get_top_emotion(emotions):
    return max(emotions, key=emotions.get)

# Get the top emotion for each comment
df['top_emotion'] = df['emotions'].apply(get_top_emotion)

# Save the DataFrame with emotion analysis to a new CSV file
output_file_path = 'nrc_emotions_top_LearnProgramming.csv'
df.to_csv(output_file_path, index=False)
