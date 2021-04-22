import enum


class Config(enum.Enum):
    timeout = 5  # 5 second timeout


class Message(enum.Enum):
    already_retweeted = "This Tweet has previously been retweeted @{}"
    tweet_retweeted = "This Tweet has been retweeted @{}"
