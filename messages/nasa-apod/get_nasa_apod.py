#!/usr/bin/env python3


import os
import sys
import json
import requests
import argparse
from bs4 import BeautifulSoup


sys.path.append(os.path.abspath(os.path.join(__file__,'../../..')))
from lunchbot import send_lunchbot_message


def get_urls():
    baseurl = 'https://apod.nasa.gov/apod/astropix.html'
    source = requests.get(baseurl)
    soup = BeautifulSoup(source.content, 'lxml')
    links_raw = [str(el.get('href')) for el in soup.find_all('a')]
    links_img = []
    for link in links_raw:
        if link.split('/')[0]=='image': links_img.append(link)
    if len(links_img)!=1:
        msg = 'ERROR: found unexpected number of image urls: {}'.format(len(links_img))
        msg += ' ({})'.format(links_img)
        raise Exception(msg)
    imgurl = baseurl.rsplit('/',1)[0] + '/' + links_img[0]
    return (baseurl, imgurl)


if __name__=='__main__':

    # command line args
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--channel', default=None)
    args = parser.parse_args()

    # get a newly generated inspirational quote from inspirobot
    (baseurl, imgurl) = get_urls()

    # format the message
    message = 'Hi @all, here\'s NASA\'s astronomy picture of the day:\n{}'.format(imgurl)
    message += '\n(read the explanation [here]({})).'.format(baseurl)

    # send the message
    send_lunchbot_message(message=message, channel=args.channel, verbose=True)
