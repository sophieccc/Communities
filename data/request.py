# -*- coding = utf-8 -*-
# @Time : 12/03/2022 11:31
# @Author : Kiser
# @File : request.py
# @Software : PyCharm
import os
import time
import pandas as pd
import datetime as dt
import praw
from psaw import PushshiftAPI
# to use PSAW
api = PushshiftAPI()
# to use PRAW
reddit = praw.Reddit(
    client_id = "YOUR_CLIENT_ID_HERE",
    client_secret = "YOUR_CLIENT_SECRET_HERE",
    username = "YOUR_USERNAME_HERE",
    password = "YOUR_PASSWORD_HERE",
    user_agent = "my agent"
)

subreddits = ['mentalhealth', 'TechSupport']
start_year = 2020
end_year = 2021
# directory on which to store the data
basecorpus = './my-dataset/'

def log_action(action):
    print(action)
    return

for year in range(start_year, end_year + 1):
    action = "[Year] " + str(year)
    log_action(action)

    dirpath = basecorpus + str(year)
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)

    # timestamps that define window of posts
    ts_after = int(dt.datetime(year, 1, 1).timestamp())
    ts_before = int(dt.datetime(year + 1, 1, 1).timestamp())

    for subreddit in subreddits:
        start_time = time.time()

        action = "\t[Subreddit] " + subreddit
        log_action(action)

        subredditdirpath = dirpath + '/' + subreddit
        if os.path.exists(subredditdirpath):
            continue
        else:
            os.makedirs(subredditdirpath)

        submissions_csv_path = str(year) + '-' + subreddit + '-submissions.csv'

        submissions_dict = {
            "id": [],
            "url": [],
            "title": [],
            "score": [],
            "num_comments": [],
            "created_utc": [],
            "selftext": [],
        }

        # use PSAW only to get id of submissions in time interval
        gen = api.search_submissions(
            after=ts_after,
            before=ts_before,
            filter=['id'],
            subreddit=subreddit,
            limit=100
        )

        # use PRAW to get actual info and traverse comment tree
        for submission_psaw in gen:
            # use psaw here
            submission_id = submission_psaw.d_['id']
            # use praw from now on
            submission_praw = reddit.submission(id=submission_id)

            submissions_dict["id"].append(submission_praw.id)
            submissions_dict["url"].append(submission_praw.url)
            submissions_dict["title"].append(submission_praw.title)
            submissions_dict["score"].append(submission_praw.score)
            submissions_dict["num_comments"].append(submission_praw.num_comments)
            submissions_dict["created_utc"].append(submission_praw.created_utc)
            submissions_dict["selftext"].append(submission_praw.selftext)

            submission_comments_csv_path = str(
                year) + '-' + subreddit + '-submission_' + submission_id + '-comments.csv'

            # extend the comment tree all the way
            submission_praw.comments.replace_more(limit=None)

            # for each submission save separate csv comment file
            pd.DataFrame(submissions_dict).to_csv(subredditdirpath + '/' + submission_comments_csv_path,
                                                          index=False)

        # single csv file with all submissions
        pd.DataFrame(submissions_dict).to_csv(subredditdirpath + '/' + submissions_csv_path,
                                              index=False)

        action = f"\t\t[Info] Found submissions: {pd.DataFrame(submissions_dict).shape[0]}"
        log_action(action)

        action = f"\t\t[Info] Elapsed time: {time.time() - start_time: .2f}s"
        log_action(action)