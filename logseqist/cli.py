#!/usr/bin/env python
# -*- coding: utf-8 -*-

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter


def parsed():
    parser = ArgumentParser(description='',
                            formatter_class=ArgumentDefaultsHelpFormatter)
    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument('--file', help='')

    return parser


if __name__ == '__main__':
    arguments = parsed().parse_args()
