# Instructions to get set up.
# Install PRAW: https://praw.readthedocs.io/en/v7.7.0/getting_started/quick_start.html
# Save this Python Script to your computer.
# Run this script with the command `python3 gamethreadscraper.py [token]`, where `[token]` is a token you want to search the thread for.
# Modify the script however you like to come up with interesting results.

# Imports
import praw, sys, re

# Setup a Reddit instance. This is a script application setup just for this Tech Challenge. You can create these at https://www.reddit.com/prefs/apps (and feel free to use your own).
reddit = praw.Reddit(
    client_id = "OQ1OsNYqBJ3vMBfJLn_DRQ",
    client_secret = "z5K8adUrqRKKKb7iUsP_4b-AZdKBzw",
    user_agent = "/r/CFB Tech Challenge",
)

# The Georgia - Ohio State Semifinal
submission = reddit.submission(id = '100cbyw')

# Expand some initially hidden comments. The limit means that at most 10 comment threads will be expanded. May take a minute.
submission.comments.replace_more(limit = 5)

# Flatten the comments from a tree into a list. Expanding and flattening will give us ~1500 comments to work with.
comments = submission.comments.list()

# Fetch the token you provided in the command line.
token = str(sys.argv[1])

# Get team from flair by taking substring in between ::
def flair_print(string):
    start = string.find(':')
    end = string[(start+1):].find(':')
    return end, string[(start+1):(end+1)]

# Create our mostly empty Dict
Dict = {'flairless': 0}

# We will remove the # from any flair, so michigan, michigan2, michigan3, etc. will all simply increment "michigan"
# Here is our regex pattern to find numbers to remove
pattern = r'[0-9]'

# Iterate through the comments and do something on each one.
for comment in comments:
  try:
    # Get the author flair of the comment.
    comment_flair = comment.author_flair_text
    # Check for number of flairs in comment by counting ':' character
    count = comment_flair.count(':')
    # If there is no flair, we increment "flairless"
    if count == 0:
        num = Dict.get('flairless')
        Dict['flairless'] = num+1
    # If there is 1 flair, we take the values between :: and add them to our Dict
    if count == 2:
        end1, flair1 = flair_print(comment_flair)
        if flair1.isalpha() != True:
            flair1 = re.sub(pattern,'',flair1)
            print(flair1)
        if flair1 in Dict.keys():
            num = Dict.get(flair1)
            Dict[flair1] = (num+1)
        else:
            Dict[flair1] = 1
    # If there are 2 flairs, we take the values between :: for the first flair, increment past it
    # Then we capture the text between :: for the second flair
    if count == 4:
        end1, flair1 = flair_print(comment_flair)
        if flair1.isalpha() != True:
            flair1 = re.sub(pattern,'',flair1)
            print(flair1)
        if flair1 in Dict.keys():
            num = Dict.get(flair1)
            Dict[flair1] = (num+1)
        else:
            Dict[flair1] = 1
        end2, flair2 = flair_print(comment_flair[(end+2):])
        if flair2.isalpha() != True:
            flair2 = re.sub(pattern,'',flair2)
            print(flair2)
        num = Dict.get(flair2)
        if flair2 in Dict.keys():
            num = Dict.get(flair2)
            Dict[flair2] = (num+1)
        else:
            Dict[flair2] = 1
  except: pass

# finally we sort our Dict in descending order based on the number of comments then print it
Dict = dict(sorted(Dict.items(), key=lambda x:x[1], reverse = True))
print(Dict)
