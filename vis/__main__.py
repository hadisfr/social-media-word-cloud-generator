#!/usr/bin/env python3

from sys import argv
from sys import stderr
from . import WordCloudGen

EX_DATAERR = 65
default_res_addr = "res.png"


def get_addr():
    if len(argv) not in [2, 3]:
        print("usage: python -m vis <txt-texts> [<result>]", file=stderr)
        exit(EX_DATAERR)

    return argv[1], argv[2] if len(argv) > 2 else default_res_addr


def read_text(addr):
    with open(addr) as f:
        res = list(f)
        print("%d lines" % len(res))
        return res


def main():
    txt_addr, res_addr = get_addr()
    with open(res_addr, "wb") as f:
        WordCloudGen().get_word_cloud(read_text(txt_addr)).save(f)


if __name__ == '__main__':
    main()
