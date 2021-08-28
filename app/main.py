#!/usr/bin/env python3

import os
import logging
from logging.handlers import RotatingFileHandler

import praw

from dotenv import load_dotenv
load_dotenv()

from datetime import datetime
from time import sleep

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)
handlers = [
    RotatingFileHandler('logging.log', maxBytes=2000, backupCount=3),
    logging.StreamHandler()
]

formatter = logging.Formatter('%(asctime)-15s - %(message)s')
for handler in handlers:
    handler.setFormatter(formatter)
    LOGGER.addHandler(handler)


class RedditBotBase(object):
    """base class for bot config"""

    def __init__(self):
        LOGGER.info('Initiating Bot...')
        self.flair = None
        self.user_agent = f"{os.getenv('BOT_NAME')} | {os.getenv('VERSION')} | " \
                          f"By {os.getenv('DEVELOPER')}"
        self.subreddit = os.getenv("SUBREDDIT")
        self.delay = os.getenv("DELAY")
        self.reddit = praw.Reddit(
            client_id=os.getenv("CLIENT_ID"),
            client_secret=os.getenv("CLIENT_SECRET"),
            username=os.getenv("USERNAME"),
            password=os.getenv("PASSWORD"),
            user_agent=self.user_agent
        )

        LOGGER.info(f"Starting up... {self.user_agent}")


class Bot(RedditBotBase):
    """subclass RedditBotBase and include main method for processing logic"""
    def main(self):
        LOGGER.info("Bot is running")

        subreddit = self.reddit.subreddit(self.subreddit)
        for comment in subreddit.stream.comments():
            self.process_comment(comment)

    def process_comment(self, comment: praw.models.Comment):
        if not comment:
            return

        if 'could care less' in comment.body:
            # Refresh is necessary because otherwise the replies will be empty -
            # https://praw.readthedocs.io/en/latest/code_overview/models/comment.html?highlight=refresh#praw.models.Comment.refresh
            comment.refresh()
            for reply in comment.replies:
                if reply.author.name == os.getenv("USERNAME"):
                    LOGGER.info(f'Avoiding a duplicate reply to {_represent_comment(comment)}')
                    return
            comment.reply('[Are you sure about that](https://could.care/)?\n\n'
                          '^(I am a bot. My code is) ^[here](https://github.com/scubbo/ABotThatCares). '
                          '^(For more information, see) ^[here](https://youtu.be/om7O0MFkmpw).')
            LOGGER.info(f'Replied to {_represent_comment(comment)}')
            # sleep to avoid rate limit
            sleep(int(self.delay))


def _represent_comment(comment: praw.models.Comment):
    return f'https://old.reddit.com/r/test/comments/{comment.submission.id}/a_firework/{comment.id}'


if __name__ == "__main__":
    LOGGER.info('Running main')
    Bot().main()
