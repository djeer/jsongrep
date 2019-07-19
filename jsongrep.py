#!/usr/bin/env python3

import sys
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
    file_path = sys.argv[1]
    try:
        grep_str = sys.argv[2]
    except IndexError:
        grep_str = None

    print_log(file_path, grep_str)

