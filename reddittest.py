import praw
from config import *



def findDepth(parentId, all_comments, postId):
    """This finds the depth of the comment relative to the original post.
    0 is the original post, 1 it's direct comments etc.
    """
    commentId = parentId
    count = 1
    while commentId != postId:
        for comment in all_comments:
            if comment.id == commentId:
                count += 1
                commentId = comment.parent_id
    return count;


reddit = praw.Reddit(client_id=client,
                     client_secret=secret,
                     user_agent=user)

print(reddit.read_only)

for submission in reddit.subreddit('videos').hot(limit=10):
    print(submission.title)
    all_comments = submission.comments.list()
    for comment in all_comments:
        print (findDepth(comment.parent_id, all_comments, submission.id))
