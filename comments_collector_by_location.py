import praw
import datetime as dt
import csv

reddit = praw.Reddit(
    client_id="SLKaJnEY-edqw82COgS6QA",
    client_secret="qTiNGh980kZhuyIrV4boyL_DE3I_ww",
    user_agent="windows:GPTCSResearch:1.0 (by /u/GPTCSResearch)",
)

sub = reddit.subreddit('all')

keywords = ['chatGPT', 'chat GPT']

# Set the location for the search query
location = 'Indianapolis'

# Construct the search query by concatenating the location with the keywords
search_query = f'{keywords} location:{location}'

start_date = dt.datetime(2022, 11, 1)
end_date = dt.datetime(2023, 3, 17)

posts = sub.search(keywords, limit=None)


# Process a single comment to check for keywords and write to files if found
def process_comment(comment):
    # Check if comment falls within the specified date range
    if start_date.timestamp() < comment.created_utc < end_date.timestamp():
        # Iterate over the keywords list
        for kw in keywords:
            # Check if the keyword is present in the comment's body (case-insensitive)
            if kw.lower() in comment.body.lower():
                # Set the author name to 'Deleted' if the author is None (e.g., deleted account)
                author_name = 'Deleted' if comment.author is None else comment.author.name
                # Write the comment data to the TXT file
                with open('comments.txt', mode='a', encoding='utf-8') as file:
                    file.write(f'Comment ID: {comment.id}\n')
                    file.write(f'Score: {comment.score}\n')
                    file.write(f'Author: {author_name}\n')
                    file.write(f'Created: {dt.datetime.fromtimestamp(comment.created_utc)}\n')
                    file.write(f'Text: {comment.body}\n\n')

                # Write the comment data to the CSV file
                with open('comments.csv', mode='a', encoding='utf-8', newline='') as csvfile:
                    csv_writer = csv.writer(csvfile)
                    csv_writer.writerow(
                        [comment.id, comment.score, author_name, dt.datetime.fromtimestamp(comment.created_utc),
                         comment.body])
                # Exit the loop when a keyword is found
                break


def process_comments(comments):
    for comment in comments:
        if isinstance(comment, praw.models.MoreComments):
            continue

        process_comment(comment)
        if comment.replies:
            process_comments(comment.replies)


with open('comments_by_location.csv', mode='w', encoding='utf-8', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    # write the header row
    csv_writer.writerow(['Comment ID', 'Score', 'Author', 'Created', 'Text'])

# Initialize the post_count variable and set the max_posts limit
post_count = 0
max_posts = 100  # Change this value to the desired number of posts

# Iterate through the posts and process their comments
for post in posts:
    process_comments(post.comments)
    post_count += 1
    if post_count >= max_posts:
        break
