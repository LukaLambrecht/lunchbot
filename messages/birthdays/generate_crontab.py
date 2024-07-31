#!/usr/bin/env python3


import os


if __name__=='__main__':

    # define the crontab
    location = os.path.abspath(os.path.join(__file__,'../'))
    cmd = 'cd {}'.format(location)
    cmd += ' && ./check_birthdays.py -i birthdays.json -c town-square'
    cmd += ' > log.txt 2> log.txt'
    hour = 8
    minute = 0
    crontab = '{} {} * * * {}'.format(minute, hour, cmd)

    # print results
    print('Copy-paste the following into your crontab file:')
    print(crontab)
