import lxml.html
import urllib
import requests
from urllib.request import urlopen
from urllib.parse import urljoin
#from urlparse import urljoin
import http.cookiejar
#import cookielib
from bs4 import BeautifulSoup as bsoup
import re
import os

def count_score_num():
    count = 0
    for url in open('top50composer.txt'):
        parent = 'results/composer/'+url[31:-1]
        piecetxt = os.path.join(parent,'pieces.txt')
        try:
            score_links = open(piecetxt)
            for url in score_links:
                    piecename = url[22:url.find('(')]
                    path = os.path.join(parent, piecename)
                    completeName = os.path.join(path, "html.txt")     
                    try:
                        text = open(completeName, "r")
                        soup = bsoup(text.read(), "html.parser")
                        # get ID
                        result = soup.find_all('span', class_='we_file_info2')
                        for i in range(0, len(result)):
                            if 'pdf' in str(result[i]):
                                count += 1
                        print('till',piecename,':',count)
                    except IOError:
                        print('html.txt not found')
        except IOError:
            print('pieces.txt not found')



count_score_num()

