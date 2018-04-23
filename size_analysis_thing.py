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
    for url in open('results/people_url.txt'):
        parent = 'results/composer/'+url[31:-1]
        piecetxt = os.path.join(parent,'pieces.txt')
        score_links = open(piecetxt)
        for url in score_links:
            piecename = url[22:url.find('(')]
            path = os.path.join(parent, piecename)
            completeName = os.path.join(path, "html.txt")
            print(completeName)
            text = open(completeName, "r")  
            soup = bsoup(text.read(), "html.parser")
            # get ID and size
            result = soup.find_all('span', class_='we_file_info2')
            for piece in result:
                a = piece.find_all(string=True)
                print(a)
                fileID = a[1]
                print("fileID is : ")
                print(fileID)


                runningFileSize = 0
                fileNumSize = 0
                filesize = 0
                tempSize = 0
                searchnum = 0
                tempSize = 'a'


                # get filesize, take care of possible ways it is stored in array a
                # MB might be in the same index w/ the number, or in the next index
                for i in range(0,len(a)):
                    if 'MB' in a[i][0:2]:
                        #this is if MB is at the beginning of the thing in a, in case it's not in sm index
                        filesize = a[i-1]

                #below works only if nice, first iterate thru a
                    elif 'MB' in a[i]:
                        for let in range(0,len(a[i])):
                            if a[i][let].isdigit():
                                searchNum = a[i][let]
                        tempSize = a[i]
                        filesize = tempSize[tempSize.find(searchNum):tempSize.find('M')]

                    else:
                        filesize = a[2][3:a[2].find(",")] #will prob include the MB
                        filesize = filesize[:-2] #chop off the 'MB' from the string
                    print("filesize is: ")
                    print(filesize)

                fileNumSize = float(filesize)
                runningFileSize += fileNumSize
    return runningFileSize

getSizes()