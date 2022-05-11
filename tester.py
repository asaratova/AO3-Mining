
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re
import urllib.request
import requests
import time

url = "https://archiveofourown.org/tags/Birds%20of%20Prey%20(TV)/works?page="
page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser")
results = soup.find(id="main")
workNum = []
page_elements = results.find_all("div", class_="work index group")
for item in page_elements:
    elem = item.find("h2", class_="id")
    print(elem)
    page_elements.append(elem)
    time.sleep(5)


headers = {'user-agent': 'Chrome/99.0.4844.82 (Lenovo; IdeaPad 5 15IIL05)'}
req = Request(url, headers)
html_page = urlopen(req)

soup = BeautifulSoup(html_page, "lxml")

links = []
for link in soup.findAll('a'):
    links.append(link.get('href'))

print(links)
