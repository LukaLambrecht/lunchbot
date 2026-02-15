# Automatic meeting reminders at fixed days and times during the week

There are several options, that in the end all boil down to calling the main lunchbot script from a cron job.
The difference exists in how to set up the cron jobs.
- Manually edit the crontab file.
- Parse suitable crontab rules from a json file. See `from-json` for details.
- Parse suitable crontab rules from a google sheet. See `from-google-sheet` for details.
