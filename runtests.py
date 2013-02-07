#!/usr/bin/env python

import sys

import nose


if __name__ == '__main__':
    nose_args = sys.argv + ['--config', 'test.cfg', '--with-doctest']
    if nose.run(argv=nose_args):
        sys.exit(0)
    else:
        sys.exit(1)

