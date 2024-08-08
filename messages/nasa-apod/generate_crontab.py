#!/usr/bin/env python3


import os


if __name__=='__main__':

    # define the crontab
    location = os.path.abspath(os.path.join(__file__,'../'))
    cmd = 'cd {}'.format(location)
    cmd += ' && ./get_nasa_apod.py -c test'
    cmd += ' > log.txt 2> log.txt'
    hour = 11
    minute = 0
    crontab = '{} {} * * * {}'.format(minute, hour, cmd)

    # print results
    print('Copy-paste the following into your crontab file:')
    print(crontab)
