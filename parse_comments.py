import os

# Create the output directory if it doesn't exist
if not os.path.exists('comments_parsed'):
    os.makedirs('comments_parsed')

# Define a counter for file names
file_counter = 1

# Initialize an empty list to store comments
comments = []

# Define a counter for comments
comment_counter = 0

# Read the text file
with open('comments_text_only.txt', 'r', encoding='utf-8') as f:
    for line in f:
        # If the line is not blank, add it to the current comment
        if line.strip():
            comments.append(line.strip())
        # If the line is blank and there's a comment, increment the comment counter
        elif comments:
            comment_counter += 1
            comments.append("\n")  # Add a newline to separate comments
            # If we've processed 1000 comments, save them to a new file
            if comment_counter == 1000:
                with open(f'comments_parsed/{str(file_counter).zfill(4)}.txt', 'w', encoding='utf-8') as out_file:
                    out_file.write("\n".join(comments))
                # Reset the comment and file counter
                comments = []
                comment_counter = 0
                file_counter += 1
    # Save the last batch of comments if they exist
    if comments:
        with open(f'comments_parsed/{str(file_counter).zfill(4)}.txt', 'w', encoding='utf-8') as out_file:
            out_file.write("\n".join(comments))

print("Parsing complete!")
