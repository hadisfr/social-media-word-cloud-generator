import json
import csv
import re
from sys import stderr


class Parser:
    """Twitter Twint Exported JSON Parser"""

    def __init__(self, addr):
        self.addr = addr

    def get_msgs_as_text(self):
        if self.addr.endswith("csv"):
            return self.get_msgs_as_text_csv()
        if self.addr.endswith("tsv"):
            return self.get_msgs_as_text_csv("\t")
        return self.get_msgs_as_text_json()

    def get_msgs_as_text_csv(self, delimiter=","):
        with open(self.addr) as f:
            res = [
                self._clean(tweet["tweet"])
                # re.sub(r"#[^\s]+", "", self._clean(tweet["tweet"]))
                for tweet in csv.DictReader(f, delimiter=delimiter)
                if tweet["reply_to"] == "[]" and tweet["tweet"][0] != "@" and tweet["retweet"] == "False"
            ]
            print("%d tweets" % len(res), file=stderr)
            return res

    def get_msgs_as_text_json(self):
        with open(self.addr) as f:
            res = [
                self._clean(tweet["tweet"])
                # re.sub(r"#[^\s]+", "", self._clean(tweet["tweet"]))
                for tweet in [json.loads(raw_tweet) for raw_tweet in f]
                # for tweet in json.load(f)
                if len(tweet["reply_to"]) == 0 and tweet["tweet"][0] != "@" and not tweet["retweet"]
            ]
            print("%d tweets" % len(res), file=stderr)
            return res

    def _clean(self, msg):
        msg = re.sub(r"pic\.twitter\.com\/\S*", "", msg)
        return msg
