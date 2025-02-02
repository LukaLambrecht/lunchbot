#!/usr/bin/env python3


import os
import sys
import json
import argparse


if __name__=='__main__':

    # command line args
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--inputfile', default='meetings.json')
    parser.add_argument('-c', '--channel', default=None)
    parser.add_argument('-u', '--user', default=None)
    args = parser.parse_args()

    # read input file
    with open(args.inputfile, 'r') as f:
        meetings = json.load(f)
    print('Read following meetings from input file:')
    for meeting_name, meeting_info in meetings.items():
        print('  - {}: {}'.format(meeting_name, meeting_info))

    # set path to lunchbot directory
    thisdir = os.path.abspath(os.path.dirname(__file__))
    lunchbotdir = os.path.abspath(os.path.join(thisdir, '../../'))

    # loop over meetings
    crons = []
    for meeting_name, meeting_info in meetings.items():

        # convert day and time to cron format
        day = meeting_info['day'].lower()[:3]
        time = meeting_info['time']
        hour, minutes = time.split(':')
        hour = int(hour)
        minutes = int(minutes)
        cron_time = '{} {} * * {}'.format(minutes, hour, day)

        # make message
        msg = 'Reminder'
        if args.user is not None: msg += f' to @{args.user}'
        msg += f': your meeting "{meeting_name}" is starting soon!'
        if meeting_info['url'] is not None:
            msg += ' Join via this link: {}'.format(meeting_info['url'])

        # make full cron command
        cmd = 'cd {}'.format(lunchbotdir)
        cmd += ' && ./lunchbot.py -m \'{}\''.format(msg)
        if args.channel is not None: cmd += ' -c {}'.format(args.channel)
        cmd += ' > log.txt 2>&1'
        cron = cron_time + ' ' + cmd
        crons.append(cron)

    # print results
    print('Copy-paste the following into your crontab file:')
    for cron in crons: print(cron)
