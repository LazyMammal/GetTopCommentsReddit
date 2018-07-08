import time
import praw

# generator function for subreddit posts (top + new + hot + gilded)
# note: timestamp search is no longer part of reddit api
# note: yielded posts are unique (duplicates are discarded)


def get_all_posts(subreddit):
    reddit = praw.Reddit(site_name='get_top_comments',
                         user_agent='Get all subreddit posts, by LazyMammal v 0.1')  # , log_requests=1)
    sr = reddit.subreddit(subreddit)

    post_limit = 1000
    post_id_cache = set()

    for gen in [sr.top, sr.new, sr.hot, sr.gilded]:
        for post in gen(limit=post_limit):
            if post.id not in post_id_cache:
                post_id_cache.add(post.id)
                yield post


def main():
    # debug output
    for post in get_all_posts('saved'):  # /r/saved is a small subreddit
        if isinstance(post, praw.models.reddit.submission.Submission):
            print post
            for k in post.__dict__.keys():
                print '\t', k, str(post.__dict__[k])
            break


if __name__ == "__main__":
    main()
