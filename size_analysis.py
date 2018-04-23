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

def getSizes():
    runningFileSize = 0
    fileNumSize = 0
    filesize = 0
    for url in open('results/people_url.txt'):
        parent = 'results/composer/'+url[31:-1]
        piecetxt = os.path.join(parent,'pieces.txt')
        try:
            with open(piecetxt) as score_links:
                for url in score_links:
                    piecename = url[22:url.find('(')]
                    path = os.path.join(parent, piecename)
                    completeName = os.path.join(path, "html.txt")     
                    print(completeName)
                    try:
                        with open(completeName, "r") as text:
                            soup = bsoup(text.read(), "html.parser")
                            # get ID and size
                            result = soup.find_all('span', class_='we_file_info2')
                            for piece in result:
                                a = piece.find_all(string=True)
                                print(a)
                                fileID = a[1]
                                print("fileID is : ",fileID)
                                if 'MB' in a[4][0:2]:
                                    filesize = a[3]
                                elif a[2] == ' ' :
                                    if a[3] == ' - ':
                                        filesize = a[4]
                                    else:
                                        filesize = a[3][3:a[2].find(",")]
                                        filesize = filesize[0:filesize.find('M')]
                                else:
                                    filesize = a[2][3:a[2].find(",")] #will prob include the MB
                                    filesize = filesize[0:filesize.find('M')]
                    except Exception:
                        print('not found')
                    fileNumSize = float(filesize)
                    print("filesize is: ",fileNumSize)
                    runningFileSize += fileNumSize
                    print("full size is: ", runningFileSize)
        except Exception:
            print('not found')



                # get filesize, take care of possible ways it is stored in array a
                # MB might be in the same index w/ the number, or in the next index
                # for i in range(0,len(a)):
                #     print('loop')
                #     if 'MB' in a[i][0:2]:
                #         #this is if MB is at the beginning of the thing in a, in case it's not in sm index
                #         filesize = a[i-1]
                #     #below works only if nice, first iterate thru a
                #     else:
                #         filesize = a[2][3:a[2].find(",")] #will prob include the MB
                #         filesize = filesize[0:filesize.find('M')] #chop off the 'MB' from the string

    return runningFileSize
getSizes()
