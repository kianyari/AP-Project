import productwindow
import main
from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap
import pandas as pd
from MatchingFinal import Matching, CustomThread
from DigikalaFinal import Digikala
import Menu
from functools import partial


class mainWindow(QtWidgets.QMainWindow):
    """
    menuBarBtn: go to menu page that include -> 1.categories  2.favorite list  3.compare list
    searchBarTorob: line edit that user input his need in this section
    doSearchBtn: button that send user input to us to search it in websites
    profileInfoBtn: shows user information
    product1-6: shape of behind the products info -> parent for graphic
    productBtn1-6: when we hit the product action this button will do the transfer
    productName1-6: digikala name of product
    productPrice1-6: digikala price of product
    """
    def __init__(self):
        """
        create the first view of app and connect back and front
        """
        super(mainWindow, self).__init__() # pyqt5 stuff don't care =)
        self.ui_address = "main ui\\main window.ui" # ui file of this Class
        loadUi(self.ui_address, self) # actualli connect the graphic from the ui file into the backend
        self.doSearchBtn.clicked.connect(self.do_search)
        self.menuBarBtn.clicked.connect(mainWindow.go_menu)
        try:
            # if user search sth so csv file with this path created
            digikala_data = pd.read_csv("products information\\digikala.csv")
        except:
            # if user haven't search yet so we follow our products database
            digikala_data = pd.read_csv("src data first window\\fisrt window digikala.csv")
        
        row, col = digikala_data.shape # to get size of dataframe(database)
        
        # if output is less than 6 result so we hide the other empty objects
        for i in range(row, 6): 
            eval(f"self.product{i + 1}.setStyleSheet(u'color: rgba(0, 0, 0, 0);')")
            eval(f"self.product{i + 1}.setStyleSheet(u'border-color: rgba(0, 0, 0, 0);')")
            eval(f"self.productBtn{i + 1}.setStyleSheet(u'color: rgba(0, 0, 0, 0);')")
            eval(f"self.productBtn{i + 1}.setStyleSheet(u'border-color: rgba(0, 0, 0, 0);')")
            eval(f"self.productPhoto{i + 1}.setStyleSheet(u'color: rgba(0, 0, 0, 0);')")

        
        for i in range(row):
            self.pixmap = QPixmap("image src\\" + digikala_data.loc[i, 'name']) # get image of products
            eval(f"self.productName{i + 1}.setText(digikala_data.loc[i, 'name'])") # set name of each product
            eval(f"self.productPrice{i + 1}.setText(str(digikala_data.loc[i, 'price']))") # set price of each product
            eval(f"self.productPhoto{i + 1}.setPixmap(self.pixmap)") # set image of each product
            # when we hit each product it must to do thinngs for us:
            eval(f"self.productBtn{i + 1}.clicked.connect(partial(self.click_product,digikala_data.loc[i, 'name'], str(digikala_data.loc[i, 'id'])))")


    def click_product(self, product_name, product_id):
        """
        find sellers and detail of the product
        to increase the speed this method is multi thread
        after all of that we go to the productwindow module to go to the next step
        """
        try:
            sellers_address = "products information\\sellers.csv"
            pd.read_csv(sellers_address)
        except:
            sellers_address = "src data first window\\first window sellers.csv"

        # find the sellers with Matching module
        t1 = CustomThread(target= Matching.click, args= (product_name, sellers_address))
        # find the details with Digikala module
        t2 = CustomThread(target= Digikala.details, args=(product_id,)) 
        t1.start()
        t2.start()
        matched_sellers = t1.join()
        product_details = t2.join()

        try:
            # user search exist
            product_database_address = "products information\\digikala.csv"
            pd.read_csv(product_database_address)
        except:
            # user nothing searched yet so we go to our database
            product_database_address = "src data first window\\fisrt window digikala.csv"

        # go to the productwindow module
        product_window = productwindow.ProductWindow(
            product_name,
            matched_sellers,
            product_details,
            product_database_address,
            )
        main.Main.widget.addWidget(product_window)
        main.Main.widget.setCurrentIndex(main.Main.widget.currentIndex()+1)

    def do_search(self):
        """
        get user search input and use it in matching module
        refresh the main window to show the results
        """
        Matching.search(self.searchBarTorob.text())
        main_window = mainWindow()
        main.Main.widget.addWidget(main_window)
        main.Main.widget.setCurrentIndex(main.Main.widget.currentIndex()+1) # refresh the window

    def go_menu():
        """
        go to the menu window when user hit the menu button
        """
        menu_page = Menu.MenuWindow()
        main.Main.widget.addWidget(menu_page)
        main.Main.widget.setCurrentIndex(main.Main.widget.currentIndex()+1)