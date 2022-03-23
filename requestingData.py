# Creating a basis for scraping
import urllib.request
import scrapeData

import requests
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
import csv
import time


# this may give blank pages

session = requests.Session()
retry = Retry(connect=7, backoff_factor=5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

# insert header here like: headers = {'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15'}
headers = {'user-agent': 'Chrome/99.0.4844.82 (Lenovo; IdeaPad 5 15IIL05)'}
url = 'https://archiveofourown.org/tags/Bill%20Nye%20the%20Science%20Guy/works'

req = urllib.request.Request(url, headers=headers)
resp = urllib.request.urlopen(req)
content = resp.read()


def getContent(url, start_page=1, end_page=1):
    basic_url = url
    # should be of the form: "https://archiveofourown.org/tags/###TAG###/works?page="

    for i in range(start_page, end_page+1):
        url = basic_url+str(i)
        try:
            req = urllib.request.Request(url, headers=headers)
            resp = urllib.request.urlopen(req)
            pageName = "./SomeContent/"+str(i)+".html"
            with open(pageName, 'w') as f:
                f.write(resp.read().decode('utf-8'))
                print(pageName, end=" ")
            time.sleep(5)
        except urllib.error.HTTPError as e:
            if e.code == 429:
                print('Too many requests!---SLEEPING---')
                print('we should restart on page', i)
                print('we should restart with this url:', url)
                break
            raise


totalPages = 0
for i in range(1, totalPages+1):
    pageName = "./SomeContent/"+str(i)+".html"
    with open(pageName, mode='r', encoding='utf8') as f:
        print('Now we are opening page', i, '...')
        page = f.read()
        scrapeData.process_basic(page)
