from bs4 import BeautifulSoup
import re

header = ['Title', 'Author', 'ID', 'Date_updated', 'Rating', 'Pairing', 'Warning', 'Complete', 'Language', 'Word_count', 'Num_chapters', 'Num_comments', 'Num_kudos', 'Num_bookmarks', 'Num_hits']
with open('SomeName.csv','w', encoding='utf8') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    

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

    for article in bs.find_all('li', {'role':'article'}):
        titles.append(article.find('h4', {'class':'heading'}).find('a').text)
        try:
            authors.append(article.find('a', {'rel':'author'}).text)
        except:
            authors.append('Anonymous')
        ids.append(article.find('h4', {'class':'heading'}).find('a').get('href')[7:])
        date_updated.append(article.find('p', {'class':'datetime'}).text)
        ratings.append(article.find('span', {'class':re.compile(r'rating\-.*rating')}).text)
        pairings.append(article.find('span', {'class':re.compile(r'category\-.*category')}).text)
        warnings.append(article.find('span', {'class':re.compile(r'warning\-.*warnings')}).text)
        complete.append(article.find('span', {'class':re.compile(r'complete\-.*iswip')}).text)
        languages.append(article.find('dd', {'class':'language'}).text)
        count = article.find('dd', {'class':'words'}).text
        if len(count) > 0:
            word_count.append(count)
        else:
            word_count.append('0')
        chapters.append(article.find('dd', {'class':'chapters'}).text.split('/')[0])
        try:
            comments.append(article.find('dd', {'class':'comments'}).text)
        except:
            comments.append('0')
        try:
            kudos.append(article.find('dd', {'class':'kudos'}).text)
        except:
            kudos.append('0')
        try:
            bookmarks.append(article.find('dd', {'class':'bookmarks'}).text)
        except:
            bookmarks.append('0')
        try:
            hits.append(article.find('dd', {'class':'hits'}).text)
        except:
            hits.append('0')

    df = pd.DataFrame(list(zip(titles, authors, ids, date_updated, ratings, pairings,\
                              warnings, complete, languages, word_count, chapters,\
                               comments, kudos, bookmarks, hits)))
    
    print('Successfully processed', len(df), 'rows!')
    
    with open('SomeName.csv','a', encoding='utf8') as f:
        df.to_csv(f, header=False, index=False)
    temp = pd.read_csv('SomeName.csv')
    print('Now we have a total of', len(temp), 'rows of data!')
    print('================================')
    
    
    def get_tags(article):
    tags = []
    for child in article.find('ul', {'class':'tags commas'}).children:
        if isinstance(child, NavigableString):
            pass
        else:
            tags.append(child.text.strip())
    return ', '.join(tags)

def get_summary(article):
    try:
        out = article.find('blockquote', {'class':'userstuff summary'}).text.strip()
        return out
    except:
        return ''
        

def open_fic(work_id, headers):
    url = 'https://archiveofourown.org' + work_id + '?view_adult=true&show_comments=true&view_full_work=true'
    req = urllib.request.Request(url, headers=headers)
    resp = urllib.request.urlopen(req)
    print('Successfully opened fiction:', url)
    bs = BeautifulSoup(resp, 'lxml')
    time.sleep(5)
    return bs

# when there's one or none page of comments
def compile_comments(bs):
    comments = bs.find_all('li', {'class':'comment group odd'}) # only include comments on the first level (no replies)
    l_comments = []
    if len(comments) > 0:
        for i in comments:
            l_comments.append(i.blockquote.text.strip())
        return '+++'.join(l_comments)
    else:
        return ''

# when there are 2+ pages of comments
def turn_page_comments(bs, work_id, headers, start_page = 1):
    page_limit = int(bs.find('li', {'class':'next'}).previous_sibling.previous_sibling.text)
    print('** We have a total of', page_limit, 'pages of comments')
    out = ''
    for i in range(start_page, page_limit+1):
        url = 'https://archiveofourown.org' + work_id + '?page=' + str(i) + '&show_comments=true&view_adult=true&view_full_work=true'
        try:
            req = urllib.request.Request(url, headers=headers)
            resp = urllib.request.urlopen(req)
            bs = BeautifulSoup(resp, 'lxml')
            time.sleep(5)
            out += compile_comments(bs) + '+++'
        except urllib.error.HTTPError as e:
            if e.code == 429:
                print('---Too many requests when accessing COMMENTS---')
                print('We should start with this comment page later:', i)
                break
            raise
    return out
