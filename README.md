Inspired by [/u/pashbrown and /u/demeschor](https://bit.ly/2Wwfe6G), this bot
really cares about clear communication. Perhaps, it couldn't care more.

Base code inspired by [nickatnight@](https://github.com/nickatnight/docker-reddit-bot-base).

## Usage

Run with `docker run -v <path_to_env>:/app/.env <image_name>`, where
the `.env` file should be of the form:

```
USERNAME=
PASSWORD=
CLIENT_ID=
CLIENT_SECRET=
SUBREDDIT=
DELAY=
BOT_NAME=
VERSION=
DEVELOPER=
```