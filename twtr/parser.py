import json
import re


class Parser:
    """Twitter Twint Exported JSON Parser"""

    def __init__(self, addr):
        self.addr = addr

    def get_msgs_as_text(self):
        with open(self.addr) as f:
            return [self._clean(json.loads(tweet)["tweet"]) for tweet in f if len(json.loads(tweet)["reply_to"])]

    def _clean(self, msg):
        msg = re.sub(r"pic\.twitter\.com\/\S*", "", msg)
        return msg
