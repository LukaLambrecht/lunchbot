#!/usr/bin/env python3

# References:
# - https://developers.mattermost.com/integrate/webhooks/incoming/?utm_source=mattermost&utm_medium=in-product&utm_content=installed_incoming_webhooks&uid=d5p7qup7off9jy48u5qbek68uc&sid=1q5ehw3axtgk9ex8e9i8nez95o


import os
import json
import argparse
import requests

from URL import lunchboturl


def send_lunchbot_message(message=None, channel=None, verbose=False):
    
    # fixed settings
    headers = {'Content-Type': 'application/json'}
    icon_emoji = ':sandwich:'

    # parse the message
    text = ''
    if message is None: text = 'Lunchtime!'
    elif message.endswith('.txt'):
        if os.path.exists(message):
            with open(message, 'r') as f:
                text = f.readlines()
            text = ''.join(text)
            text = text.strip(' \t\n')
        else:
            msg = 'ERROR: message file {} not found.'.format(message)
            raise Exception(msg)
    else: text = message
    if verbose:
        print('Found following message to send:')
        print(text)

    # make the json payload
    payload = {}
    payload['text'] = text
    payload['icon_emoji'] = icon_emoji
    if channel is not None: payload['channel'] = channel
    if verbose:
        print('Constructed following payload:')
        print(payload)

    # make the POST request
    response = requests.post(lunchboturl, headers=headers, json=payload)
    if verbose:
        print('POST request returned the following response:')
        print(response.text)


if __name__=='__main__':

    # command line args
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--message', default=None)
    parser.add_argument('-c', '--channel', default=None)
    args = parser.parse_args()

    # send the message
    send_lunchbot_message(
            message=message,
            channel=channel,
            verbose=True
    )
