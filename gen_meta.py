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
    
def find_next_url(link = 'http://imslp.org/wiki/Category:Composers', debug=False):
    """
    This function takes in two arguments:
    1) link, the link of the page that we want to parse
    2) debug, a boolean indicates whether we want to debug. If true, write
                out the result into a file name "results/people_subpage.txt"

    This function returns a list of url, which are subpages of the people page.
    """
    url = link
    result = []
    while True: 
        r = requests.get(url)
        soup = bsoup(r.text, "html.parser")
        url_list = [link.get('href') for link in soup.find_all(href=next_url)]
        if url_list == []:
            break
        url = 'http://imslp.org' + url_list[-1]
        result.append(url)

    # write result into a file
    if debug == True:
        text = open("results/people_subpage.txt","w")
        text.write("%s\n" % link)
        for item in result[:-1]:
            text.write("%s\n" % item)
        text.close()

    return result[:-1]

def find_people_url(url):
    """
    Helper function for write_people_url.
    """
    r = requests.get(url)
    soup = bsoup(r.text, "html.parser")
    url_list = [link.get('href') for link in soup.find_all('a',class_='categorysubcatlink')]
    return url_list

def write_people_url():
    """
    This function generate a file with list of all composer urls
    """
    result = []
    for url in open('results/people_subpage.txt'):
        result = result + find_people_url(url)
    text = open("results/people_url.txt","w")
    for item in result[4:]:
        item = 'http://imslp.org'+item
        text.write("%s\n" % item)
    text.close()
    print("total number of composer: ", len(result))

def find_next_score_url(url):
    """
    Helper function for find_score_url
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
    """
    This function takes in one arguments:
    1) url, a composer url page to parse
    This function returns a list of piece url for a specific composer.
    """
    list_page = [url]
    r = requests.get(url)
    soup = bsoup(r.text, "html.parser")
    # add everything on the first page to the list
    result = soup.find_all('div', class_="jq-ui-tabs" )
    if result == []:
        return "badlink"
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
    """
    This function writes all score url into a file. 
    """
    text = open("result.txt","w")
    for url in open('results/people_url.txt'):
        result = []
        print(url)
        result = find_score_url(url)
        for item in result:
            item = 'http://imslp.org'+item
            text.write("%s\n" % item)
        # TODO: add Id using oldid function
    text.close()

def create_dir():
    """
    This function create directory for each composer, 
    and for each composer, seperate score folder
    """
    badlinks = []
    for url in open('results/people_url.txt'):
        parent = 'results/composer/'+url[31:-1]
        print('write into: ', parent)
        score_links = find_score_url(url)
        if score_links == "badlink":
            badlinks += url
        elif score_links != []:
            for url in score_links:
                piecename = url[6:url.find('(')]
                path = os.path.join(parent, piecename)
                print('final dir:',path)
                os.makedirs(path, exist_ok=True)
                completeName = os.path.join(path, "html.txt")
                if os.path.exists(completeName):
                    continue
                file1 = open(completeName, "wb")
                r = requests.get('http://imslp.org'+url)
                file1.write(r.text.encode('utf-8'))
                file1.close()

            # # write a script to save pieces
            piece = 'pieces.txt'
            fullpath = os.path.join(parent, piece)
            if os.path.exists(fullpath):
                    continue
            text = open(fullpath,"w+")
            for item in score_links:
                item = 'http://imslp.org'+item
                text.write("%s\n" % item)
            text.close()
    print("badlinks:",badlinks)
    return badlinks
        # except:
        #     pass


def parse_data():
    for url in open('results/composer_url.txt'):
        parent = 'composer/'+url[31:-1]
        piecetxt = os.path.joint(parent,'pieces.txt')
        score_links = open(piecetxt)
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
    # # generate the list of subpages
    # find_next_url(debug=True)
    # write_people_url()
    create_dir()
