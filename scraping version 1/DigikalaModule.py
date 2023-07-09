from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Digikala():
    driver = webdriver.Chrome("chromedriver")
    driver.minimize_window()
    wait = WebDriverWait(driver, 20)
    
    @classmethod
    def search(cls, search_for): 

        if len(cls.driver.window_handles) > 1:
            cls.driver.switch_to.window(cls.driver.window_handles[0])
            cls.driver.close()
            cls.driver.switch_to.window(cls.driver.window_handles[0])
            
        search_for = '%20'.join(search_for.split())
        search_for = "search/?q=" + search_for
        cls.driver.get("https://www.digikala.com/" + search_for)

        products = {}
        
        for i in range(1, 6):
            name = cls.wait.until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="ProductListPagesWrapper"]/section/div[2]/div[{i}]/a/div/article/div[2]/div[2]/div[2]/h3'))).text
            price = cls.wait.until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="ProductListPagesWrapper"]/section/div[2]/div[{i}]/a/div/article/div[2]/div[2]/div[4]/div[1]/div/span'))).text
            click_path = f'//*[@id="ProductListPagesWrapper"]/section/div[2]/div[{i}]/a/div/article/div[2]/div[2]/div[2]/h3'
            if len(price) < 4:
                price = cls.wait.until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="ProductListPagesWrapper"]/section/div[2]/div[{i}]/a/div/article/div[2]/div[2]/div[4]/div[1]/div[2]/span'))).text      
            products[name] = [price, click_path]
        
        return products
            
    @classmethod
    def click_product(cls, path):
        cls.wait.until(EC.element_to_be_clickable((By.XPATH, path))).click()
        
        cls.driver.switch_to.window(cls.driver.window_handles[1])
        
        details_dictionary = {}
        
        recommendation = {}
        
        for i in range(1, 6):
            key = cls.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, f"#specification > div.mt-4.grow-1 > div > div > div:nth-child({i}) > p"))).text
            value = cls.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, f"#specification > div.mt-4.grow-1 > div > div > div:nth-child({i}) > div > p"))).text
            details_dictionary[key] = value
        
        for i in range (1, 6):
            name = cls.wait.until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="__next"]/div[1]/div[2]/div[4]/div[2]/div[2]/div[5]/div/div[2]/a[{i}]/div/article/div[2]/div[2]/div[1]/h3'))).text
            price = cls.wait.until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="__next"]/div[1]/div[2]/div[4]/div[2]/div[2]/div[5]/div/div[2]/a[{i}]/div/article/div[2]/div[2]/div[3]/div[1]/div/span'))).text
            click_path = f'//*[@id="__next"]/div[1]/div[2]/div[4]/div[2]/div[2]/div[5]/div/div[2]/a[{i}]/div/article/div[2]/div[2]/div[1]/h3'
            recommendation[name] = [price, click_path]

        return details_dictionary, recommendation
    
    
    @classmethod
    def back(cls):
        cls.driver.close()
        cls.driver.switch_to.window(cls.driver.window_handles[0])