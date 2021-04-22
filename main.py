from configparser import RawConfigParser
from src.bot import CovINDBot

raw_config_parser = RawConfigParser()
raw_config_parser.read("secret.ini")

ACCESS_TOKEN = raw_config_parser.get("Twitter", "ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = raw_config_parser.get("Twitter", "ACCESS_TOKEN_SECRET")
API_KEY = raw_config_parser.get("Twitter", "API_KEY")
API_SECRET = raw_config_parser.get("Twitter", "API_SECRET")

config_file = {
    "Access Token": ACCESS_TOKEN,
    "Access Token Secret": ACCESS_TOKEN_SECRET,
    "API Key": API_KEY,
    "API Secret": API_SECRET,
}

if __name__ == "__main__":
    cov_ind_bot = CovINDBot(config_file)
