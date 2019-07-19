#!/usr/bin/env python3

import argparse
from datetime import datetime
from typing import Optional

from settings import Settings

try:
    import ujson as json
except ImportError:
    import json


def print_log(file_path: str, grep_str: Optional[str],
              time_gt: str, time_lt: str, time_eq: str):
    with open(file_path) as f:
        line = f.readline()
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
            except ValueError as e:
                print('Bad json: ', line)
            except KeyError as e:
                print(f'Bad field {e}: ', line)
            finally:
                line = f.readline()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="File to parse as json log")
    parser.add_argument("-s", "--string", help="File to parse as json log")
    parser.add_argument("-g", "--time_gt", help="Time is greater than")
    parser.add_argument("-l", "--time_lt", help="Time is less than")
    parser.add_argument("-t", "--time_eq", help="Time equals")
    args = parser.parse_args()
    print_log(args.file, args.string, time_gt=args.time_gt, time_lt=args.time_lt, time_eq=args.time_eq)
