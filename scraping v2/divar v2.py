# import time
# search_input = input()
# search_input = search_input.replace(" ", "%20")
# saerch_url = "https://divar.ir/s/tehran?q=" + search_input
# print(saerch_url)
# start = time.time()
from selenium import webdriver 
from bs4 import BeautifulSoup
from time import sleep
saerch_url = "https://divar.ir/s/tehran/mobile-phones?q=iphone%2013"
driver = webdriver.Chrome("chromedriver") 
driver.get(saerch_url)
# sleep(3)
html = driver.page_source

soup = BeautifulSoup(html, "html.parser")
# print(soup.prettify())

names_divar = soup.find_all("h2", class_= "kt-post-card__title")
url_divar = soup.find_all("a", class_= "")

print(len(names_divar))
for i in names_divar:
    print(i.text)
for i in url_divar:
    # if i[:2] == "/v":
    if i.get("href").startswith("/v"):
        print("https://divar.ir" + i.get("href"))

stop = time.time()

print(stop-start)

# product_url = soup.find_all("a", class_ = "d-block pointer pos-relative bg-000 overflow-hidden grow-1 py-3 px-4 px-2-lg h-full-md styles_VerticalProductCard--hover__ud7aD")
# for i in product_url:
#     print(i.get("href"))
# print(product_url)
