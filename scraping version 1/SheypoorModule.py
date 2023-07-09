from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Sheypoor():
    driver = webdriver.Chrome("chromedriver")
    driver.minimize_window()
    wait = WebDriverWait(driver, 20)
    
    @classmethod
    def search(cls, search_for):
        search_for = "search/?q=" + '%20'.join(search_for.split())
        cls.driver.get("https://www.sheypoor.com/s/iran?q=" + search_for)
        
        products = {}
        
        for i in range(1, 21):
            name = cls.wait.until(EC.element_to_be_clickable((By.XPATH, f'/html/body/main/section[3]/div/div/div/article[{i}]/div[2]/h2/a'))).text
            price = cls.wait.until(EC.element_to_be_clickable((By.XPATH, f'/html/body/main/section[3]/div/div/div/article[{i}]/div[2]/div/p/strong'))).text
            click_path = f'/html/body/main/section[3]/div/div/div/article[{i}]/div[2]/h2/a'
            products[name] = [price, click_path]
        return products
    
    @classmethod
    def click_product(cls, path):
        cls.wait.until(EC.element_to_be_clickable((By.XPATH, path))).click()
    