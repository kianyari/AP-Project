import requests
from bs4 import BeautifulSoup

url = "https://www.sheypoor.com/s/iran?q=%D8%A7%DB%8C%D9%81%D9%88%D9%86%2013"

s = requests.Session()
s.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'
r = s.get(url)

soup = BeautifulSoup(r.text, "lxml")

contents = soup.find_all("div", class_= "content")

for content in contents:
    a_tag = content.find("a")
    print(a_tag.get('href')) # link
    print(a_tag.text.strip()) # name
    print(a_tag)
    try:
        price = content.find("strong", class_= "item-price").text
    except:
        price = "قیمت توافقی"
    print(price)
    
    print("---------------------------------------------------------------------------------")