# Parse google sheet into crontab rules for lunchbot reminders

### Making the sheet
There are multiple options, but they all start from a google sheet in the appropriate format.
To do: add details on format

### Generating crontab rules via Apps Script
This method uses a script that can be run directly in the google sheet by clicking a button.
The script prints a set of crontab rules that can be copy-pasted to the appropriate crontab file.

Instructions for creating the Apps Script:
- Open the google sheet
- Click Extensions, then Apps Script
- Delete any existing code
- Paste the script stored in [templates/template_apps_script.txt](templates/templates_apps_script.txt)
- Modify as needed. In particular, modify the "lunchbotDir" variable to your local lunchbotDir path.
- Click Save

To do: automatically modify the "lunchbotDir" variable using a generator from the template.

Instructions for creating a clickable button:
- In the google sheet, click Insert, then Drawing.
- Create something that looks like a button.
- Click Save and Close.
- Click the 3 dots on the drawing.
- Select Assign script.
- Enter the name of the function in your Apps Script.

### Modify crontab via python script
This alternative method runs a python script to generate the crontab rules
and modify the crontab file programmatically rather than manually.
Moreover, the running of this script can be added as a cron job itself,
so that the crontab is periodically kept in sync with the google sheet.

Instructions:
- Make sure the script is publicly accessible (read-only is fine).
- Run `python update_crontab.py <url of google sheet>`.
- Alternatively, make a file called `sheeturl.py` with only one line reading `sheeturl = "<sheet URL>"`
  and run `python update_crontab.py` without arguments (the URL will be read from this file automatically).
- Optional: add this command as a cron job.
