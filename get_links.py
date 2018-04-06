import lxml.html
import urllib
import requests
from urllib.request import urlopen
from urllib.parse import urljoin
import http.cookiejar
from bs4 import BeautifulSoup

def sort_pdf(base_url):
    paths = []
    # fetch the page
    res = urlopen(base_url)
    # parse the response into an xml tree
    tree = lxml.html.fromstring(res.read())
    # construct a namespace dictionary to pass to the xpath() call
    # this lets us use regular expressions in the xpath
    ns = {'re': 'http://exslt.org/regular-expressions'}
    # iterate over all <a> tags whose href ends in ".pdf" (case-insensitive)
    for node in tree.xpath('//a[re:test(@href, "\.pdf$", "i")]', namespaces=ns):
        path = urljoin(base_url, node.attrib['href'])
        paths.append(path)
        return paths

def download_file(url):
    local_filename = url.split('/')[-1]
    headers={'Cookie': 'imslpdisclaimeraccepted=yes'}

    # Login process
    login_url = 'https://imslp.org/index.php?title=Special:UserLogin&returnto=Main%20Page'
    s = requests.Session()
    r = s.get(login_url)
    cookies = dict(r.cookies)
    response = r.content
    soup = BeautifulSoup(response,"html.parser")
    token = soup.find("input",{"name":"wpLoginToken"})['value']
    payload = {
        'wpName': 'ttsai@g.hmc.edu',
        'wpPassword': 'ScoreData2018!',
        'wpLoginAttempt':'Log in',
        'wpLoginToken': token
    }
    login_url = 'https://imslp.org/index.php?title=Special:UserLogin&action=submitlogin&type=login&returnto=Main%20Page'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    p = s.post(login_url, data = payload, cookies=cookies)
    # print(p.text)
    # print(p.headers)
    cookies = requests.utils.dict_from_cookiejar(s.cookies)
    # print(cookies)
    composerurl = "http://imslp.org/wiki/Floating_Islands_(Aadler,_C._A.)"
    r = s.get(composerurl)
    text = open("test.html","w")
    text.write(r.text)
    text.close()
    # r = s.get(url, allow_redirects=True)
    # print(r.text)
    soup = BeautifulSoup(r.text)
    current_link = ''
    for link in soup.find_all('a'):
        current_link = link.get('href')
        if current_link != None and current_link.endswith('pdf'):
            print(current_link)
    current_link = 'http://imslp.org/wiki/Special:IMSLPDisclaimerAccept/88875'
    req = s.get(current_link)
    text = open("test.html","w")
    text.write(req.text)
    text.close()
    #print(req.text)
    # for r in r.history:
    #     print (r.status_code, r.url)

    with open(local_filename, 'wb') as f:
        for chunk in req.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
        return local_filename


if __name__=='__main__':
    base_url = "http://imslp.org/wiki/Floating_Islands_(Aadler,_C._A.)"
    paths = sort_pdf(base_url)
    for path in paths:
        download_file(path)


# http://ks.imslp.info/files/imglnks/usimg/c/cc/IMSLP299555-PMLP485142-AadlerCA_FloatingIslandsWaltz.pdf
# http://hz.imslp.info/files/imglnks/usimg/c/cc/IMSLP299555-PMLP485142-AadlerCA_FloatingIslandsWaltz.pdf
# https://imslp.org/wiki/Special:ImagefromIndex/299555/hfpn
# https://imslp.org/wiki/Special:ImagefromIndex/299555
# http://imslp.org/wiki/Special:IMSLPDisclaimerAccept/299555
