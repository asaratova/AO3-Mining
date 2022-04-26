# Creating a basis for scraping
import urllib.request

import requests
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
import csv
import time

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


def getIds():
    url = 'https://archiveofourown.org/tags/Birds%20of%20Prey%20(TV)/works?page='
    workName = []
    ids = []
    end_page = 2
    print("In get contents")
    for i in range(1, end_page):
        print(i)
        url = url+str(i)
        page = requests.get(url)
        # print(page.content)
        soup = BeautifulSoup(page.content)
        results = soup.find("div", {"class": "works-index filtered region"})

        newResults = results.find_all("ol", {"class": "work index group"})

        for article in results.find_all('li', {'role': 'article'}):
            workName.append(article.find(
                'h4', {'class': 'heading'}).find('a').text)
            ids.append(article.find('h4', {'class': 'heading'}).find(
                'a').get('href')[7:])
        time.sleep(5)
    return ids


def getPageInfo(url, id):
    page = requests.get(url)
    soup = BeautifulSoup(page.content)
    results = soup.find("div", {"class": "workskin"})
    # content = results.find('div', {'id': 'chapters'})
    someText = str(id) + ".txt"
    content = soup.find('div', {'id': 'chapters'}).text.strip()
    print(content)
    language = soup.find('dd', {'class': 'language'}).text
    if language == "en-US":
        with open(someText, 'w') as f:
            for item in content:
                f.write(item)
            f.write("\n")
            f.close()
    else:
        return "not in English"


def process_basic(page_content):
    bs = BeautifulSoup(page_content, 'lxml')
    titles = []
    authors = []
    ids = []
    date_updated = []
    ratings = []
    pairings = []
    warnings = []
    complete = []
    languages = []
    word_count = []
    chapters = []
    comments = []
    kudos = []
    bookmarks = []
    hits = []

    for article in bs.find_all('li', {'role': 'article'}):
        titles.append(article.find('h4', {'class': 'heading'}).find('a').text)
        try:
            authors.append(article.find('a', {'rel': 'author'}).text)
        except:
            authors.append('Anonymous')
        ids.append(article.find('h4', {'class': 'heading'}).find(
            'a').get('href')[7:])
        date_updated.append(article.find('p', {'class': 'datetime'}).text)
        ratings.append(article.find(
            'span', {'class': re.compile(r'rating\-.*rating')}).text)
        pairings.append(article.find(
            'span', {'class': re.compile(r'category\-.*category')}).text)
        warnings.append(article.find(
            'span', {'class': re.compile(r'warning\-.*warnings')}).text)
        complete.append(article.find(
            'span', {'class': re.compile(r'complete\-.*iswip')}).text)
        languages.append(article.find('dd', {'class': 'language'}).text)
        count = article.find('dd', {'class': 'words'}).text
        if len(count) > 0:
            word_count.append(count)
        else:
            word_count.append('0')
        chapters.append(article.find(
            'dd', {'class': 'chapters'}).text.split('/')[0])
        try:
            comments.append(article.find('dd', {'class': 'comments'}).text)
        except:
            comments.append('0')
        try:
            kudos.append(article.find('dd', {'class': 'kudos'}).text)
        except:
            kudos.append('0')
        try:
            bookmarks.append(article.find('dd', {'class': 'bookmarks'}).text)
        except:
            bookmarks.append('0')
        try:
            hits.append(article.find('dd', {'class': 'hits'}).text)
        except:
            hits.append('0')

    df = pd.DataFrame(list(zip(titles, authors, ids, date_updated, ratings, pairings,
                               warnings, complete, languages, word_count, chapters,
                               comments, kudos, bookmarks, hits)))

    print('Successfully processed', len(df), 'rows!')

    with open('SomeName.csv', 'a', encoding='utf8') as f:
        df.to_csv(f, header=False, index=False)
    temp = pd.read_csv('SomeName.csv')
    print('Now we have a total of', len(temp), 'rows of data!')
    print('================================')


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


if __name__ == "__main__":
    main()
