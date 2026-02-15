# Parse google sheet into crontab rules for lunchbot reminders

Instructions:
- Make a google sheet in the appropriate format.
- Make sure it is publicly accessible (read-only is fine).
- Run `python parse_google_sheet_to_crontab.py <url of google sheet>`
- Copy paste the output to your crontab file.

Todo: avoid the need for running the python script by inserting a button directly in the sheet running a sheet script.
