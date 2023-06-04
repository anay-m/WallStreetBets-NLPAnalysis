import praw
import datetime as dt
import os
import pymysql as sql
import asyncio

#Access Reddit Info
CLIENT_ID = os.environ["CLIENT_ID"]
CLIENT_SECRET = os.environ["CLIENT_SECRET"]
USER_AGENT = os.environ["USER_AGENT"]
reddit = praw.Reddit(client_id = CLIENT_ID, 
                     client_secret = CLIENT_SECRET, 
                     user_agent = USER_AGENT)

async def fetch_submission(submission):
    print(f"Fetching submission: {submission.title}")
    await asyncio.sleep(2)
    return submission.title

async def process_subreddit(subreddit_name, limit=5):
    subreddit = reddit.subreddit(subreddit_name)
    submissions = subreddit.hot(limit=limit)

    tasks = [fetch_submission(submission) for submission in submissions]
    return await asyncio.gather(*tasks)

async def main():
    subreddit_names = ["wallstreetbets", "stocks"]

    for subreddit_name in subreddit_names:
        print(f"Processing subreddit: {subreddit_name}")
        results = await process_subreddit(subreddit_name)
        print(f"Processed subreddit: {subreddit_name}")
        for result in results:
            print(f"Submission: {result}")

asyncio.run(main())