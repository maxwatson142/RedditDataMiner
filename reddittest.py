import praw
import csv
from config import *


def findDepth(parentId, all_comments, postId):
    """This finds the depth of the comment relative to the original post.
    0 is the original post, 1 it's direct comments etc.
    """
    commentId = parentId
    count = 1
    "Post id's when referenced from other objects start with the prefix t3_"
    while not(commentId.startswith('t3_')):
        for comment in all_comments:
            if comment.id in commentId:
                count += 1
                commentId = comment.parent_id
    return count;

def findParentBody(parentId, all_comments):
    for comment in all_comments:
        if comment.id in parentId:
            return comment.body
    return null

reddit = praw.Reddit(client_id=client,
                     client_secret=secret,
                     user_agent=user)

print(reddit.read_only)
subcount = 0
commentcount = 0
with open('test.txt', mode='w') as reddit_file:
    reddit_writer = csv.writer(reddit_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for submission in reddit.subreddit('videos').hot(limit=10):
        "initialize variables for writing the post"
        title = submission.title
        depth = 0
        body = submission.selftext
        parent_body = ""
        post_body = ""
        subreddit = submission.subreddit
        time = submission.created_utc
        reddit_writer.writerow([title,depth,body,parent_body,post_body,subreddit,time])
        "Initialize variables for writing comments"
        post_body = submission.selftext
        title = ""
        submission.comments.replace_more()
        all_comments = submission.comments.list()
        for comment in all_comments:
            body = comment.body
            depth = findDepth(comment.parent_id, all_comments, submission.id)
            if depth > 1:
                parent_body = findParentBody(comment.parent_id, all_comments)
            else:
                parent_body = post_body
            time = comment.created_utc
            reddit_writer.writerow([title,depth,body,parent_body,post_body,subreddit,time])
        subcount +=1
        commentcount += len(all_comments)
        print (subcount),
        print(" Posts collected with "),
        print(commentcount),
        print(" comments.")
