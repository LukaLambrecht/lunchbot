import os
import sys
import numpy as np
import pandas as pd
import subprocess


# Set absolute path to lunchbot exe
THIS_DIR = os.path.abspath(os.path.dirname(__file__))
LUNCHBOT_DIR = os.path.abspath(os.path.join(THIS_DIR, '../../../'))

# Define set of possible days (needed to correctly wrap margins)
DAYS = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]


def subtract_margin(day, hour, minute, margin):
    """
    Subtract margin minutes from meeting time.
    Handles hour + weekday wraparound.
    """

    total_minutes = hour * 60 + minute - margin

    # handle negative (previous day)
    while total_minutes < 0:
        total_minutes += 24 * 60
        day_index = DAYS.index(day)
        day = DAYS[(day_index - 1) % 7]

    new_hour = total_minutes // 60
    new_minute = total_minutes % 60

    return day, new_hour, new_minute


def generate_crontab_rules_from_df(df):
    '''
    Generate a set of crontab rules from a correctly formatted dataframe.
    '''

    # loop over rows
    rules = [] 
    for _, row in df.iterrows():
        day = row['Day'][:3].lower()
        meeting_hour = int(row['Hour'])
        meeting_minute = int(row['Minutes'])
        margin = int(row.get('Margin', 0))

        day, hour, minute = subtract_margin(day, meeting_hour, meeting_minute, margin)

        msg = "Reminder"
        if pd.notna(row.get('User')):
            msg += f" to @{row['User']}"
        if pd.notna(row.get('Message')):
            msg += f": {row['Message']}"
        if pd.notna(row.get('URL')):
            msg += f" (link: {row['URL']})"

        cmd = f"cd {LUNCHBOT_DIR} && ./lunchbot.py -m '{msg}' > log.txt 2>&1"

        rules.append(f"{minute} {hour} * * {day} {cmd}")

    return rules


def update_crontab(rules):
    marker_start = "# BEGIN LUNCHBOT (AUTO-GENERATED)"
    marker_end = "# END LUNCHBOT (AUTO-GENERATED)"

    result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
    current = result.stdout if result.returncode == 0 else ""

    if marker_start in current:
        before = current.split(marker_start)[0]
        after = current.split(marker_end)[-1]
        new_cron = before
    else:
        new_cron = current

    new_cron += f"\n{marker_start}\n"
    new_cron += "\n".join(rules)
    new_cron += f"\n{marker_end}\n"

    subprocess.run(["crontab", "-"], input=new_cron, text=True)


if __name__=='__main__':

    # read url from command line or default from stored in file
    if len(sys.argv) > 1: sheeturl = sys.argv[1]
    else:
        try:
            from sheeturl import sheeturl
        except: raise Exception('Could not read default sheet URL.')

    # make url suitable for reading content as csv
    sheetid = sheeturl.split('/d/')[-1].split('/')[0]
    sheeturl = f'https://docs.google.com/spreadsheets/d/{sheetid}/export?format=csv'

    # read sheet in pandas dataframe
    df = pd.read_csv(sheeturl)
    df = df.dropna(axis=0, subset=['Day', 'Hour', 'Minutes'])
    df = df.replace({np.nan: None})
    df.reset_index(inplace=True)
    print('Found following dataframe:')
    print(df)

    # make crontab rules
    rules = generate_crontab_rules_from_df(df)

    # print result
    print('Found following crontab rules:')
    for rule in rules: print(rule)

    # edit crontab file
    update_crontab(rules)
    print('Crontab file has been updated.')
