import json
import requests

subreddit = 'techsupport'
limit = 1000
listing = 'new'  # controversial, best, hot, new, random, rising, top


def get_reddit(subreddit, listing, limit, after=''):
    r_all = []
    while len(r_all) < 1000:
        try:
            base_url = f'https://www.reddit.com/r/{subreddit}/{listing}.json?limit={limit}{after}'
            request = requests.get(base_url, headers={'User-agent': 'yourbot'})
            r = request.json()
            after = "&after=" + r["data"]["after"]
            r_all += r["data"]["children"]
        except:
            print('An Error Occured')
            return r_all
    return r_all


r_all = get_reddit(subreddit, listing, limit)
keys = ["selftext", "author", "title", "id", "created_utc", "num_comments"]
with open('data/techsupport.json', 'a') as f:
    json_objs = []
    for post in r_all:
        json_obj = {
            "id": post["data"]["id"],
            "created": post["data"]["created_utc"],
            "num_comments": post["data"]["num_comments"],
            "score": post["data"]["score"],
            "text": post["data"]["selftext"],
            "author": post["data"]["author"],
            "title": post["data"]["title"]
        }
        json_objs.append(json_obj)
    json.dump(json_objs, f)