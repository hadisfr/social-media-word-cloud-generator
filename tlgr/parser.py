import re
from sys import stderr
from os import path
from os import listdir
from lxml import html


class Parser:
    """Teleram Extracted Chat Parser"""

    def __init__(self, addr):
        super(Parser, self).__init__()
        if not path.isdir(addr):
            raise ValueError("%s is not a directory" % addr)

        print("Teleram Extracted Chat: %s" % addr, file=stderr)
        self.files = [path.join(addr, file) for file in listdir(addr) if re.match("messages[0-9]*.html", file)]

        if len(self.files) == 0:
            raise ValueError("%s is not a Teleram extracted chat directory" % addr)

    def get_msgs_as_text(self):
        msgs = []
        for file in self.files:
            print("reading %s" % file, file=stderr)
            msgs += self._get_msgs_as_text(file)
        print("%d messages" % len(msgs), file=stderr)
        return msgs

    def _get_msgs_as_text(self, file):
        with open(file) as f:
            msgs = []
            for msg in re.findall(r"<div class=\"text\">(.+?)</div>", f.read().replace("\n", "")):
                msgs += list(html.fromstring(msg).itertext())
        return msgs
