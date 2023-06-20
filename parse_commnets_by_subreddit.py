import os
import pandas as pd

# Load the excel data
data = pd.read_excel('comments.xlsx', engine='openpyxl')

# Loop over the unique subreddits in the data
for subreddit in data['subreddit'].unique():
    # Create a folder for the subreddit if it doesn't exist
    subdir = os.path.join('comments_parsed_', subreddit)
    if not os.path.exists(subdir):
        os.makedirs(subdir)

    # Filter the data for the current subreddit
    subreddit_data = data[data['subreddit'] == subreddit]
    
    # Loop over the comments in the subreddit
    for index, row in subreddit_data.iterrows():
        # Create a file for the comment
        filename = os.path.join(subdir, f"{str(index).zfill(4)}.txt")
        with open(filename, 'w', encoding='utf-8') as out_file:
            out_file.write(row['comment'])

print("Parsing complete!")
