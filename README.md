### Small utility to grep logs encoded in JSON format

#### Usage:

_Print all json messages text:_

`python jsongrep.py user_events.log`


_Print messages with filter (like grep):_

`python jsongrep.py user_events.log -s some_filter_string`

_Print json messages after 2019-07-19T08:31:29:_

`python jsongrep.py user_events.log some_filter_string -g 2019-07-19T08:31:29.169Z `

_Print json messages at the 2019-07-19T08:31:29 time:_

`python jsongrep.py user_events.log some_filter_string -e 2019-07-19T08:31:29 `


Time comparing is naive, it compares python strings. It works well for all iso-like formats like "%y-%m-%d %H:%M:%S" or "%Y-%m-%dT%H:%M:%SZ" without need to parse dates & handle timezones and you can write time partitially like "2019-07-19T08:30".  