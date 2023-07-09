from DigikalaModule import Digikala
from DivarModule import Divar
from SheypoorModule import Sheypoor
from threading import Thread
import pandas as pd
import difflib

class CustomThread(Thread):

    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None
 
    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)
             
    def join(self, *args):
        Thread.join(self, *args)
        return self._return


class Matching():
    
    @classmethod
    def search(cls, search_for):
        t1 = CustomThread(target=Digikala.search, args=(search_for,))
        t2 = CustomThread(target=Divar.search, args=(search_for,))
        t3 = CustomThread(target=Sheypoor.search, args=(search_for,))
        t1.start()
        t2.start()
        t3.start()
        search_digikala = t1.join()
        search_divar = t2.join()
        search_sheypoor = t3.join()
        
        matched_products = {
            "digikala price": [],
            "divar price": [],
            "sheypoor price": [],
            "digikala link": [],
            "divar link": [],
            "sheypoor link": [],
        }


        for item in search_digikala.keys():
            divar_name = difflib.get_close_matches(item, search_divar.keys(), 1, 0.1)
            Sheypoor_name = difflib.get_close_matches(item, search_sheypoor.keys(), 1, 0.1)
            divar_name = divar_name[0]
            Sheypoor_name = Sheypoor_name[0]
            matched_products["digikala price"].append(search_digikala[item][0])
            matched_products["digikala link"].append(search_digikala[item][1])
            matched_products["divar price"].append(search_divar[divar_name][0])
            matched_products["divar link"].append(search_divar[divar_name][1])
            matched_products["sheypoor price"].append(search_sheypoor[Sheypoor_name][0])
            matched_products["sheypoor link"].append(search_sheypoor[Sheypoor_name][1])
            
        df = pd.DataFrame(matched_products, index = list(search_digikala.keys()))
        
        return df
    
    @classmethod
    def search_recommendation(cls, search_for, price, path):
        search_divar = Divar.search(search_for)
        divar_name = difflib.get_close_matches(search_for, search_divar.keys(), 1, 0.1)

        return {search_for: [[price, path], search_divar[divar_name]]}
    
print(Matching.search("iphone 13"))
Matching.search("iphone 13").to_csv("Match.csv")