from DigikalaFinal import Digikala
from DivarFinal import Divar
from SheypoorFinal import Sheypoor
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
    
    @staticmethod
    def search(search_for):
        t1 = CustomThread(target=Digikala.search, args=(search_for,))
        t2 = CustomThread(target=Divar.search, args=(search_for,))
        t3 = CustomThread(target=Sheypoor.search, args=(search_for,))
        t1.start()
        t2.start()
        t3.start()
        search_digikala = t1.join()
        search_divar = t2.join()
        search_sheypoor = t3.join()
        search_digikala.to_csv("products information\\digikala.csv")
        sellers = pd.concat([search_divar, search_sheypoor], axis=0)  
        sellers = sellers.set_index("name")
        sellers.to_csv("products information\\sellers.csv")



    @staticmethod
    def click(digi_name, sellers_address):
        sellers = pd.read_csv(sellers_address)
        sellers = sellers.set_index("name")

        matched_names = difflib.get_close_matches(digi_name, list(sellers.index), 6, 0.1)
        matched_sellers = sellers.loc[[i for i in matched_names]]
        return matched_sellers
