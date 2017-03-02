
# Automatic Google Sheets Punch Clock

This is a small bash script coupled with a Python script that logs the first desktop-unlock and the last desktop-lock event for each day to a Google Spreadsheet, to serve as an automatic punch-clock. 

## Packages needed

```
pip3 install gspread
pip3 install --upgrade oauth2client
````

## How to use

* Follow the instructions from the [gspread](https://github.com/burnash/gspread) repo to set up OAuth2 credentials from the Google Developers Console.
    * Download the json file, rename it to `creds.json` and copy it to the directory.

* Create a spreadsheet in your Google Drive and share it with the Google service account you've created.

* In the directory, create a file `sheet_key.py` containing only `key = <key_from_your_spreadsheet_url_here>`. Will later change this to a config file or a command line parameter.

* Create a symlink to `punch_clock.py` named `/usr/bin/punch-clock` or otherwise arrange it so that running `punch-clock` from a terminal results in running the program.

* Copy `lock_unlock_monitor.sh` script to `/etc/init.d/lock-unlock-monitor.sh` to run it on every boot (make sure it has execute permission). It will monitor desktop lock/unlock events.

## TODO:

* Do a check if sheet exists and create one if it doesn't.
* Add a spreadsheet template.
* Add command line flags for specifying spreadsheet name or key.