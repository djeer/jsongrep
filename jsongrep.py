#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import sys

try:
    import ujson as json  # import faster parser, if present
except ImportError:
    import json


class Settings:
    MESSAGE_FIELD = 'message'
    TIME_FIELD = '@timestamp'
    VERBOSITY = 1


def process_line(line, params):
    data = json.loads(line)

    if params.super_string and params.super_string not in line:
        return

    msg = data[Settings.MESSAGE_FIELD]
    if params.string and params.string not in msg:
        return
    if params.exclude_string and params.exclude_string in msg:
        return

    time = data[Settings.TIME_FIELD]
    if params.time_gt and time < params.time_gt:
        return
    if params.time_lt and time > params.time_lt:
        return
    if params.time_eq and not time.startswith(params.time_eq):
        return

    if params.key:
        for s in params.key:
            k, v = s.split('=')[:2]
            if str(data[k]) != v:
                return

    return '%s %s' % (time, msg)


def process_lines(lines, params):
    total_lines = 0
    print_lines = 0
    error_lines = 0
    for line in lines:
        total_lines += 1
        try:
            text = process_line(line, params)
            if text is None:
                continue
            print(text)
            print_lines += 1
        except Exception as e:
            if params.verbosity > 1:
                print(e, e.__class__, line)
            error_lines += 1
    if params.verbosity > 0:
        print(' --- Printed %s records (total %s, errors %s) ---' %
              (print_lines, total_lines, error_lines))


def file_iterator(file_path):
    with open(file_path) as f:
        line = f.readline()
        while line:
            yield line
            line = f.readline()


def stdin_iterator():
    for line in sys.stdin:
        yield line


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="File to parse as json log", nargs='?')
    parser.add_argument("-s", "--string", help="String to apply as filter to message", nargs='?')
    parser.add_argument("-xs", "--exclude_string", help="String to apply as exclude filter to message", nargs='?')
    parser.add_argument("-ss", "--super_string", help="String to apply as filter to whole json record", nargs='?')
    parser.add_argument("-k", "--key", help="Filter json top level data, i.e. --key level=WARNING", nargs='*')
    parser.add_argument("-g", "--time_gt", help="Time is greater than", nargs='?')
    parser.add_argument("-l", "--time_lt", help="Time is less than", nargs='?')
    parser.add_argument("-t", "--time_eq", help="Time equals", nargs='?')
    parser.add_argument("-v", "--verbosity", type=int, choices=[0, 1, 2], default=Settings.VERBOSITY,
                        help="Increase output verbosity", nargs='?')
    args = parser.parse_args()
    if args.file is None or args.file == 'stdin':
        lines_iterator = stdin_iterator()
    else:
        lines_iterator = file_iterator(args.file)
    process_lines(lines_iterator, params=args)
