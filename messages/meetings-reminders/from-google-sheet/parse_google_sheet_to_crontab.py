import os
import sys
import numpy as np
import pandas as pd


if __name__=='__main__':

    # read url from command line
    url = sys.argv[1]

    # make url suitable for reading content as csv
    url = url.replace('edit?usp=sharing', 'export?format=csv')

    # read sheet in pandas dataframe
    df = pd.read_csv(url)
    df = df.dropna(axis=0, subset=['Day', 'Hour', 'Minutes'])
    df = df.replace({np.nan: None})
    df.reset_index(inplace=True)
    print('Found following dataframe:')
    print(df)

    # parse days
    days = df['Day'].values
    days = [day[:3].lower() for day in days]

    # set path to lunchbot directory
    thisdir = os.path.abspath(os.path.dirname(__file__))
    lunchbotdir = os.path.abspath(os.path.join(thisdir, '../../../'))

    # loop over rows
    rules = []
    for index, row in df.iterrows():

        # get data
        day = days[index]
        hour = int(row['Hour'])
        minute = int(row['Minutes'])
        message = row['Message']
        url = row['URL']
        user = row['User']
        channel = row['Channel']

        # make message
        msg = 'Reminder'
        if user is not None: msg += f' to @{user}'
        if message is not None: msg += f': {message}'
        if url is not None: msg += f' (link: {url})'

        # make command
        cmd = f'cd {lunchbotdir} && ./lunchbot.py -m \'{msg}\''
        if channel is not None: cmd += f' -c {channel}'
        cmd += ' > log.txt 2>&1'

        # make crontab rule
        rule = f'{minute} {hour} * * {day} {cmd}'
        rules.append(rule)

    # print result
    print('Copy-paste the following into your crontab file:')
    for rule in rules: print(rule)
