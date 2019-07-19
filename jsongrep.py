#!/usr/bin/env python3

import argparse
from typing import Optional

from settings import Settings

try:
    import ujson as json
except ImportError:
    import json


def print_log(file_path: str, grep_str: Optional[str],
              time_gt: str, time_lt: str, time_eq: str, verbosity: int):
    with open(file_path) as f:
        line = f.readline()
        total_lines = 1
        print_lines = 0
        error_lines = 0
        while line:
            try:
                data = json.loads(line)
                msg = data[Settings.MESSAGE_FIELD]
                time = data[Settings.TIME_FIELD]
                if grep_str is None or grep_str in msg:
                    if time_gt and time < time_gt:
                        continue
                    if time_lt and time > time_lt:
                        continue
                    if time_eq and not time.startswith(time_eq):
                        continue
                    print(time, msg)
                    print_lines += 1
            except Exception as e:
                if verbosity > 1:
                    print(f'{e.__class__} {e}: {line}')
                error_lines += 1
            finally:
                line = f.readline()
                total_lines += 1
        if verbosity > 0:
            print(f' --- Filtered {print_lines} records (total {total_lines}, errors {error_lines}) ---')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="File to parse as json log")
    parser.add_argument("-s", "--string", help="File to parse as json log")
    parser.add_argument("-g", "--time_gt", help="Time is greater than")
    parser.add_argument("-l", "--time_lt", help="Time is less than")
    parser.add_argument("-t", "--time_eq", help="Time equals")
    parser.add_argument("-v", "--verbosity", type=int, choices=[0, 1, 2], default=Settings.VERBOSITY,
                        help="Increase output verbosity")
    args = parser.parse_args()
    print_log(args.file, args.string, time_gt=args.time_gt, time_lt=args.time_lt, time_eq=args.time_eq,
              verbosity=args.verbosity)
