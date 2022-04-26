# Creating a basis for scraping
import urllib.request

import requests
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
import csv
import time
import pandas as pd
from bs4 import BeautifulSoup
import re

from html.parser import HTMLParser
import html5lib

import codecs


# this may give blank pages

session = requests.Session()
retry = Retry(connect=7, backoff_factor=5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

# insert header here like: headers = {'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15'}
headers = {'user-agent': 'Chrome/99.0.4844.82 (Lenovo; IdeaPad 5 15IIL05)'}
url = 'https://archiveofourown.org/tags/Birds%20of%20Prey%20(TV)/works?page='

req = urllib.request.Request(url, headers=headers)
resp = urllib.request.urlopen(req)
content = resp.read()
endpage = 0

# separator tags
# https://archiveofourown.org/works?work_search%5Bsort_column%5D=revised_at&work_search%5Bother_tag_names%5D=&exclude_work_search%5Bfreeform_ids%5D%5B%5D=110&exclude_work_search%5Bfreeform_ids%5D%5B%5D=176&exclude_work_search%5Bfreeform_ids%5D%5B%5D=2379&exclude_work_search%5Bfreeform_ids%5D%5B%5D=2026&exclude_work_search%5Bfreeform_ids%5D%5B%5D=62&work_search%5Bexcluded_tag_names%5D=&work_search%5Bcrossover%5D=&work_search%5Bcomplete%5D=&work_search%5Bwords_from%5D=&work_search%5Bwords_to%5D=&work_search%5Bdate_from%5D=&work_search%5Bdate_to%5D=&work_search%5Bquery%5D=&work_search%5Blanguage_id%5D=&commit=Sort+and+Filter&tag_id=Marvel
# https://archiveofourown.org/tags/Marvel/works?commit=Sort+and+Filter&exclude_work_search%5Bfreeform_ids%5D%5B%5D=110&exclude_work_search%5Bfreeform_ids%5D%5B%5D=176&exclude_work_search%5Bfreeform_ids%5D%5B%5D=2379&exclude_work_search%5Bfreeform_ids%5D%5B%5D=2026&exclude_work_search%5Bfreeform_ids%5D%5B%5D=62&page=2&work_search%5Bcomplete%5D=&work_search%5Bcrossover%5D=&work_search%5Bdate_from%5D=&work_search%5Bdate_to%5D=&work_search%5Bexcluded_tag_names%5D=&work_search%5Blanguage_id%5D=&work_search%5Bother_tag_names%5D=&work_search%5Bquery%5D=&work_search%5Bsort_column%5D=revised_at&work_search%5Bwords_from%5D=&work_search%5Bwords_to%5D=


def getIds():
    url = 'https://archiveofourown.org/tags/Marvel/works?commit=Sort+and+Filter&exclude_work_search%5Bfreeform_ids%5D%5B%5D=110&exclude_work_search%5Bfreeform_ids%5D%5B%5D=176&exclude_work_search%5Bfreeform_ids%5D%5B%5D=2379&exclude_work_search%5Bfreeform_ids%5D%5B%5D=2026&exclude_work_search%5Bfreeform_ids%5D%5B%5D=62&page='
    secondurl = '&page=2&work_search%5Bcomplete%5D=&work_search%5Bcrossover%5D=&work_search%5Bdate_from%5D=&work_search%5Bdate_to%5D=&work_search%5Bexcluded_tag_names%5D=&work_search%5Blanguage_id%5D=&work_search%5Bother_tag_names%5D=&work_search%5Bquery%5D=&work_search%5Bsort_column%5D=revised_at&work_search%5Bwords_from%5D=&work_search%5Bwords_to%5D='
    workName = []
    ids = []
    start_page = 4
    end_page = 6
    print("In get contents")
    for i in range(start_page, end_page):
        print(len(ids))
        url = url+str(i)+secondurl
        page = requests.get(url)
        # print(page.content)
        soup = BeautifulSoup(page.content)
        # ids.append(article.find('h4', {'class':'heading'}).find('a').get('href')[7:])
        for article in soup.find_all('li', {'role': 'article'}):
            item = article.find('h4', {'class': 'heading'}).find(
                'a').get('href')[7:]
            if item is not None:
                ids.append(item)
    return ids


def getPageInfo(url, id):
    page = requests.get(url)
    soup = BeautifulSoup(page.content)
    results = soup.find("div", {"class": "workskin"})
    # content = results.find('div', {'id': 'chapters'})
    someText = str(id) + ".txt"
    content = soup.find('div', {'id': 'chapters'})
    #language = soup.find('dd', {'class': 'language'}).text
    relationship = soup.find('dd', {'class': 'relationship tags'})
    freeform = soup.find('dd', {'class': 'freeform tags'})
    fandom = soup.find('dd', {'class': 'relationship tags'})
    if content is not None:
        content = content.text.strip()
        with open(someText, 'w', encoding="utf-8") as f:
            for item in content:
                f.write(item)
            f.write("\n")
            f.write("[starting tags]")
            f.write("\n")
            f.write("relationship: ")
            try:
                for i in relationship.text:
                    f.write(i)
            except:
                f.write("None")
            f.write("\n")
            f.write("freeform: ")
            try:
                for i in freeform.text:
                    f.write(i)

            except:
                f.write("None")
            f.write("\n")
            f.write("fandom: ")
            try:
                for i in fandom.text:
                    f.write(i)

            except:
                f.write("None")
            f.write("\n")
            f.close()
    time.sleep(5)


def get_tags(article):
    tags = []
    for child in article.find('ul', {'class': 'tags commas'}).children:
        if isinstance(child, NavigableString):
            pass
        else:
            tags.append(child.text.strip())
    return ', '.join(tags)


def get_summary(article):
    try:
        out = article.find(
            'blockquote', {'class': 'userstuff summary'}).text.strip()
        return out
    except:
        return ''


def open_fic(work_id, headers):
    url = 'https://archiveofourown.org' + work_id + \
        '?view_adult=true&show_comments=true&view_full_work=true'
    req = urllib.request.Request(url, headers=headers)
    resp = urllib.request.urlopen(req)
    print('Successfully opened fiction:', url)
    bs = BeautifulSoup(resp, 'lxml')
    time.sleep(5)
    return bs

# when there's one or none page of comments


def main():
    header = ['Title', 'Author', 'ID', 'Date_updated', 'Rating', 'Pairing', 'Warning', 'Complete',
              'Language', 'Word_count', 'Num_chapters', 'Num_comments', 'Num_kudos', 'Num_bookmarks', 'Num_hits']
    with open('SomeName.csv', 'w', encoding='utf8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
    print("In main requesting")
    # getContent('https://archiveofourown.org/tags/Birds%20of%20Prey%20(TV)/works?page=', 1, 5)

    ids = getIds()
    for i in range(1, len(ids)):
        pageName = 'https://archiveofourown.org/works/' + \
            str(ids[i]) + '?view_adult=true'
        getPageInfo(pageName, ids[i])
        # process_basic(pageName)


if __name__ == "__main__":
    main()
