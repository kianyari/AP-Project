from selenium import webdriver
import requests
import json
import pandas as pd


class Divar():
    """
    search what user searched in the main window in the divar and get 20 results
    find the information using api -> to find correct api we use the Postman website 
    """
    @staticmethod
    def search(search_for):
        """
        1.get user input as argument
        2.create the url
        3.translate the url with requests module
        4.create the json file
        5.query on json file -> count: 20 products (max)
        """
        search_for = '%20'.join(search_for.split()) # create the url of product
        # get the url info with requests module
        result = requests.get(f"https://api.divar.ir/v8/web-search/tehran?goods-business-type=all&q={search_for}")
        result = json.dumps(result.json(), indent=2) # create the json file to query on it
        result =json.loads(result)
        
        products = {
            "name":[],
            "price": [],
            "url": [],
        }

        # find name, price, post token, url with query on json file
        for i in range(1, 21):
            try:
                name = result['web_widgets']['post_list'][i]['data']['title']
                price = result['web_widgets']['post_list'][i]['data']['middle_description_text']
                token = result['web_widgets']['post_list'][i]['data']['token']
                url = "https://divar.ir/v/" + token
                
                products["name"].append(name)
                products["price"].append(price)
                products["url"].append(url)

            # if we hit error or sth
            except:
                pass

        df = pd.DataFrame(products) # create the df of information of divar
        return df
        
    @staticmethod
    def click(url):
        """go to the url of product using webdriver module"""
        driver = webdriver.Chrome("chromedriver")
        driver.get(url)

