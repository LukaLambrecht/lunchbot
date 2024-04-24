#!/usr/bin/env python3

# References:
# - https://developers.mattermost.com/integrate/webhooks/incoming/?utm_source=mattermost&utm_medium=in-product&utm_content=installed_incoming_webhooks&uid=d5p7qup7off9jy48u5qbek68uc&sid=1q5ehw3axtgk9ex8e9i8nez95o

import os
import json
import argparse
import requests

from URL import lunchboturl

if __name__=='__main__':

    # command line args
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--message', default=None)
    parser.add_argument('-c', '--channel', default=None)
    args = parser.parse_args()

    # fixed settings
    headers = {'Content-Type': 'application/json'}
    icon_emoji = ':sandwich:'

    # parse the message
    text = ''
    if args.message is None: text = 'Lunchtime!'
    elif args.message.endswith('.txt'):
        if os.path.exists(args.message):
            with open(args.message, 'r') as f:
                text = f.readlines()
            text = ''.join(text)
            text = text.strip(' \t\n')
        else:
            msg = 'ERROR: message file {} not found.'.format(args.message)
            raise Exception(msg)
    else: text = args.message

    # make the json payload
    payload = {}
    payload['text'] = text
    payload['icon_emoji'] = icon_emoji
    if args.channel is not None: payload['channel'] = args.channel
    print('Constructed follwing payload:')
    print(payload)

    # make the POST request
    response = requests.post(lunchboturl, headers=headers, json=payload)
    print('POST request returned the following response:')
    print(response.text)
