import time
import praw

# generator function for subreddit posts (top + new + search)
# note: attempts to get posts from all time using timestamp search
# note: yielded posts are unique (duplicates from top+new are discarded)
# note: NOT sorted purely by timestamp: /top, /new, then /search
def get_all_posts(subreddit):
    r = praw.Reddit(user_agent='Get all subreddit posts, by LazyMammal v 0.1') #, log_requests=1)
    sr = r.get_subreddit(subreddit)

    # cache post id for uniqueness check
    post_id_cache = set()

    # timestamp for search window
    ts = 0

    # generate top posts
    new_posts = sr.get_top_from_all(limit=None) # no limit (returns 1000)
    for post in new_posts:
        if post.id not in post_id_cache:
            ts = max(int(ts), int(post.created)) # keep newest (max) timestamp
            post_id_cache.add( post.id )
            yield post

    # generate new posts
    new_posts = sr.get_new(limit=None) # no limit (returns 1000)
    for post in new_posts:
        if post.id not in post_id_cache:
            ts = min(int(ts), int(post.created)) # keep oldest (min) timestamp
            post_id_cache.add( post.id )
            yield post

    # generate search results
    new_flag = True
    while new_flag:
        # attempt to get all posts up to (and including) oldest post found so far
        # note: it's tempting to use "ts-1" but that might skip posts created with identical timestamps
        # note: loop may terminate early if 25 posts exist with identical timestamp (very unlikely within 1 subreddit)
        querystring = 'timestamp:{}..{}'.format(0, int(ts))
        search_posts = r.search(querystring, subreddit=subreddit, sort='new', syntax='cloudsearch')

        # generate new posts
        new_flag = False
        for post in search_posts:
            if post.id not in post_id_cache:
                ts = min(int(ts), int(post.created)) # keep oldest (min) timestamp
                post_id_cache.add( post.id )
                new_flag = True
                post.permalink = post.permalink.replace('?ref=search_posts','')
                yield post

def main():
    # debug output
    for post in get_all_posts('saved'):  # /r/saved is a small subreddit
        if isinstance(post, praw.objects.Submission):
            print post
            for k in post.__dict__.keys():
                print '\t', k, str(post.__dict__[k])

if __name__ == "__main__":
    main()
