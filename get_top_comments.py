import codecs
import argparse
import json
import praw
from get_all_posts import get_all_posts

def comment_details_json(comment):
    return json.dumps({
        "id": unicode(comment.id),
        "link_id": unicode(comment.link_id),
        "created": comment.created,
        "ups": comment.ups,
        "downs": comment.downs,
        "score": comment.score,
        "author": unicode(comment.author),
        "body": unicode(comment.body),
        "permalink": unicode(comment.permalink)
        })

def post_details_json(post):
    return json.dumps({
        "id": unicode(post.id),
        "name": unicode(post.name),
        "created": post.created,
        "ups": post.ups,
        "downs": post.downs,
        "score": post.score,
        "author": unicode(post.author),
        "title": unicode(post.title),
        "selftext": unicode(post.selftext),
        "url": unicode(post.url),
        "permalink": unicode(post.permalink)
        })

def main():
    parser = argparse.ArgumentParser(description='Get top comments in subreddit from all time')
    parser.add_argument("--subreddit", dest="subreddit", required=True)          # e.g. SketchDaily
    parser.add_argument("--maxtop", dest="maxtop", required=False, default=1000) # maximum top count
    parser.add_argument("--minups", dest="minups", required=False, default=0)    # minimum 'ups' threshold
    args = parser.parse_args()

    post_cache = {}
    top_comments = []
    threshold = int(args.minups)
    maxcomments = int(args.maxtop)

    print '{"section": "--- ALL POSTS (/top + /new + /search) ---"}' # TODO: codecs.BOM_UTF8 ??

    # use generator to get all posts
    for post in get_all_posts(args.subreddit):
        if isinstance(post, praw.models.reddit.submission.Submission) and post.name not in post_cache:
            post_cache[ post.name ] = post
            print post_details_json( post )
            for comment in post.comments: # use praw.helpers.flatten_tree(post.comments) to also process sub-level comments
                # must be comment (not a readmore node)
                # must be above upvote threshold
                if isinstance(comment, praw.models.reddit.comment.Comment) and comment.ups > threshold:
                    top_comments.append( comment )
            # manage top_comments list
            if len(top_comments) > (maxcomments + 20):
                top_comments.sort(key=lambda comment: comment.ups, reverse=True) # python sort() is very fast on partially sorted lists
                top_comments = top_comments[:maxcomments] # only keep top comments
                threshold = int(top_comments[-1].ups) # [-1] is okay because len() == maxcomments

    # final size of top_comments list
    top_comments.sort(key=lambda comment: comment.ups, reverse=True)
    top_comments = top_comments[:int(maxcomments)] # only keep top comments

    print '{"section": "--- TOP COMMENTS (grouped by original parent post) ---"}'
    
    # re-build list of top comments (group by parent post)
    post_comment_ids = {}
    post_list = []
    for comment in top_comments:
        # check if post_id already encountered 
        if comment.link_id not in post_comment_ids:
            post_comment_ids[ comment.link_id ] = [] # empty list for 'child' comments
            post_list.append( comment.link_id )      # add to sorted list of 'parent' posts
        # store comment for later display
        post_comment_ids[ comment.link_id ].append( comment )
   
    # display nested posts/comments lists
    for post_id in post_list:
        if post_id in post_cache:
            print post_details_json( post_cache[ post_id ] )
            for comment in post_comment_ids[ post_id ]:
                print comment_details_json( comment )

if __name__ == "__main__":
    main()
