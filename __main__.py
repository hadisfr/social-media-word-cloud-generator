#!/usr/bin/env python3

from sys import argv
from sys import stderr

from tlgr import Parser
from tlgr import WordCloud

EX_DATAERR = 65
default_res_addr = "res.png"


def get_addr():
    if len(argv) not in [2, 3]:
        print("usage: %s <extracted-chats-folder> [<result>]" % argv[0], file=stderr)
        exit(EX_DATAERR)

    return argv[1], argv[2] if len(argv) > 2 else default_res_addr


def main():
    tlgr_addr, res_addr = get_addr()
    with open(res_addr, "wb") as f:
        WordCloud().get_word_cloud(Parser(tlgr_addr).get_msgs_as_text()).save(f)


if __name__ == '__main__':
    main()
