#!/usr/bin/env python3


import os
import sys
import json
import random
import datetime
import argparse


sys.path.append(os.path.abspath(os.path.join(__file__,'../../..')))
from lunchbot import send_lunchbot_message


def get_cake_urls():
    import requests
    from bs4 import BeautifulSoup
    baseurl = 'https://www.bbcgoodfood.com/recipes/collection/birthday-cake-recipes'
    links = []
    for page in [1,2,3]:
        source = requests.get(baseurl+'?page={}'.format(page))
        soup = BeautifulSoup(source.content, 'lxml')
        links_raw = [str(el.get('href')) for el in soup.find_all('a')]
        for link in links_raw:
            if link.startswith('/'): link = 'https://www.bbcgoodfood.com/recipes'+link
            if not link.startswith('https://www.bbcgoodfood.com/recipes/'): continue
            if not 'cake' in link: continue
            if 'search' in link: continue
            if 'collection' in link: continue
            if link in links: continue
            links.append(link)
    return links


if __name__=='__main__':

    # command line args
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--inputfile', default='birthdays.json')
    parser.add_argument('-c', '--channel', default=None)
    args = parser.parse_args()

    # read input file
    with open(args.inputfile, 'r') as f:
        data = json.load(f)
    print('Read following birthdays from input file:')
    for name, date in sorted(data.items()): print('  - {}: {}'.format(name, date))

    # convert dates to python date objects (datetime module)
    # todo: current implementation using datetime.today().year
    #       will not work for early warning messages
    #       for birthdays just after new year,
    #       need to somehow use the next year instead.
    dates = {}
    for name, datestr in sorted(data.items()):
        try:
            day = int(datestr.split('/')[0])
            month = int(datestr.split('/')[1])
            date = datetime.date(datetime.date.today().year, month, day)
            dates[name] = date
        except:
            print('WARNING: did not find valid date for {}.'.format(name))

    # define messages for today
    messages = []
    cake_urls = get_cake_urls()
    for name, date in sorted(dates.items()):
        # first warning, a few days in advance
        if (date - datetime.timedelta(days=3)) == datetime.date.today():
            # message for channel members
            if name.lower()==name:
                m = "Attention @all, please be aware that @{}'s birthday is coming soon".format(name)
                m += " (on {}/{})!".format(date.day, date.month)
                m += " @{}, please do not forget to prepare a birthday cake".format(name)
                m += " for your dear colleagues".format(name)
                m += " (for example this one: {}).".format(random.choice(cake_urls))
                messages.append(m)
            # message for non-channel members
            else:
                m = "Attention @all, please be aware that {}'s birthday is coming soon".format(name)
                m += " (on {}/{})!".format(date.day, date.month)
                m += " You may also remind {} to prepare a birthday cake".format(name)
                m += " (for example this one: {}).".format(random.choice(cake_urls))
                messages.append(m)
        # on the morning of the day itself
        if date == datetime.date.today():
            # message for channel members
            if name.lower()==name:
                m = "Hi @all, final reminder of @{}'s birthday today!".format(name)
                messages.append(m)
            # message for non-channel members
            else:
                m = "Hi @all, final reminder of {}'s birthday today!".format(name)
                messages.append(m)
    print('Found following birthday messages to be sent today:')
    for message in messages: print('  - {}'.format(message))

    # exit if no messages to display
    if len(messages)==0:
        print('No birthday messages to send today, exiting.')
        sys.exit()

    # send the messages
    for message in messages:
        send_lunchbot_message(message=message, channel=args.channel, verbose=True)
