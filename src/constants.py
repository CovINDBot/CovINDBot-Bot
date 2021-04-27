import enum


class Config(enum.Enum):
    timeout = 30  # 30 second timeout


class Message(enum.Enum):
    already_retweeted = "This Tweet has previously been retweeted @{}"
    tweet_retweeted = "This Tweet has been retweeted @{}"
