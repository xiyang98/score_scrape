import re
from bs4 import BeautifulSoup
import requests
import urllib
import lxml.html
#urls = re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', url)
pieces = open('score_id_to_url_map.txt', 'r')
for line in pieces.readlines():
    filename = line[:6] #grabs the ID
    url = re.search("(?P<url>https?://[^\s]+)", line).group("url") #gets url from line

    s = requests.Session()
    urlContents = s.get(url)

    pageText = urlContents.content

    #write to a file
    writeFile = open(filename+'.txt', 'wb')
    writeFile.write(pageText)
    writeFile.close()