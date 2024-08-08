#!/usr/bin/env python3


import os
import sys
import json
import random
import datetime
import argparse
import requests
from bs4 import BeautifulSoup


sys.path.append(os.path.abspath(os.path.join(__file__,'../../..')))
from lunchbot import send_lunchbot_message


def get_url():
    baseurl = 'https://cms.cern/tags/physics-briefing'
    source = requests.get(baseurl)
    soup = BeautifulSoup(source.content, 'lxml')
    links_raw = [str(el.get('href')) for el in soup.find_all('a')]
    url = 'https://cms.cern' + [l for l in links_raw if l.startswith('/news/')][0]
    return url


if __name__=='__main__':

    # command line args
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--channel', default=None)
    args = parser.parse_args()

    # get latest briefing url
    url = get_url()

    # read file with latest already posted briefing and compare
    latest_file = 'latest.txt'
    latest_url = None
    if os.path.exists(latest_file): 
        with open(latest_file, 'r') as f:
            latest_url = f.readline()
    if latest_url is not None and latest_url==url:
        msg = 'No new briefing found, exiting.'
        print(msg)
        sys.exit()
    else:
        with open(latest_file, 'w') as f:
            f.write(url)

    # format message
    message = 'Hi all, there is a new CMS Physics Briefing!'
    message += '\nRead it here: {}'.format(url)

    # send the messages
    send_lunchbot_message(message=message, channel=args.channel, verbose=True)
