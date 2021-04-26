import tweepy
import logging
import time
from src.constants import Config, Message

logger = logging.getLogger()


class CovINDBot:
    def __init__(self, config_file: dict) -> None:
        self.twitter_api = None
        self.last_id = 1
        self.bot_setup(config_file)
        self.run_bot()

    # Continously run the bot
    def run_bot(self) -> None:
        while True:
            try:
                self.check_mentions()
                logger.debug(self.last_id)
                time.sleep(Config.timeout.value)
            except Exception as exc:
                logger.error(exc)

    # Initialise the bot
    def bot_setup(self, config_file: dict) -> None:
        auth = tweepy.OAuthHandler(config_file["API Key"], config_file["API Secret"])
        auth.set_access_token(
            config_file["Access Token"], config_file["Access Token Secret"]
        )
        self.twitter_api = tweepy.API(
            auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True
        )
        try:
            self.twitter_api.verify_credentials()
        except Exception as exc:
            logger.error(exc)
            raise exc

    def check_mentions(self) -> None:
        for tweet in tweepy.Cursor(
            self.twitter_api.mentions_timeline, since_id=self.last_id
        ).items():
            self.last_id = tweet.id
            retweet_success = None
            username = ""
            if tweet.in_reply_to_status_id is None:
                retweet_success = self.bot_retweet(
                    tweet.id
                )  # Retweet the original tweet
                username = tweet.author.screen_name  # Get author of original tweet
            else:
                retweet_success = self.bot_retweet(
                    tweet.in_reply_to_status_id
                )  # Retweet the tweet to which it is replied to
                username = (
                    tweet.in_reply_to_screen_name
                )  # Get author of reply ie. mentioner
            message = ""
            if retweet_success:
                message = Message.tweet_retweeted.value.format(username)
            else:
                message = Message.already_retweeted.value.format(username)
            if not username:
                continue  # If username is not present, reply doesn't work
            # Do not reply as it populates the timeline
            # self.reply_to_mention(tweet.id, message)  # Reply to the mention

    # Reply to a tweet
    def reply_to_mention(self, reply_id: str, text: str) -> None:
        self.twitter_api.update_status(
            status=text,
            in_reply_to_status_id=reply_id,
        )

    # Retweet a tweet
    def bot_retweet(self, tweet_id: str) -> bool:
        status = self.twitter_api.get_status(tweet_id)
        if not status.retweeted:
            self.twitter_api.retweet(tweet_id)
            return True
        return False  # Already been retweeted
