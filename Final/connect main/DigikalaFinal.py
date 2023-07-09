from selenium import webdriver
import requests
import json
import pandas as pd
import Category

class Digikala():
    """
    search what user searched in the main window in the divar and get 6 results
    using one-api website to get token and api links to scrape website
    """
    token = "375404:64a0dcb8b94cc"
    
    @classmethod
    def search(cls, product):
        """
        1.get user input as argument
        2.create the url
        3.translate the url with requests module
        4.create the json file
        5.query on json file -> count: 6 products (max)
        """
        product = "%20".join(product.split()) # create the url
        # get the url info with requests module -> using one-api website
        search_result = requests.get(f'https://one-api.ir/digikala/?token={cls.token}&action=search&q={product}&page=1')
        search_result = json.dumps(search_result.json(), indent=2) # create the json file to query on it
        search_result =json.loads(search_result)
        products = {
            "name": [],
            "price": [],
            "url": [],
            "id": [],
            "category_id": [],
        }
        
        # find name, price, post id -> create the url, category id
        for i in range(6):
            try:
                name = search_result["result"][i]["title_fa"]
                price = search_result["result"][i]["price"]["selling_price"]
                product_id = search_result["result"][i]["id"]
                category_id = search_result["result"][i]["category_id"]
                url = "https://www.digikala.com/product/dkp-" + str(product_id) +'/' + name
                products["name"].append(name)
                products["price"].append(price)
                products["id"].append(product_id)
                products["category_id"].append(category_id)
                products["url"].append(url)

                # get the photo of digikala website and save it into our database
                with open(f"image src/{name}.jpg", "wb") as f:
                    f.write(requests.get(search_result["result"][i]["images"]["main"]).content)
            except:
                pass
        
        df = pd.DataFrame(data= products) # create the df of information of divar
        return df


    @classmethod
    def details(cls, product_id):
        """
        get details of each product
        similar to scrape user search
        create url and convert it to json file and query in it
        """
        details = {}
        result = requests.get(f'https://one-api.ir/digikala/?token={cls.token}&action=product_specifications&id={product_id}')
        result = json.dumps(result.json(), indent=2)
        result =json.loads(result)
        
        for i in range(len(result["result"][0]["attributes"])):
            details[result["result"][0]["attributes"][i]["title"]] = ' '.join(result["result"][0]["attributes"][i]["values"])
                    
        return details
    
    
    @classmethod
    def add_category(cls, selected_product, category_name):
        """
        add product dynamic
        1.if we have the category that user wants of us we add product to it
        2.find the 15 similar product category and create the new category
        in this case product id will help us
        """
        if category_name in Category.categoryWindow.category_names:
            selected_category = pd.read_csv(f"category/{category_name}.csv", index_col=0)
            merged_category = pd.concat([selected_category, selected_product], axis=0)
            merged_category.to_csv(f"category/{category_name}.csv")
            return
        Category.categoryWindow.category_names.append(category_name)
        result = requests.get(f'https://one-api.ir/digikala/?token={cls.token}&action=compare_search&id={selected_product.id}&page=1')
        result = json.dumps(result.json(), indent=2)
        result =json.loads(result)
        
        products = {
            "name": [],
            "price": [],
            "url": [],
            "id": [],
            "category_id": [],
        }
        
        for i in range(15):
            name = result["result"][i]["title_fa"]
            price = result["result"][i]["price"]["selling_price"]
            product_id = result["result"][i]["id"]
            category_id = result["result"][i]["category_id"]
            url = "https://www.digikala.com/product/dkp-" + str(product_id) +'/' + name
            products["name"].append(name)
            products["price"].append(price)
            products["id"].append(product_id)
            products["category_id"].append(category_id)
            products["url"].append(url)
            try:
                with open(f"category/img/{name}.png", "wb") as f:
                    f.write(requests.get(result["result"][i]["images"]["main"]).content)
            except:
                pass      
        selected_category = pd.DataFrame(data= products)
        selected_category.reset_index(inplace=True)
        selected_category.to_csv(f"category/{category_name}.csv", index=False)
        
    
    @staticmethod
    def click(url):
        """go to the url of product using webdriver module"""
        driver = webdriver.Chrome("chromedriver")
        driver.get(url)

