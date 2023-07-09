import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

class Sheypoor:
    """
    in this website every information that we need is static
    use requests and bs4 module to find the elements that we need
    """
    @staticmethod
    def search(search_for):
        url = "https://www.sheypoor.com/s/iran?q=" + "%20".join(search_for.split())
        s = requests.Session()
        s.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'
        r = s.get(url)
        products = {
            "name": [],
            "price": [],
            "url": [],
        }
        
        soup = BeautifulSoup(r.text, "lxml")
        try:
            contents = soup.find_all("div", class_="content") # class content include name and price and url
        except:
            return products
        
        
        for content in contents:
            name = content.find("a").text.strip() # to get product name
            try:
                price = content.find("strong", class_="item-price").text # to get product price
            except:
                price = "قیمت توافقی"
            
            url = content.find("a").get('href') # to get product url 
            products["name"].append(name)
            products["price"].append(price)
            products["url"].append(url)

        df = pd.DataFrame(products)
        return df
    
    @staticmethod
    def click(url):
        """go to the product webpage"""
        driver = webdriver.Chrome("chromedriver")
        driver.get(url)

