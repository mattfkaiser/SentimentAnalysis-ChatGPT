import praw
import datetime as dt
import csv

reddit = praw.Reddit(
    client_id="SLKaJnEY-edqw82COgS6QA",
    client_secret="qTiNGh980kZhuyIrV4boyL_DE3I_ww",
    user_agent="windows:GPTCSResearch:1.0 (by /u/GPTCSResearch)",
)

subreddit_list = ['artificial', 'deeplearning', 'ChatGPT', 'computerscience', 'learnprogramming', 'learnmachinelearning', 'technology', 'LLM', 'ChatGPTCoding', 'ArtificialInteligence']

total_comments = 0
comments_per_subreddit = {}

start_date = dt.datetime(2022, 11, 1)
end_date = dt.datetime(2023, 6, 18)

keywords = ['chatGPT', 'chat GPT']

# Process a single comment to check for keywords and write to files if found
def process_comment(comment):
    global total_comments
    global comments_per_subreddit
    # Check if comment falls within the specified date range
    if start_date.timestamp() < comment.created_utc < end_date.timestamp():
        # Iterate over the keywords list
        for kw in keywords:
            # Check if the keyword is present in the comment's body (case-insensitive)
            if kw.lower() in comment.body.lower():
                # Set the author name to 'Deleted' if the author is None (e.g., deleted account)
                author_name = 'Deleted' if comment.author is None else comment.author.name

                # Write the comment data to the CSV file
                with open('comments_narrow_11_1_22_present.csv', mode='a', encoding='utf-8', newline='') as csvfile:
                    csv_writer = csv.writer(csvfile)
                    csv_writer.writerow(
                        [comment.id, comment.score, author_name, dt.datetime.fromtimestamp(comment.created_utc),
                         comment.body, comment.subreddit.display_name])  # Add subreddit name
                    
                                    # Update the counters
                total_comments += 1
                comments_per_subreddit[comment.subreddit.display_name] = comments_per_subreddit.get(comment.subreddit.display_name, 0) + 1
                
                # Exit the loop when a keyword is found
                break

# Process a list of comments to check for keywords and write to files if found
def process_comments(comments):
    global total_comments
    global comments_per_subreddit
    for comment in comments:
        if isinstance(comment, praw.models.MoreComments):
            continue

        # Check if comment falls within the specified date range
        if start_date.timestamp() < comment.created_utc < end_date.timestamp():
            # Iterate over the keywords list
            for kw in keywords:
                # Check if the keyword is present in the comment's body (case-insensitive)
                if kw.lower() in comment.body.lower():
                    print(f'Found relevant comment: {comment.id}')  # New print statement

        process_comment(comment)
        if comment.replies:
            process_comments(comment.replies)  # Calling process_comments instead of process_comment


# Create the CSV file and write the header row
with open('comments_narrow_11_1_22_present.csv', mode='w', encoding='utf-8', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    # write the header row
    csv_writer.writerow(['Comment ID', 'Score', 'Author', 'Created', 'Text', 'Subreddit'])  # Add 'Subreddit'

# Initialize the max_posts limit
max_posts_per_subreddit = 100  # Change this value to the desired number of posts per subreddit

# Iterate through the list of subreddits
for sub_name in subreddit_list:
    print(f'Starting to search subreddit: {sub_name}')  # New print statement
    sub = reddit.subreddit(sub_name)

    # Search posts within the subreddit
    posts = sub.search(keywords, limit=None)
    
    post_count = 0  # Initialize the post count for this subreddit

    # Iterate through the posts and process their comments
    for post in posts:
        print(f'Processing post: {post.title}')  # New print statement
        process_comments(post.comments)
        post_count += 1
        if post_count >= max_posts_per_subreddit:
            break  # Break when we've reached the max posts for this subreddit

# Write the total comments and comments per subreddit to the CSV file
with open('comments_narrow_11_1_22_present.csv', mode='a', encoding='utf-8', newline='') as csvfile:
    total_comments
    comments_per_subreddit
    csv_writer = csv.writer(csvfile)

    # Write total comments to the CSV file
    csv_writer.writerow(["Total comments:", total_comments])

    # Write comments per subreddit to the CSV file
    csv_writer.writerow(["Comments per subreddit:"])
    for subreddit, comment_count in comments_per_subreddit.items():
        csv_writer.writerow([subreddit, comment_count])
