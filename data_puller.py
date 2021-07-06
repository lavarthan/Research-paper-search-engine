import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep


def get_results(page):
    resp = requests.get(
        'https://pureportal.coventry.ac.uk/en/publications/?search=&pageSize=100&format=&page={}'.format(page))
    soup = BeautifulSoup(resp.content, 'html.parser')
    results = soup.find_all('div', attrs={'class': 'result-container'})
    return results


def get_title(result):
    return result.h3.text.strip()


def get_title_link(result):
    return result.h3.a['href']


def get_date(result):
    return result.find('span', attrs={'class': 'date'}).text


def get_authors(result):
    uni_authors = [i.text.strip() for i in result.find_all('a', attrs={'rel': 'Person'})]
    uni_authors_profile = [i['href'] for i in result.find_all('a', attrs={'rel': 'Person'})]
    temp = sum([i.strip().split('.,') for i in
                result.text.strip().split('\n')[0].split(publish_date)[0].replace(title, '').strip().split('&')], [])
    all_authors = []
    for i in temp:
        if i != '':
            if i.strip()[-1] == '.':
                all_authors.append(i.strip())
            else:
                all_authors.append(i.strip() + '.')
    non_uni_authors = [elem.strip() for elem in all_authors if elem not in uni_authors and elem != '.']

    authors = []
    for i in range(len(uni_authors)):
        authors.append(uni_authors[i] + ' => ' + uni_authors_profile[i])
    authors += non_uni_authors

    return authors


data = []
error = []
for page in range(10, 284):
    print(page, 'going')
    results = get_results(page)
    for x in results:
        try:
            title = get_title(x)
            publish_date = get_date(x)
            title_link = get_title_link(x)
            authors = get_authors(x)
            data.append([title, publish_date, title_link, authors])
        except:
            title = get_title(x)
            error.append([page, title])

    sleep(1)
df = pd.DataFrame(data=data, columns=['Title', 'Published date', 'Link', 'Authors'])
df.to_csv('train_data/final.csv', index=False)
