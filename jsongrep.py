#!/usr/bin/env python3

import argparse
from datetime import datetime
from typing import Optional

from settings import Settings

try:
    import ujson as json
except ImportError:
    import json


def print_log(file_path: str, grep_str: Optional[str]):
    with open(file_path) as f:
        line = f.readline()
        while line:
            try:
                data = json.loads(line)
                msg = data[Settings.MESSAGE_FIELD]
                if grep_str is None or grep_str in msg:
                    print(data[Settings.TIME_FIELD], msg)
            except ValueError as e:
                print('Bad json: ', line)
            except KeyError as e:
                print(f'Bad field {e}: ', line)
            line = f.readline()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="File to parse as json log")
    parser.add_argument("-s", "--string", help="File to parse as json log")
    # TODO parser.add_argument("-t", "--start", help="Time is greater than")
    # TODO parser.add_argument("-u", "--until", help="Time is less than")
    args = parser.parse_args()
    print_log(args.file, args.string)
