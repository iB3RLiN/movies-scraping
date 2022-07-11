# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import csv
from itertools import zip_longest
import time
import random
from tqdm import tqdm
import pandas as pd
import numpy as np


page_number = 1
target = 'https://www.faselhd.pro/movies_top_views/page/'
timeWaiting = random.randrange(start=2, stop=6)
#src = result.content

page_movies_url = []

for movies_page in target:
    if page_number == 2:
        break
    time.sleep(timeWaiting)
    result = requests.get(target+str(page_number))
    soup = BeautifulSoup(result.text, 'html.parser')  # (src, "lxml")
    links = soup.find_all('div', class_="postDiv")
    page_number += 1
    for page in links:
        url = page.find('a').get('href')
        page_movies_url.append(url)

print('Page Links is ', page_movies_url)
print('len of Page is ', len(page_movies_url))


index_page = 0
titles = []
descriptions = []
movies_links = []

for movies in page_movies_url:
    if index_page == len(page_movies_url):
        break
    time.sleep(timeWaiting)
    result = requests.get(page_movies_url[index_page])
    soup = BeautifulSoup(result.text, 'html.parser')
    title = soup.find('div', class_='h1 title').get_text().replace('\n', '')
    titles.append(title)
    description = soup.find('div', class_="singleDesc").get_text().replace('\n', '')
    descriptions.append(description)
    link = soup.find('iframe').get('src')
    movies_links.append(link)
    index_page += 1
    print('------------------------------------')
    print('len of Page = ', len(page_movies_url))
    print('len of titles = ', len(titles))
    print('len of descriptions = ', len(descriptions))
    print('len of movies_links = ', len(movies_links))
    print('index page = ', index_page)

file_list = [titles, descriptions, movies_links]
exported = zip_longest(*file_list)
with open("test.csv", 'w', encoding='utf-8', newline = '') as my_file:
    write = csv.writer(my_file)
    write.writerow(["titles", 'descriptions', "links"])
    write.writerows(exported)
