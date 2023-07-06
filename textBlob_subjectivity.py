import pandas as pd
from textblob import TextBlob

# Load the CSV file
file_path = 'ChatGPTComments.xlsx'
df = pd.read_excel(file_path)

# Assuming the column containing comments is named 'Text'
comments = df['Text'].astype(str)

# Function to get the subjectivity
def get_subjectivity(text):
    return TextBlob(text).sentiment.subjectivity

# Calculate subjectivity for each comment
subjectivities = []
for comment in comments:
    subjectivity = get_subjectivity(comment)
    subjectivities.append(subjectivity)

# Add subjectivity to the DataFrame
df['subjectivity'] = subjectivities

# Function to categorize subjectivity
def categorize_subjectivity(subjectivity, threshold=0.5):
    if subjectivity >= threshold:
        return 'Subjective'
    else:
        return 'Objective'

# Categorize subjectivity for each comment
df['subjectivity_category'] = df['subjectivity'].apply(categorize_subjectivity)

# Save the DataFrame with subjectivity analysis to a new CSV file
output_file_path = 'textBlob_subjectivity_chatgpt.csv'
df.to_csv(output_file_path, index=False)