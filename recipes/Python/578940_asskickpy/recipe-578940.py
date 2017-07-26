#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: pantuts
# URL: http://pantuts.com
# Agreement: You can use, modify, or redistribute this tool under the terms of GNU General Public License (GPLv3).
# This tool is for educational purposes only. Any damage you make will not affect the author.
# Dependencies:
# requests: https://pypi.python.org/pypi/requests
# beautifulSoup4: https://pypi.python.org/pypi/beautifulsoup4/4.3.2
# tabulate: https://pypi.python.org/pypi/tabulate

from bs4 import BeautifulSoup
import os
import re
import requests
import subprocess
import sys
import tabulate


class OutColors:
    DEFAULT = '\033[0m'
    BW = '\033[1m'
    LG = '\033[0m\033[32m'
    LR = '\033[0m\033[31m'
    SEEDER = '\033[1m\033[32m'
    LEECHER = '\033[1m\033[31m'


def helper():
    print(OutColors.DEFAULT + "\nSearch torrents from Kickass.to ;)")


def select_torrent():
    torrent = input('>> ')
    return torrent


def download_torrent(url):
    fname = os.getcwd() + '/' + url.split('title=')[-1] + '.torrent'
    # http://stackoverflow.com/a/14114741/1302018
    try:
        r = requests.get(url, stream=True)
        with open(fname, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    f.flush()
    except requests.exceptions.RequestException as e:
        print('\n' + OutColors.LR + str(e))
        sys.exit(1)

    return fname


def aksearch():
    helper()
    tmp_url = 'http://kickass.to/usearch/'

    query = input('Type query: ')
    url = tmp_url + query + '/'

    try:
        cont = requests.get(url)
    except requests.exceptions.RequestException as e:
        raise SystemExit('\n' + OutColors.LR + str(e))

    # check if no torrents found
    if not re.findall(r'Download torrent file', str(cont.content)):
        print('Torrents found: 0')
        aksearch()
    else:
        soup = BeautifulSoup(cont.content)

        # to use by age, seeders, and leechers
        # sample:
        # 700.46 MB
        # 5
        # 2 years
        # 1852
        # 130
        al = [s.get_text() for s in soup.find_all('td', {'class':'center'})]

        href = [a.get('href') for a in soup.find_all('a', {'title':'Download torrent file'})]
        size = [t.get_text() for t in soup.find_all('td', {'class':'nobr'}) ]
        title = [ti.get_text() for ti in soup.find_all('a', {'class':'cellMainLink'})]
        age = al[2::5]
        seeders = al[3::5]
        leechers = al[4::5]

        # for table printing
        table = [[OutColors.BW + str(i+1) + OutColors.DEFAULT if (i+1) % 2 == 0 else i+1,
                    OutColors.BW + title[i] + OutColors.DEFAULT if (i+1) % 2 == 0 else title[i],
                    OutColors.BW + size[i] + OutColors.DEFAULT if (i+1) % 2 == 0 else size[i],
                    OutColors.BW + age[i] + OutColors.DEFAULT if (i+1) % 2 == 0 else age[i],
                    OutColors.SEEDER + seeders[i] + OutColors.DEFAULT if (i+1) % 2 == 0 else OutColors.LG + seeders[i] + OutColors.DEFAULT,
                    OutColors.LEECHER + leechers[i] + OutColors.DEFAULT if (i+1) % 2 == 0 else OutColors.LR + leechers[i] + OutColors.DEFAULT] for i in range(len(href))]
        print()
        print(tabulate.tabulate(table, headers=['No', 'Title', 'Size', 'Age', 'Seeders', 'Leechers']))

        # torrent selection
        if len(href) == 1:
            torrent = 1
        else:
            print('\nSelect torrent: [ 1 - ' + str(len(href)) + ' ] or [ M ] to go back to main menu or [ Q ] to quit')
            torrent = select_torrent()
            if torrent == 'Q' or torrent == 'q':
                sys.exit(0)
            elif torrent == 'M' or torrent == 'm':
                aksearch()
            else:
                if int(torrent) <= 0 or int(torrent) > len(href):
                    print('Use eyeglasses...')
                else:
                    print('Download >> ' + href[int(torrent)-1].split('title=')[-1] + '.torrent')
                    fname = download_torrent(href[int(torrent)-1])
                    subprocess.Popen(['xdg-open', fname], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    aksearch()


if __name__ == '__main__':
    try:
        aksearch()
    except KeyboardInterrupt:
        print('\nHuha!')
