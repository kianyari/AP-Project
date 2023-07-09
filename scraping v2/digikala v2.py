import requests
from bs4 import BeautifulSoup
import pandas as pd
import urllib
from requests_html import HTMLSession
# data-intrack-useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"

search_input = input()
search_input = search_input.replace(" ", "%20")
saerch_url = "https://www.digikala.com/search/?q=" + search_input
print(saerch_url)


session = HTMLSession()
page = session.get('https://python.org/')


# saerch_url = urllib.request.urlopen(saerch_url).read()
# page = requests.get(saerch_url)
soup = BeautifulSoup(page.text, "lxml")
# print(soup.prettify())

product_url = soup.find_all("a", class_ = "d-block pointer pos-relative bg-000 overflow-hidden grow-1 py-3 px-4 px-2-lg h-full-md styles_VerticalProductCard--hover__ud7aD")



# raw_names = soup.find_all("div", class_ = "coin-name")
# row_data.append('https://maktabkhooneh.org' + course.find('a', class_ = 'course-card__wrapper')['href'])

print(product_url)
