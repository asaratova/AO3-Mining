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
from collections import Counter

import os
import shutil

from html.parser import HTMLParser


# this may give blank pages

session = requests.Session()
retry = Retry(connect=7, backoff_factor=5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

# there was the possibility of needing headers, and the first url I used to test a lot of initial functions
#headers = {'user-agent': 'Chrome/99.0.4844.82 (Lenovo; IdeaPad 5 15IIL05)'}
#url = 'https://archiveofourown.org/tags/Birds%20of%20Prey%20(TV)/works?page='

#req = urllib.request.Request(url, headers=headers)
#resp = urllib.request.urlopen(req)
#content = resp.read()
#endpage = 0

# TO-DO: need to see why there are so many empty content IDs, may be in other function
# TO-DO: check what IDs spit out


def getIds(start_page, end_page):
    ''' this function parses through several pages, collecting 20 ids from each page
    The two urls are used as the initial template with the page number being squished in there to take us to the needed page
    This may need work on traversing through all the chapters
    '''
    original_url = "https://archiveofourown.org/tags/Harry%20Potter%20-%20J*d*%20K*d*%20Rowling/works?commit=Sort+and+Filter&page="
    second_url = "&work_search%5Bcomplete%5D=&work_search%5Bcrossover%5D=&work_search%5Bdate_from%5D=&work_search%5Bdate_to%5D=&work_search%5Bexcluded_tag_names%5D=&work_search%5Blanguage_id%5D=en&work_search%5Bother_tag_names%5D=&work_search%5Bquery%5D=&work_search%5Bsort_column%5D=hits&work_search%5Bwords_from%5D=&work_search%5Bwords_to%5D="
    ids = []
    print("In get contents")
    for page in range(start_page, end_page):
        print(len(ids))
        url = original_url+str(page)+second_url
        page = requests.get(url)
        # print(page.content)
        soup = BeautifulSoup(page.content, features="html.parser")
        # ids.append(article.find('h4', {'class':'heading'}).find('a').get('href')[7:])
        for article in soup.find_all('li', {'role': 'article'}):
            item = article.find('h4', {'class': 'heading'}).find(
                'a').get('href')[7:]
            if item is not None:
                ids.append(item)
    return ids


# TO-DO: see how untagged things are stored
# TO-DO: Explore one chapter vs multiple chapter fiction
# TO-DO: Double check that this is in the same place for all pages
def getPageInfo(url, id):
    ''' finds contents, and helpful tags associated, marking with category
    Gets first chapter and throws in in text file along with tags
    This needs try excepts because of None type issues
    '''
    print("\nURL: ", url)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, features="html.parser")
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
            max_lines = 5000
            cur_line = 0
            for item in content:
                if cur_line > max_lines:
                    break
                if item != "\n" or item != "":
                    f.write(item)
                    cur_line += 1
            f.write("\n")
            f.write("[starting tags]")
            f.write("\n")
            f.write("relationship: \n")
            try:
                for i in relationship.strings:
                    if i != "\n":
                        f.write(i + "\n")
            except:
                f.write("None")
            f.write("\n")
            f.write("freeform: \n")
            try:
                for i in freeform.strings:
                    if i != "\n":
                        f.write(i + "\n")

            except:
                f.write("None")
            f.write("\n")
            f.write("fandom: \n")
            try:
                for i in fandom.strings:
                    if i != "\n":
                        f.write(i + "\n")

            except:
                f.write("None")
            f.write("\n")
            f.close()

    print("Finished reading a file")
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
    '''This is either an exerpt from the fic, or an author's summary
    This may include something about how the author writes
    '''
    try:
        out = article.find(
            'blockquote', {'class': 'userstuff summary'}).text.strip()
        return out
    except:
        return ''


def open_fic(work_id, headers):
    ''' Processes unique work ID into a soup to use
    '''
    url = 'https://archiveofourown.org' + work_id + \
        '?view_adult=true&show_comments=true&view_full_work=true'
    req = urllib.request.Request(url, headers=headers)
    resp = urllib.request.urlopen(req)
    print('Successfully opened fiction:', url)
    bs = BeautifulSoup(resp, 'lxml')
    time.sleep(5)
    return bs


def main():
    # this part is not ready, might be eventually useful to consolidate info into one file
    # header = ['Title', 'Author', 'ID', 'Date_updated', 'Rating', 'Pairing', 'Warning', 'Complete',
    #          'Language', 'Word_count', 'Num_chapters', 'Num_comments', 'Num_kudos', 'Num_bookmarks', 'Num_hits']
    # with open('SomeName.csv', 'w', encoding='utf8') as f:
    #    writer = csv.writer(f)
    #    writer.writerow(header)

    # processing information on certain pages and then every work content is processed
    print("In main requesting")

    # Must start at 1
    start_id = 1
    end_id = 10

    ids = getIds(start_id, end_id)
    print(Counter(ids))
    for i in range(1, len(ids)):
        pageName = 'https://archiveofourown.org/works/' + \
            str(ids[i]) + '?view_adult=true'
        getPageInfo(pageName, ids[i])
        if i % 20 == 0:
            print(i)

    path = "./test_data"
    try:
        os.mkdir(path)
    except:
        print("Data directory already made.")

    first = True
    for root, dirs, files in os.walk("."):
        if first:
            for file in files:
                if file[-3:] == "txt" and "predictions" not in file and "results" not in file:
                    try:
                        shutil.move(root + "/" + file, path)
                    except:
                        print("File already exists")
        first = False


if __name__ == "__main__":
    main()
