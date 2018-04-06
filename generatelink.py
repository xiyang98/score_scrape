from requests import get
from urllib import parse
from os import path, getcwd
from bs4 import BeautifulSoup as soup
from sys import argv

def get_page(base_url):
    req= get(base_url)
    if req.status_code==200:
        return req.text
    raise Exception('Error {0}'.format(req.status_code))

def get_all_links(html):
    bs= soup(html)
    links= bs.findAll('a')
    return links

def download_file(url):
    local_filename = url.split('/')[-1]
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk:
                f.write(chunk)
    return local_filename

def get_pdf(base_url):
    html= get_page(base_url)
    links= get_all_links(html)
    print(links)
    if len(links)==0:
        raise Exception('No links found on the webpage')
    n_pdfs= 0
    for link in links:
        print (link['href'])
        if link['href'][-4:]=='.pdf':
            n_pdfs+= 1
            content= get(urljoin(base_url, link['href']))
            download_file(link)
    if n_pdfs==0:
        raise Exception('No pdfs found on the page')
    print ("{0} pdfs downloaded and saved in {1}".format(n_pdfs, base_dir))

if __name__=='__main__':
    url = "https://imslp.org/wiki/Violin_Concerto%2C_Op.77_(Brahms%2C_Johannes)"
    get_pdf(url)
