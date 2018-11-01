import requests
from bs4 import BeautifulSoup

def test_spider(max_pages):
    page = 0
    counter =0
    while page < max_pages:
        url = 'https://losangeles.craigslist.org/search/sss?query=ps4&s=' + str(page*120)
        source_code = requests.get(url)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, "html.parser")
        for link in soup.findAll('a', {'class': 'result-title hdrlnk' }):
            href = link.get('href')
            title = link.string
            #print(href)
            #print(title)
            get_single_item_desc(href, counter)
            counter += 1
        page+=1


def get_single_item_desc(item_url, counter):
    source_code = requests.get(item_url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, "html.parser")
    for link in soup.findAll('span', {'id': 'titletextonly'}):
        href = link.get('href')
        title = link.string
        # print(href)
        print(counter,title)
        counter += 1


test_spider(1)