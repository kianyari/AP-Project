from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep

class Divar():
    driver = webdriver.Chrome("chromedriver")
    driver.minimize_window()

    @classmethod
    def search(cls, search_for):
        search_for = "?q=" + '%20'.join(search_for.split())
        cls.driver.get("https://divar.ir/s/tehran" + search_for)
        html = cls.driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        
        products = {}
        names = soup.find_all("h2", class_= "kt-post-card__title")
        prices = soup.find_all("div", class_= "kt-post-card__description")
        url_divar = soup.find_all("a", class_= "")
        
        for name, price, url in zip(names, prices, url_divar):
            if url.get("href").startswith("/v"):
                products[name.text] = [price.text,"https://divar.ir" + url.get("href")]
        
        return products
        
    @classmethod
    def click_product(cls, url):
        cls.driver.get(url)
