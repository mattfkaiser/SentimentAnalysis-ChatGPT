import os
import pandas as pd

# Load the data
data = pd.read_csv(r'G:\SentimentAnalysis-ChatGPT\Vader\vader_polarity_LearnProgramming_negative_only.csv')

# Remove rows with 'nan' in 'Subreddit' column
data = data[data['Subreddit'].notna()]

# Print the number of unique subreddits
print(f'Number of unique subreddits: {len(data["Subreddit"].unique())}')

# Loop over the unique subreddits in the data
for subreddit in data['Subreddit'].unique():
    # Filter the data for the current subreddit
    subreddit_data = data[data['Subreddit'] == subreddit]

    # Print the number of comments in the current subreddit
    print(f'Number of comments in {subreddit}: {len(subreddit_data)}')

    # Create a folder for the subreddit if it doesn't exist
    subdir = os.path.join('LearnProgramming_negative_only_parsed', subreddit)
    if not os.path.exists(subdir):
        os.makedirs(subdir)

    # Loop over the comments in the subreddit
    for i, (_, row) in enumerate(subreddit_data.iterrows()):
        # Create a file for the comment
        filename = os.path.join(subdir, f"{str(i).zfill(4)}.txt")
        with open(filename, 'w', encoding='utf-8') as out_file:
            out_file.write(str(row['Text']))

print("Parsing complete!")
