#!/usr/bin/env python3

from sys import argv
from sys import stderr

from tlgr import Parser

EX_DATAERR = 65


def get_addr():
    if len(argv) != 2:
        print("usage: %s <extracted-chats-folder>" % argv[0], file=stderr)
        exit(EX_DATAERR)

    return argv[1]


def main():
    texts = Parser(get_addr()).get_msgs_as_text()
    print("\n".join(texts))


if __name__ == '__main__':
    main()
