#!/usr/bin/env python3

from sys import argv
from sys import stderr

from tlgr import Parser
from tlgr import WordCloud

EX_DATAERR = 65


def get_addr():
    if len(argv) != 2:
        print("usage: %s <extracted-chats-folder>" % argv[0], file=stderr)
        exit(EX_DATAERR)

    return argv[1]


def main():
    texts = Parser(get_addr()).get_msgs_as_text()
    # texts = texts[:10]
    # print("\n".join(texts))
    WordCloud().get_word_cloud(texts)


if __name__ == '__main__':
    main()
