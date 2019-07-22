#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import sys

try:
    import ujson as json
except ImportError:
    import json


class Settings:
    MESSAGE_FIELD = 'message'
    TIME_FIELD = '@timestamp'
    VERBOSITY = 1


def process_line(line, grep_str, exclude_str, super_str, time_gt, time_lt, time_eq):
    data = json.loads(line)

    if super_str and super_str not in line:
        return

    msg = data[Settings.MESSAGE_FIELD]
    if grep_str and grep_str not in msg:
        return None, None
    if exclude_str and exclude_str in msg:
        return None, None

    time = data[Settings.TIME_FIELD]
    if time_gt and time < time_gt:
        return None, None
    if time_lt and time > time_lt:
        return None, None
    if time_eq and not time.startswith(time_eq):
        return None, None

    return time, msg


def print_log(file_path, grep_str, exclude_str, super_str,
              time_gt, time_lt, time_eq, verbosity):
    with open(file_path) as f:
        line = f.readline()
        total_lines = 0
        print_lines = 0
        error_lines = 0
        while line:
            total_lines += 1
            try:
                time, msg = process_line(line, grep_str, exclude_str, super_str, time_gt, time_lt, time_eq)
                if msg is None:
                    continue
                print('%s %s' % (time, msg))
                print_lines += 1
            except Exception as e:
                if verbosity > 1:
                    print(e, e.__class__, line)
                error_lines += 1
            finally:
                line = f.readline()
        if verbosity > 0:
            print(' --- Filtered %s records (total %s, errors %s) ---' %
                  (print_lines, total_lines, error_lines))


def process_stdin(grep_str, exclude_str, super_str,
                  time_gt, time_lt, time_eq, verbosity):
    total_lines = 0
    print_lines = 0
    error_lines = 0
    for line in sys.stdin:
        total_lines += 1
        try:
            time, msg = process_line(line, grep_str, exclude_str, super_str, time_gt, time_lt, time_eq)
            if msg is None:
                continue
            print('%s %s' % (time, msg))
            print_lines += 1
        except Exception as e:
            if verbosity > 1:
                print(e, e.__class__, line)
            error_lines += 1
    if verbosity > 0:
        print(' --- Filtered %s records (total %s, errors %s) ---' %
              (print_lines, total_lines, error_lines))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="File to parse as json log", nargs='?')
    parser.add_argument("-s", "--string", help="String to apply as filter to message", nargs='?')
    parser.add_argument("-xs", "--exclude_string", help="String to apply as exclude filter to message", nargs='?')
    parser.add_argument("-ss", "--super_string", help="String to apply as filter to whole json record", nargs='?')
    parser.add_argument("-g", "--time_gt", help="Time is greater than", nargs='?')
    parser.add_argument("-l", "--time_lt", help="Time is less than", nargs='?')
    parser.add_argument("-t", "--time_eq", help="Time equals", nargs='?')
    parser.add_argument("-v", "--verbosity", type=int, choices=[0, 1, 2], default=Settings.VERBOSITY,
                        help="Increase output verbosity", nargs='?')
    args = parser.parse_args()
    if args.file == 'stdin':
        process_stdin(grep_str=args.string, exclude_str=args.exclude_string, super_str=args.super_string,
                  time_gt=args.time_gt, time_lt=args.time_lt, time_eq=args.time_eq,
                  verbosity=args.verbosity)
    else:
        print_log(args.file, grep_str=args.string, exclude_str=args.exclude_string, super_str=args.super_string,
                  time_gt=args.time_gt, time_lt=args.time_lt, time_eq=args.time_eq,
                  verbosity=args.verbosity)
