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

def next_url(href):
    return href and re.compile("subcatfrom").search(href)

def oldid(href):
    return href and re.compile("oldid").search(href)
    
    
# badlink = [
#     /index.php?title=Category:People&subcatfrom=Aeschbacher%2C+Karl#mw-subcategories
# http://imslp.org/index.php?title=Category:People&oldid=2523965
# /wiki/Special:GetFCtrStats/=Category%3APeople
# /wiki/Special:SwitchSkin/vector/Category%3APeople
# ]
# loop through the links and get peope url

def find_next_url(link):
    """
    find the sub-pages for all people list
    """
    url = link
    result = []
    while True: 
        r = requests.get(url)
        soup = bsoup(r.text, "html.parser")
        url_list = [link.get('href') for link in soup.find_all(href=next_url)]
        url = 'http://imslp.org' + url_list[-1]
        print(url)
        result.append(url)
    return result

def find_people_url(url):
    r = requests.get(url)
    soup = bsoup(r.text, "html.parser")
    url_list = [link.get('href') for link in soup.find_all('a',class_='categorysubcatlink')]
    return url_list

def write_people_url():
    result = []
    for url in open('results/people_page_url.txt'):
        result = result + find_people_url(url)
    text = open("result.txt","w")
    for item in result:
        item = 'http://imslp.org'+item
        text.write("%s\n" % item)
        # TODO: add Id using oldid function
    text.close()
    print("total number of composer: ", len(result))

def find_next_score_url(url):
    """
    find the sub-page for score list
    """
    result = []
    while True:
        r = requests.get(url)
        soup = bsoup(r.text, "html.parser")
        url_list = [link.get('href') for link in soup.find_all('a',class_='categorypaginglink',string='next 200')]
        if url_list == []:
            break
        url = 'http://imslp.org' + url_list[-1]
        result.append(url)
    return result

def find_score_url(url):
    list_page = [url]
    r = requests.get(url)
    soup = bsoup(r.text, "html.parser")
    # add everything on the first page to the list
    result = soup.find_all('div', class_="jq-ui-tabs" )
    scores = result[0].find_all('a',class_='categorypagelink')
    url_list = [link.get('href') for link in scores]
    # check sub-page
    list_page = find_next_score_url(url)
    if list_page != []:
        for page in list_page:
            r = requests.get(page)
            soup = bsoup(r.text, "html.parser")
            url_list += [link.get('href') for link in soup.find_all('a',class_='categorypagelink')]
    return url_list

def write_score_url():
    text = open("result.txt","w")
    for url in open('results/composer_url.txt'):
        result = []
        print(url)
        result = find_score_url(url)
        for item in result:
            item = 'http://imslp.org'+item
            text.write("%s\n" % item)
        # TODO: add Id using oldid function
    text.close()


def create_composer_dir():
    for url in open('results/composer_url.txt'):
        parent = 'composer/'+url[31:-1]
        print('write into: ', parent)
        score_links = find_score_url(url)

        for url in score_links:
            piecename = url[6:url.find('(')]
            path = os.path.join(parent, piecename)
            print('final dir:',path)
            os.makedirs(path, exist_ok=True)
            completeName = os.path.join(path, "html.txt")         
            file1 = open(completeName, "wb")
            r = requests.get('http://imslp.org'+url)
            file1.write(r.text.encode('utf-8'))
            file1.close()

        # write a script to save pieces
        piece = parent + '/pieces.txt'
        text = open(piece,"wb")
        for item in score_links:
            item = 'http://imslp.org'+item
            text.write("%s\n" % item)
        text.close()


def parse_data():
    for url in open('results/composer_url.txt'):
        parent = 'composer/'+url[31:-1]
        for url in score_links:
            piecename = url[6:url.find('(')]
            path = os.path.join(parent, piecename)
            completeName = os.path.join(path, "html.txt")     
            text = open(completeName, "r")  
            soup = bsoup(text.read(), "html.parser")
            # get ID and size
            result = soup.find_all('span', class_='we_file_info2')
            for piece in result:
                a = piece.find_all(string=True)
                fileID = a[1]
                filesize = a[2][3:a.find(",")]
            # 

    

# def create_piece_dir():
#     for url in open('results/composer_url.txt'):
#         path = '/Users/CarrieYang/Desktop/score_scrape/composer/'+url[31:-1]+



if __name__=='__main__':
    # # find all the links for different pages
    # link = 'http://imslp.org/wiki/Category:Composers'
    # find_next_url(link)
    create_composer_dir()