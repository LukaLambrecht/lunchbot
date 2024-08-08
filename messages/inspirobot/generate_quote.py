#!/usr/bin/env python3


import os
import sys
import json
import requests
import argparse


sys.path.append(os.path.abspath(os.path.join(__file__,'../../..')))
from lunchbot import send_lunchbot_message


def get_quote_url():
    url = 'https://inspirobot.me/api?generate=true'
    response = requests.get(url)
    if response.status_code==200:
        imgurl = response.text
        return imgurl
    else:
        msg = 'ERROR: request returned status code {}'.format(request.status)
        msg += ' with message {}'.format(request.text)
        raise Exception(msg)

if __name__=='__main__':

    # command line args
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--channel', default=None)
    args = parser.parse_args()

    # get a newly generated inspirational quote from inspirobot
    imgurl = get_quote_url()

    # format the message
    message = '@all, here\'s your inspiration for today:\n{}'.format(imgurl)

    # send the message
    send_lunchbot_message(message=message, channel=args.channel, verbose=True)
