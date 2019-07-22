### Small utility to grep logs encoded in JSON format


#### Installion:
```
cd /var/local
sudo git clone https://github.com/djeer/jsongrep.git
cd jsongrep
sudo chmod +x jsongrep.py
sudo ln jsongrep.py /usr/bin/jsongrep
```


#### Usage:

_Print all json messages text:_

`python jsongrep.py user_events.log` - without installion
 
`jsongrep user_events.log` - after installion


_Print messages with filter (like grep):_

`jsongrep user_events.log -s some_filter_string`

_Print json messages after 2019-07-19T08:31:29:_

`jsongrep user_events.log some_filter_string -g 2019-07-19T08:31:29.169Z `

_Print json messages at the 2019-07-19T08:31:29 time:_

`jsongrep user_events.log some_filter_string -e 2019-07-19T08:31:29 `


Time comparing is naive, it compares python strings. It works well for all iso-like formats without need to parse dates & handle timezones and you can write time partitially like `2019-07-19T08:30` which cannot be parsed without tricks.  

#### Handle stdin UNIX pipeline:


`tail -f transfer_transactions.log | jsongrep `

or with filter:

`tail -f transfer_transactions.log | jsongrep -s sometext`
