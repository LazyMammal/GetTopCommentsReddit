GetTopCommentsReddit
====================

# Purpose

This script is for finding highly upvoted top-level comments in a subreddit (from all time). 

An example would be finding top submissions on /r/SketchDaily (where user submissions are actually comment replies to automated daily theme posts).


# Dependencies

PRAW:
* https://praw.readthedocs.io/en/stable/
* pip install praw
* setup ~/.config/praw.ini


# Usage

`python get_top_comments.py --subreddit SketchDaily > SketchDaily.txt`

Output is line-delimited JSON objects (in two sections):

    # Section 1: All Posts  
    {"section": "--- ALL POSTS (/top + /new + /search) ---"}

    # Section 2: Top Comments 
    {"section": "--- TOP COMMENTS (grouped by original parent post) ---"}

    # Submission/Post JSON (appears in section 1 and 2)
    {"author": "Floonet", "downs": 0, "selftext": "Today is another style challenge. Try sketching in a Dr Seussian style!\n\n\"Be who you are and say what you feel, because those who mind don't matter, and those who matter don't mind.\" \n\u2014 Dr. Seuss", "id": "iwt42", "permalink": "https://www.reddit.com/r/SketchDaily/comments/iwt42/july_22nd_dr_seuss/", "name": "t3_iwt42", "created": 1311372161.0, "url": "https://www.reddit.com/r/SketchDaily/comments/iwt42/july_22nd_dr_seuss/", "title": "July 22nd- Dr Seuss", "score": 66, "ups": 66}

    # Comment JSON (only in section 2)
    {"body": "Just saw the movie last night, so I thought I'd try a [Mashup](http://i.imgur.com/3ffIh.jpg)", "permalink": "https://www.reddit.com/r/SketchDaily/comments/iwt42/july_22nd_dr_seuss/c27bdbn", "score": 378, "created": 1311390761.0, "downs": 0, "author": "skitchbot", "ups": 378, "id": "c27bdbn", "link_id": "t3_iwt42"}


# Do It Yourself

    from get_all_posts import get_all_posts
    
    for post in get_all_posts('SketchDaily'):
        print post
        # do something with post.comments
