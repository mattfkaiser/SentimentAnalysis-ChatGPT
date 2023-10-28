import pandas as pd
import datetime

# Initialize positive and negative counts for each month for each file and for all files
months = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
pos_counts = {month: 0 for month in months}
neg_counts = {month: 0 for month in months}
total_pos_counts = {month: 0 for month in months}
total_neg_counts = {month: 0 for month in months}

# Loop through each of the 4 files
for filename in ["vader_pos_neg_ChatGPT.xlsx", "vader_pos_neg_LearnMachineLearning.xlsx", "vader_pos_neg_LearnProgramming.xlsx", "vader_pos_neg_Technology.xlsx"]:
    # Print the filename being processed
    print(f"Processing {filename}...")
    
    # Read in the comment IDs and their corresponding sentiment scores from the first sheet
    df = pd.read_excel(f"G:\SentimentAnalysis-ChatGPT\{filename}", sheet_name=1)
    file_comment_ids = df["Comment ID"]
    sentiment_scores = df["sentiment"]
    
    # Initialize positive and negative counts for each month for the current file
    file_pos_counts = {month: 0 for month in months}
    file_neg_counts = {month: 0 for month in months}
    
    # Loop through each comment ID in the current file
    for comment_id in df["Comment ID"]:
        # Print the comment ID being processed
        print(f"Processing comment ID {comment_id}...")
        
        # Get the created date for the comment
        created_date_str = df.loc[df["Comment ID"] == comment_id, "Created"]
        if not created_date_str.empty:
            created_date_str = created_date_str.iloc[0].strftime("%m/%d/%Y %H:%M")
        else:
            print(f"Skipping comment ID {comment_id} because the created date is missing...")
            continue  # Skip this comment if the created date is missing
        
        # Parse the created date string into a datetime object
        created_date = datetime.datetime.strptime(created_date_str, "%m/%d/%Y %H:%M")
        
        # Extract the month from the created date
        month = created_date.strftime("%m")
        
        # Check if the comment ID is in the current file
        if comment_id in file_comment_ids.values:
            # Get the sentiment score for the comment
            sentiment_score_str = sentiment_scores[file_comment_ids == comment_id].iloc[0]

            # Check if the sentiment score is 'Positive' or 'Negative'
            if sentiment_score_str == 'Positive':
                file_pos_counts[month] += 1
                total_pos_counts[month] += 1
            elif sentiment_score_str == 'Negative':
                file_neg_counts[month] += 1
                total_neg_counts[month] += 1
            else:
                print(f"Skipping comment ID {comment_id} because the sentiment score is not 'Positive' or 'Negative'...")
                continue  # Skip this comment if the sentiment score is not 'Positive' or 'Negative'
        else:
            print(f"Skipping comment ID {comment_id} because it is not in the current file...")
    
    # Create a new DataFrame with columns for each month of the year and rows for the positive and negative counts for the current file
    file_sentiment_counts = pd.DataFrame({"Month": months, "Positive": [file_pos_counts[month] for month in months], "Negative": [file_neg_counts[month] for month in months]})
    
    # Write the DataFrame to a new CSV file with the same name as the current file, but with "_counts" appended before the file extension
    file_sentiment_counts.to_csv(f"{filename.split('.')[0]}_counts.csv", index=False)

# Create a new DataFrame with columns for each month of the year and rows for the total positive and negative counts for all files
total_sentiment_counts = pd.DataFrame({"Month": months, "Positive": [total_pos_counts[month] for month in months], "Negative": [total_neg_counts[month] for month in months]})

# Write the DataFrame to a new CSV file called "total_sentiment_counts.csv"
total_sentiment_counts.to_csv("total_sentiment_counts.csv", index=False)