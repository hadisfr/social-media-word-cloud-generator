import json
import re


class Parser:
    """Twitter Twint Exported JSON Parser"""

    def __init__(self, addr):
        self.addr = addr

    def get_msgs_as_text(self):
        with open(self.addr) as f:
            return [
                self._clean(tweet["tweet"])
                for tweet in [json.loads(raw_tweet) for raw_tweet in f]
                if len(tweet["reply_to"]) == 1
            ]

    def _clean(self, msg):
        msg = re.sub(r"pic\.twitter\.com\/\S*", "", msg)
        return msg
